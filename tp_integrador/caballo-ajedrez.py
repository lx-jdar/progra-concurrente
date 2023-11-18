import os
import random
import threading
import pygame
import sys
import numpy as np 
from pygame.locals import*
ANCHO_CABALLO = 70
ALTO_CABALLO  = 50
TAM_TABLERO = 8
threads = []

class Tablero:
        casillas = np.full((TAM_TABLERO, TAM_TABLERO),True)

                        
class Caballo:
        img_caballo=pygame.image.load("Imagenes/caballo.jpg")
        pieza_caba = pygame.transform.scale(img_caballo, (ANCHO_CABALLO, ALTO_CABALLO))
        movimientosPosibles={}
        posX = -1
        posY = -1


        def mover( self,new_posX, new_posY,tablero):
                if self.posX ==-1 and new_posX>=0 and new_posX<=7 and new_posY>=0 and new_posY<=7:    
                  self.posX = new_posX
                  self.posY = new_posY
                  ventana.blit(caballo.pieza_caba,(65+caballo.posX*85,caballo.posY*66+42))
                  tablero.casillas[new_posX][new_posY]=False
                  self.calcularMov(tablero)
                  return
                print(self.movimientosPosibles)
                if '{}{}'.format(new_posX,new_posY) in self.movimientosPosibles and tablero.casillas[new_posX][new_posY]:
                        tablero.casillas[new_posX][new_posY]=False
                        self.posX = new_posX
                        self.posY = new_posY
                        ventana.blit(caballo.pieza_caba,(65+caballo.posX*85,caballo.posY*66+42))
                self.movimientosPosibles={}
                self.calcularMov(tablero)
                 
        def calcularMov(self,tablero):
                if(self.posX - 2) >= 0:
                 if(self.posY - 1) >= 0:
                        self.movimientosPosibles['{}{}'.format(self.posX-2, self.posY-1)]=True
                 if(self.posY + 1) <= 7:
                        self.movimientosPosibles['{}{}'.format(self.posX-2, self.posY+1)]=True

                if(self.posY - 2) >= 0:
                 if(self.posX - 1) >= 0:
                         self.movimientosPosibles['{}{}'.format(self.posX-1, self.posY-2)]=True 
                 if(self.posX + 1) <= 7:
                         self.movimientosPosibles['{}{}'.format(self.posX+1, self.posY-2)]=True


                if(self.posX + 2) <= 7:
                 if(self.posY - 1) >= 0:
                         self.movimientosPosibles['{}{}'.format(self.posX+2, self.posY-1)]=True
                 if(self.posY + 1) <= 7:
                         self.movimientosPosibles['{}{}'.format(self.posX+2, self.posY+1)]=True

                if(self.posY + 2) <= 7:
                  if(self.posX - 1) >= 0:
                        self.movimientosPosibles['{}{}'.format(self.posX-1, self.posY+2)]=True
                  if(self.posX + 1) <= 7:
                        self.movimientosPosibles['{}{}'.format(self.posX+1, self.posY+2)]=True

     
        #validar_mov1(self,new_pos, new_posY)
        #validar_mov2(self,new_pos, new_posY)
        #validar_mov3(self,new_pos, new_posY)
        #validar_mov4(self,new_pos, new_posY)

def config_ini():
        img_tablero=pygame.image.load("Imagenes/tablero.png")
        fondo = pygame.transform.scale(img_tablero, (800,600))

        #Color=pygame.Color(70,80,150)
        ventana.blit(fondo,(0,0))
        #for i in range(0,9):
         #   pygame.draw.line(ventana,Color,(i*100,0),(i*100,600),10)
          #  pygame.draw.line(ventana,Color,(0,i*75),(800,75*i),10)
                      
def esperar_fin():
        while True:
                for evento in pygame.event.get():
                  if evento.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    thread_config_ini.join()


ventana= pygame.display.set_mode((800,600))
thread_confi_ini=threading.Thread(target=config_ini);
thread_confi_ini.start()
thread_exit = threading.Thread(target=esperar_fin);
thread_exit.start()

                

pygame.init()

pygame.display.set_caption("Hola Mundo")
tablero=Tablero()
caballo= Caballo()
print(tablero.casillas)
while True:
        for evento in pygame.event.get():
          if evento.type == pygame.MOUSEBUTTONUP:
                posX,posY=pygame.mouse.get_pos()
                print(posX)
                print(posY)
                caballo.mover(int((posX-55)/85),int((posY-36)/66),tablero)
          pygame.display.update()





thread_exit.join()
