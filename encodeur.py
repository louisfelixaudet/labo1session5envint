import threading
import time
from gpiozero import DigitalInputDevice
from algoPos import AlgoPos

CIRCONFERENCE_CM = 21.5
TRANSITIONS_PAR_TOUR = 40          # 20 fentes × 2 bords
CM_PAR_TICK = CIRCONFERENCE_CM / TRANSITIONS_PAR_TOUR  # ≈ 0.5375
DT = 0.040                         # 40 ms


class EncodeurRoue:
    def __init__(self, pin):
        self._n = 0
        self._lock = threading.Lock()
        self.dev = DigitalInputDevice(pin, pull_up=False, bounce_time=0.0005)
        self.dev.when_activated = self._tick
        self.dev.when_deactivated = self._tick   # les 2 transitions comptent

    def _tick(self):
        with self._lock:
            self._n += 1

    def consommer(self):
        with self._lock:
            n = self._n
            self._n = 0
            return n

    def close(self):
        self.dev.close()


class Odometrie:
    def __init__(self, pin_g=17, pin_d=27):
        self.algo = AlgoPos()
        self.enc_g = EncodeurRoue(pin_g)
        self.enc_d = EncodeurRoue(pin_d)
        self.signe_g = 0
        self.signe_d = 0

        self.x = 0.0
        self.y = 0.0
        self.angle = 0.0           # rad
        self.distance = 0.0        # cm cumulés
        self.vg = self.vd = self.v = 0.0   # cm/s

        self._stop = threading.Event()
        threading.Thread(target=self._boucle, daemon=True).start()

    def set_signes(self, sg, sd):
        self.signe_g = sg
        self.signe_d = sd

    def _boucle(self):
        t0 = time.monotonic()
        while not self._stop.wait(DT):
            t1 = time.monotonic()
            dt = t1 - t0
            t0 = t1
            self._update(dt if dt > 0 else DT)

    def _update(self, dt):
        dg = self.enc_g.consommer() * CM_PAR_TICK * self.signe_g
        dd = self.enc_d.consommer() * CM_PAR_TICK * self.signe_d

        dtheta = self.algo.calculeOrientation(dd, dg)
        d = self.algo.calculeDistance(dd, dg)
        dx = self.algo.deplcementX(d, self.angle, dtheta)
        dy = self.algo.deplcementY(d, self.angle, dtheta)

        self.x = self.algo.getX(self.x, dx)
        self.y = self.algo.getY(self.y, dy)
        self.angle = self.algo.getOrientation(self.angle, dtheta)
        self.distance += abs(d)

        self.vg = dg / dt
        self.vd = dd / dt
        self.v = d / dt

    def __str__(self):
        return (
            f"d={self.distance:.1f} cm  v={self.v:.1f} cm/s "
            f"(vg={self.vg:.1f} vd={self.vd:.1f})  "
            f"pos=({self.x:.1f},{self.y:.1f})  "
            f"θ={(self.angle * 180 / 3.1416) % 360:.1f}°"
        )

    def close(self):
        self._stop.set()
        self.enc_g.close()
        self.enc_d.close()