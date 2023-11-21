import pygame
import random
import threading
import time


class TableroAjedrezGame:

    __instance = None

    # Set up the window
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    MAX_THREADS = 2

    __screen = None

    __img_tablero = None
    __img_tablero_rect = None

    __caballo = None
    __caballo_rect = None

    __update_horse = False
    __running = False

    __threads = []

    # barrera para iniciar todos los threads luego de la config
    __bar = None

    @classmethod
    def get__instance(cls): # Nuestron constructor alternativo
        if not cls.__instance:
            cls.__instance = cls.__new__(cls)
        return cls.__instance

    def load_config(self):
        # Initialize Pygame
        pygame.init()
        self.__screen = pygame.display.set_mode((self.WINDOW_WIDTH,self.WINDOW_HEIGHT))
        pygame.display.set_caption("Caballo de Ajedrez")

        self.__img_tablero = pygame.image.load("PyGamePractice/btablero2.png").convert()
        self.__img_tablero = pygame.transform.scale(self.__img_tablero, (self.WINDOW_WIDTH,self.WINDOW_HEIGHT))
        # Obtengo el rectángulo del objeto anterior
        self.__img_tablero_rect = self.__img_tablero.get_rect()
        # Pongo la tablero en el origen de coordenadas
        self.__img_tablero_rect.move_ip(0,0)

        self.__caballo = pygame.image.load("PyGamePractice/caballo.jpg")
        self.__caballo = pygame.transform.scale(self.__caballo, (70, 50))
        self.__caballo_rect = self.__caballo.get_rect()
        #self.__caballo_rect.move_ip(42+1*92,36+1*68)

        self.__screen.blit(self.__img_tablero, self.__img_tablero_rect)
        #self.__screen.blit(self.__caballo, self.__caballo_rect)
        pygame.display.flip()
        self.__update_horse = False
        self.__running = True
    
    def init(self):
        
        self.__bar = threading.Barrier(self.MAX_THREADS, action=self.load_config) 

        # Create 10 threads for drawing shapes
        self.__threads.append(threading.Thread(target=self.draw_thread))
        
        [t.start() for t in self.__threads]
        
        self.__bar.wait()
        # Main loop
        while self.__running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    posX,posY=pygame.mouse.get_pos()
                    print(posX,posY)
                    new_posX, new_posY = int((posX-31)/92),int((posY-24)/69)
                    print(new_posX,new_posY)
                    self.__caballo_rect.x=43+new_posX*92.3
                    self.__caballo_rect.y=35+new_posY*69
                    self.__update_horse = True

            # Update the screen
            pygame.display.update()
        pygame.quit()

    # Define a function for drawing a shape with a random color and size
    def draw_shape(self):
        if self.__update_horse:
            self.__screen.blit(self.__caballo, self.__caballo_rect)
            pygame.display.update(self.__caballo_rect)
            self.__update_horse = False
        pygame.time.Clock().tick(60)

    # Define a function for creating threads that draw shapes
    def draw_thread(self):
        self.__bar.wait()
        while self.__running:
            # Draw a shape
            self.draw_shape()
    
    def finish(self):
        [t.join() for t in self.__threads]

def main():
    game = TableroAjedrezGame().get__instance()
    game.init()
    game.finish()


if __name__ == "__main__":
    main()