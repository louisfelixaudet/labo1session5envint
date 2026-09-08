import socket
import select
import os
import threading
import sys
import struct
import time

from ev_app_client_api import *

HOST_IP            = "127.0.0.1"  # Écoute sur loop back uniquement
#HOST_IP             = "0.0.0.0"    # Écoute sur toutes les interfaces

class EvDesc:
    def __init__(self, type, donnée):
        try:
            ev_ty = int(type)
            self.type = ev_ty
            self.donnée = donnée
        except ValueError:
            print(f"ev_ty doit-être un entier -> {type}")
            raise

    def __repr__(self):
        return f"{self.type}::{self.donnée}"
    
    def split(self):
        return self.donnée.split(";")
 
class EvApp:
    def __init__(self, port_no=8999, tmo=4):  # tmo = 4 s pour éviter de gelé dans select 
                                              # et ignorer les Ctrl-C
        self._termine = False
        self.tmo = tmo

        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_sock.setblocking(False)
        self.udp_sock.bind((HOST_IP, port_no))

    def dispatch_event(self, ev):  # À spécialiser
        print(ev)

    def quitter_app(self):
        self._termine = True
        self.quitter()

    def quitter(self):             # À spécialiser
        pass

    def run(self):
        try:
            while not self._termine:
                readable, _, _ = select.select([self.udp_sock], [], [], self.tmo)
                if len(readable) == 0:        
                    ev_ty, ev_data = (0, f"{time.time():.4f}")
                    ev = EvDesc(ev_ty, ev_data)
                    self.dispatch_event(ev)
                else:
                    for sock in readable:
                        if sock == self.udp_sock:
                            msg, _ = sock.recvfrom(TAILLE_MSG_TOT)
                            ev_ty, ev_data = struct.unpack(MSG_PACK_FORMAT, msg)
                            #print("ev_ty:", ev_ty, "ev_data:", ev_data)
                            ev = EvDesc(ev_ty, ev_data.decode('utf-8').strip('\x00'))

                        self.dispatch_event(ev)
        except KeyboardInterrupt:
            print(f"Quitter EvApp")
            self.quitter_app()
        finally:
            self.udp_sock.close()
            print(f"Thank you for flying with us")