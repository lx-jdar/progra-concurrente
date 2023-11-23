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
img_tablero=pygame.image.load("Imagenes/tablero2.png")
fondo = pygame.transform.scale(img_tablero, (800,600))
img_x=pygame.image.load("Imagenes/x2.png")
ocupado = pygame.transform.scale(img_x, (ANCHO_CABALLO,ALTO_CABALLO))

threads = []
VELOCIDAD = 1

class Tablero:
        casillas = np.full((TAM_TABLERO, TAM_TABLERO),True)
        def actualizar(self):
                ventana.blit(fondo,(0,0))
                for i in range(0,TAM_TABLERO):
                   for j in range(0,TAM_TABLERO):
                    if tablero.casillas[i][j] == False:
                        ventana.blit(ocupado,(43+i*92,j*68+38))
                
                

                        
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
                  ventana.blit(caballo.pieza_caba,(43+self.posX*92,self.posY*68+38))
                  tablero.casillas[new_posX][new_posY]=False
                  self.calcularMov(tablero)
                  return
                print(self.movimientosPosibles)
                if '{}{}'.format(new_posX,new_posY) in self.movimientosPosibles and  tablero.casillas[new_posX][new_posY]!=False:
                        tablero.casillas[new_posX][new_posY]=False
                        self.animacion(new_posX,new_posY,tablero)
                        self.posX = new_posX
                        self.posY = new_posY

                self.movimientosPosibles={}
                self.calcularMov(tablero)
        def animacion(self,new_posX,new_posY,tablero):
                pos_pixelX_actual=43+self.posX*92;
                pos_pixelY_actual=self.posY*68+38;
                new_pos_pixelX=43+new_posX*92;
                new_pos_pixelY=new_posY*68+38;
                while (pos_pixelX_actual!=new_pos_pixelX):
                        tablero.actualizar()
                        if pos_pixelX_actual>new_pos_pixelX :
                          pos_pixelX_actual-=VELOCIDAD
                          ventana.blit(caballo.pieza_caba,(pos_pixelX_actual,pos_pixelY_actual))
                        if pos_pixelX_actual<new_pos_pixelX :
                          pos_pixelX_actual+=VELOCIDAD
                          ventana.blit(caballo.pieza_caba,(pos_pixelX_actual,pos_pixelY_actual))
                while (pos_pixelY_actual!=new_pos_pixelY):
                        tablero.actualizar()
                        if pos_pixelY_actual>new_pos_pixelY :
                          pos_pixelY_actual-=VELOCIDAD
                          ventana.blit(caballo.pieza_caba,(pos_pixelX_actual,pos_pixelY_actual))
                        if pos_pixelY_actual<new_pos_pixelY :
                          pos_pixelY_actual+=VELOCIDAD
                          ventana.blit(caballo.pieza_caba,(pos_pixelX_actual,pos_pixelY_actual))


        
        def calcularMov(self,tablero):
                if(self.posX - 2) >= 0:
                 if(self.posY - 1) >= 0:
                        self.movimientosPosibles['{}{}'.format(self.posX-2, self.posY-1)]=tablero.casillas[self.posX-2][self.posY-1]
                 if(self.posY + 1) <= 7:
                        self.movimientosPosibles['{}{}'.format(self.posX-2, self.posY+1)]=tablero.casillas[self.posX-2][self.posY+1]

                if(self.posY - 2) >= 0:
                 if(self.posX - 1) >= 0:
                         self.movimientosPosibles['{}{}'.format(self.posX-1, self.posY-2)]=tablero.casillas[self.posX-1][self.posY-2]
                 if(self.posX + 1) <= 7:
                         self.movimientosPosibles['{}{}'.format(self.posX+1, self.posY-2)]=tablero.casillas[self.posX+1][self.posY-2]


                if(self.posX + 2) <= 7:
                 if(self.posY - 1) >= 0:
                         self.movimientosPosibles['{}{}'.format(self.posX+2, self.posY-1)]=tablero.casillas[self.posX+2][self.posY-1]
                 if(self.posY + 1) <= 7:
                         self.movimientosPosibles['{}{}'.format(self.posX+2, self.posY+1)]=tablero.casillas[self.posX+2][self.posY+1]

                if(self.posY + 2) <= 7:
                  if(self.posX - 1) >= 0:
                        self.movimientosPosibles['{}{}'.format(self.posX-1, self.posY+2)]=tablero.casillas[self.posX-1][self.posY+2]
                  if(self.posX + 1) <= 7:
                        self.movimientosPosibles['{}{}'.format(self.posX+1, self.posY+2)]=tablero.casillas[self.posX+1][self.posY+2]

     

def config_ini():
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
                caballo.mover(int((posX-38)/92),int((posY-24)/68),tablero)
          pygame.display.update()





thread_exit.join()
