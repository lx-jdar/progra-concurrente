import os
import random
import threading
import pygame
import sys
import numpy as np
from pygame.locals import*

DESPLAZAMIENTO_X = 43
DESPLAZAMIENTO_Y = 38
MULTIPLICADOR_X  = 92
MULTIPLICADOR_Y  = 68
DESPLAZAMIENTO_GAME_OVER_X= 200
DESPLAZAMIENTO_GAME_OVER_Y= 200
ANCHO_GAME_OVER= 400
ALTO_GAME_OVER  = 200
ANCHO_CABALLO = 70
ALTO_CABALLO  = 50
TAM_TABLERO = 8
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

img_tablero = None
fondo = None
img_x = None
ocupado = None
ventana = None
running = True
global victoria
global derrota
derrota=False
victoria=False

sem_init = threading.Semaphore(0)	
threads = []

def derrota_o_victoria():
        
        global victoria
        global derrota
        victoria=False
        derrota  = False
        while running:
                if caballo.cant_mov == 64:
                        victoria = True
                        ventana.blit(win,(DESPLAZAMIENTO_GAME_OVER_X,DESPLAZAMIENTO_GAME_OVER_Y))
                        return;
                elif not(True in caballo.movimientosPosibles.values()) and False in caballo.movimientosPosibles.values():
                        print(tablero.casillas)
                        ventana.blit(game_over,(DESPLAZAMIENTO_GAME_OVER_X,DESPLAZAMIENTO_GAME_OVER_Y))
                        derrota = True
                        return;
                                    
#Funcion para actualizar el tablero en pantalla            
def hilo_actualizar(tablero,fila):
        for columna in range (0,TAM_TABLERO):
           if tablero.casillas[fila][columna] == False:
             ventana.blit(ocupado,(DESPLAZAMIENTO_X+fila*MULTIPLICADOR_X,DESPLAZAMIENTO_Y+columna*MULTIPLICADOR_Y)) 

class Tablero:
        
        casillas = np.full((TAM_TABLERO, TAM_TABLERO),True)
        #Metodo para actualizar la pantalla con cada una de las casillas por donde paso el jugador
        def actualizar(self):
                hilos_actua=[]
                ventana.blit(fondo,(0,0))
                for i in range(0, TAM_TABLERO ):
                     hilo = threading.Thread(target=hilo_actualizar, args=(self,i))
                     hilo.start()
                     hilos_actua.append(hilo)  
                for hilo in hilos_actua:
                     hilo.join()

        #Metodo para necesario para reiniciar el juego
        def restart(self):
                self.casillas = np.full((TAM_TABLERO, TAM_TABLERO),True)

class Caballo:
        img_caballo=pygame.image.load("tp_integrador/Imagenes/caballo.jpg")
        pieza_caba = pygame.transform.scale(img_caballo, (ANCHO_CABALLO, ALTO_CABALLO))
        movimientosPosibles={}
        posX = -1
        posY = -1
        cant_mov=0;
        movimientos_anteriores=[]
        movimientos_deshechos=[]

        #Metodo necesario para mover al caballo
        def mover( self,new_posX, new_posY,tablero):
                if self.posX ==-1 and new_posX>=0 and new_posX<=7 and new_posY>=0 and new_posY<=7:    
                        self.posX = new_posX
                        self.posY = new_posY
                        ventana.blit(self.pieza_caba,(DESPLAZAMIENTO_X+new_posX*MULTIPLICADOR_X,DESPLAZAMIENTO_Y+new_posY*MULTIPLICADOR_Y))
                        tablero.casillas[new_posX][new_posY]=False
                        self.calcularMov(tablero)
                        self.cant_mov+=1
                  
                elif '{}{}'.format(new_posX,new_posY) in self.movimientosPosibles and  tablero.casillas[new_posX][new_posY]!=False:
                        tablero.casillas[self.posX ][self.posY ]=False
                        self.movimientos_anteriores.append((self.posX,self.posY))
                        self.posX = new_posX
                        self.posY = new_posY
                        tablero.actualizar()
                        self.cant_mov+=1
                        ventana.blit(self.pieza_caba,(DESPLAZAMIENTO_X+new_posX*MULTIPLICADOR_X,DESPLAZAMIENTO_Y+new_posY*MULTIPLICADOR_Y)) 
                        self.movimientosPosibles={}
                        self.calcularMov(tablero)
        
        #metodo para deshacer los movimientos hechos (UNDO)
        def volver_atras(self,tablero):
                if self.movimientos_anteriores:
                        new_posX,new_posY=self.movimientos_anteriores.pop()
                        self.movimientos_deshechos.append((self.posX,self.posY))
                        tablero.casillas[new_posX][new_posY ]=True
                        new_pos_pixelX=DESPLAZAMIENTO_X+new_posX*MULTIPLICADOR_X;
                        new_pos_pixelY=DESPLAZAMIENTO_Y+new_posY*MULTIPLICADOR_Y;
                        self.posX = new_posX
                        self.posY = new_posY
                        tablero.actualizar()
                        ventana.blit(caballo.pieza_caba,(new_pos_pixelX,new_pos_pixelY))
                        self.movimientosPosibles={}
                        self.calcularMov(tablero)
                        self.cant_mov-=1;
        #Metodo para volver a realizar los movimientos deshechos (REDO)             
        def volver_adelante(self,tablero):
                if self.movimientos_deshechos:
                   new_posX,new_posY=self.movimientos_deshechos.pop()
                   self.mover(new_posX,new_posY,tablero)
                   
        #Metodo para necesario para reiniciar el juego
        def restart(self):
                self.movimientosPosibles={}
                self.posX = -1
                self.posY = -1
                self.cant_mov=0
                self.movimientos_anteriores = []
                self.movimientos_deshechos = []

        #Metodo para facilitar el ingreso de tuplas en el diccionario
        def get_key(self,val_x,val_y):
                return '{}{}'.format(self.posX+val_x, self.posY+val_y)   
        

        #Metodo donde verifico todos los movimientos posibles de un caballo en una determinada posicion
        def calcularMov(self,tablero):
                if(self.posX - 2) >= 0:
                 if(self.posY - 1) >= 0:
                        self.movimientosPosibles[self.get_key(-2,-1)]=tablero.casillas[self.posX-2][self.posY-1]
                 if(self.posY + 1) <= 7:
                        self.movimientosPosibles[self.get_key(-2,1)]=tablero.casillas[self.posX-2][self.posY+1]

                if(self.posY - 2) >= 0:
                 if(self.posX - 1) >= 0:
                         self.movimientosPosibles[self.get_key(-1,-2)]=tablero.casillas[self.posX-1][self.posY-2]
                 if(self.posX + 1) <= 7:
                         self.movimientosPosibles[self.get_key(1,-2)]=tablero.casillas[self.posX+1][self.posY-2]


                if(self.posX + 2) <= 7:
                 if(self.posY - 1) >= 0:
                         self.movimientosPosibles[self.get_key(2,-1)]=tablero.casillas[self.posX+2][self.posY-1]
                 if(self.posY + 1) <= 7:
                         self.movimientosPosibles[self.get_key(2,1)]=tablero.casillas[self.posX+2][self.posY+1]

                if(self.posY + 2) <= 7:
                  if(self.posX - 1) >= 0:
                        self.movimientosPosibles[self.get_key(-1,2)]=tablero.casillas[self.posX-1][self.posY+2]
                  if(self.posX + 1) <= 7:
                        self.movimientosPosibles[self.get_key(1,2)]=tablero.casillas[self.posX+1][self.posY+2]

#Clase creada para realizar la configuracion inicial del tablero, utilizando hilos 
class ConfigThread(threading.Thread):

    def __init__(self):
        super().__init__()

    def run(self):

        global  img_tablero, fondo, img_x, ocupado,img_game_over,game_over,win
        pygame.mixer.music.load('tp_integrador/Musica/musica.mp3')
        pygame.mixer.music.play(-1)
        img_tablero = pygame.image.load("tp_integrador/Imagenes/tablero2.png")
        fondo = pygame.transform.scale(img_tablero, (WINDOW_WIDTH,WINDOW_HEIGHT))
        img_game_over=pygame.image.load("tp_integrador/Imagenes/game_over_2.png")
        game_over= pygame.transform.scale(img_game_over, (ANCHO_GAME_OVER,ALTO_GAME_OVER))
        img_win=pygame.image.load("tp_integrador/Imagenes/win.png")
        win= pygame.transform.scale(img_win, (ANCHO_GAME_OVER,ALTO_GAME_OVER))
        img_x = pygame.image.load("tp_integrador/Imagenes/X2.png")
        ocupado = pygame.transform.scale(img_x, (ANCHO_CABALLO,ALTO_CABALLO))

#Funcion que se le pasa a un hilo para que finalice el juego                    
def esperar_fin():
        global running
        sem_init.acquire()
        running = False        
        pygame.event.post(pygame.event.Event(pygame.QUIT))            
                    
#Funcion que se encarga de realizar toda la configuracion inicial como la inicializacion del display y carga de imagenes
def configuracion_inicial():
        global ventana
        pygame.init()
        pygame.display.set_caption("Caballo de Ajedrez")
        ventana = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        thread_config_ini  = ConfigThread()
        thread_config_ini.start()
        thread_config_ini.join()
        ventana.blit(fondo,(0,0))
        pygame.display.flip()

#Inicio del programa

#Creo hilos
thread_derrota_o_victoria=threading.Thread(target=derrota_o_victoria)
thread_esperar_fin = threading.Thread(target=esperar_fin)

caballo= Caballo()
configuracion_inicial()

#Lanzo los hilos
thread_esperar_fin.start()
thread_derrota_o_victoria.start()

tablero=Tablero()

#Mientras el booleano siga en True, el juego se va a seguir ejecutando, dentro del while capto todos los eventos y los proceso
while running:
        for evento in pygame.event.get():
          if evento.type == pygame.QUIT: #Evento se cierra el juego presionando en la "X"
                sem_init.release()
          if evento.type == pygame.MOUSEBUTTONUP: #Se hace click con el mouse
                posX,posY=pygame.mouse.get_pos()
                caballo.mover(int((posX-DESPLAZAMIENTO_X)/MULTIPLICADOR_X),int((posY-DESPLAZAMIENTO_Y)/MULTIPLICADOR_Y),tablero)
          elif evento.type == pygame.KEYDOWN: #Se presiona cualquier tecla del teclado
                if evento.key == pygame.K_z : #Se presiona la tecla "Z"
                 caballo.volver_atras(tablero)
                 if derrota == True or victoria == True: #Vuelve a crear el hilo si perdio o gano y desea volver atras
                    thread_derrota_o_victoria=threading.Thread(target=derrota_o_victoria)
                    thread_derrota_o_victoria.start()
                elif evento.key == pygame.K_y: #Se presiona la tecla "Y"
                 caballo.volver_adelante(tablero)
                elif evento.key == pygame.K_ESCAPE: #Se presiona la tecla "ESCAPE"
                 sem_init.release()
                elif evento.key == pygame.K_r: #Se presiona la tecla "R"
                 tablero=Tablero()
                 caballo= Caballo()
                 tablero.restart()
                 caballo.restart()
                 tablero.actualizar()
        
        pygame.display.update()
        if derrota == True:
             thread_derrota_o_victoria.join()
        elif victoria == True:
             thread_derrota_o_victoria.join()
             
        
        
pygame.quit()
sys.exit()
