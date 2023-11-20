import pygame
import threading
import time

class TableroAjedrezGame:
    MAX_THREADS = 3

    __instance = None
    __threads = []
    __running: bool = False
    __ventana = None
    __img_tablero = None
    __fondo = None
    # barrera para iniciar todos los threads luego de la config
    __bar = threading.Barrier(MAX_THREADS) 
    __sem_conf = threading.BoundedSemaphore(1)
    __sem_display = threading.BoundedSemaphore(1)

    @classmethod
    def get__instance(cls): # Nuestron constructor alternativo
        if not cls.__instance:
            cls.__instance = cls.__new__(cls)
        return cls.__instance
    
    def init(self):
        self.__threads.append(threading.Thread(target=self.load_config))
        self.__threads.append(threading.Thread(target=self.gestion_pantalla))
        self.__threads.append(threading.Thread(target=self.gestion_movimiento))
        [t.start() for t in self.__threads]
        
    def finish(self):
        [t.join() for t in self.__threads]
            
    ########################################
    # Aca creo los objetos Tablero y Caballo
    ########################################
    def load_config(self):
        self.__running = True
        pygame.init()
        
        self.__ventana = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Caballo de Ajedrez")

        self.__img_tablero=pygame.image.load("tp_integrador/Imagenes/tablero2.png")        
        self.__fondo = pygame.transform.scale(self.__img_tablero, (800,600))
        self.__bar.wait()
        while self.__running:
            self.__sem_conf.acquire()

    ####################################################
    # Muestro los cambios una vez obtenidos los valores
    ####################################################
    def gestion_pantalla(self):
        #self.__sem_display.acquire()
        self.__bar.wait()
        self.__ventana.blit(self.__fondo,(0,0))
        print("hilo gestion_pantalla\n")
        while self.__running:
            # Todos los elementos del juego se vuelven a dibujar
            #self.__sem_display.release()
            pygame.display.update()
            #self.__sem_display.acquire()
            # Controlamos la frecuencia de refresco (FPS)
            #pygame.time.Clock().tick(60)
            
            
    ########################################
    # invoco los algoritmos de caballo
    ########################################
    def gestion_movimiento(self):
        self.__sem_conf.acquire()
        self.__bar.wait()
        self.__sem_display.acquire()
        update_screen = False
        print("hilo gestion_movimiento\n")
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                    self.__sem_display.release()
                    self.__sem_conf.release()
                if event.type == pygame.MOUSEBUTTONUP:
                    posX,posY=pygame.mouse.get_pos()
                    print(posX, posY)
                    update_screen = True
                    
            if update_screen:
                #self.__sem_display.release()
                update_screen = False
                #self.__sem_display.acquire()

def main():
    game = TableroAjedrezGame().get__instance()
    game.init()
    game.finish()


if __name__ == "__main__":
    main()