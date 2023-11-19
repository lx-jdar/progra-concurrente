import pygame
import threading

class TableroAjedrezGame:
    __instance = None
    __threads = []

    @classmethod
    def get__instance(cls): # Nuestron constructor alternativo
        if not cls.__instance:
            cls.__instance
        return cls.__instance
    
    def init(self):
        self.__threads.append(threading.Thread(self.load_config))
        self.__threads.append(threading.Thread(self.gestion_pantalla))
        self.__threads.append(threading.Thread(self.gestion_movimiento))
    
    def load_config(self):
        self.img_tablero=pygame.image.load("Imagenes/tablero2.png")        
        self.fondo = pygame.transform.scale(self.img_tablero, (800,600))

    def gestion_pantalla(self):
        print("hilo movimientos") 

    def gestion_movimiento(self):
        print("hilo movimientos")

def main():
    game = TableroAjedrezGame().get__instance()



if __name__ == "__main__":
    main()