import pygame
from pygame.locals import *

import random
##from tkinter import messagebox
import ctypes
JOGADOR_ALTURA     = 20
JOGADOR_LARGURA    = 80
JOGADOR_COR        = (255, 99, 99)
JOGADOR_VELOCIDADE = 5

BOLINHA_ALTURA     = 20
BOLINHA_LARGURA    = 20
BOLINHA_COR        = (255, 99, 99)
BOLINHA_VELOCIDADE = 4

CENARIO_COR          = (0, 0, 0)
CENARIO_LIMITE_ESQ   = 0
CENARIO_LIMITE_DIR   = 640
CENARIO_LIMITE_CIMA  = 0
CENARIO_LIMITE_BAIXO = 400

COR_BLOCO_VERMELHO = (255, 0,   0)
COR_BLOCO_LARANJA  = (252, 146, 7)
COR_BLOCO_AMARELO  = (252, 252, 7)
COR_BLOCO_VERDE    = (90 , 252, 7)
COR_BLOCO_AZUL     = (36 , 7,   252)

NUM_BLOCOS_POR_LINHA = 8
NUM_LINHAS = 5

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

        ############################################
        ############ Inicializando tela ############
        ############################################

        self._display_surf.fill(CENARIO_COR)

        self.blocos = [
            [True, True, True, True, True, True, True, True],
            [True, True, True, True, True, True, True, True],
            [True, True, True, True, True, True, True, True],
            [True, True, True, True, True, True, True, True],
            [True, True, True, True, True, True, True, True]
        ]
        ## janela tem 640 largura e 400 de altura
        ## cada bloquinho tem 640/8 = 80 de largura
        ############################################
        ########## Inicializando jogador ###########
        ############################################

        self.mover_bolinha = False

        self.mover_esquerda = False
        self.mover_direita  = False

        self.x_jogador = 280
        self.y_jogador = 330

        self._display_surf.fill(JOGADOR_COR, (self.x_jogador, self.y_jogador, JOGADOR_LARGURA, JOGADOR_ALTURA))

        ############################################
        ########## Inicializando bolinha ###########
        ############################################

        self.bolinha_esquerda = True
        self.bolinha_baixo    = True

        self.x_bolinha = self.x_jogador + JOGADOR_LARGURA / 2
        self.y_bolinha = self.y_jogador - 2 * BOLINHA_ALTURA

        self.x_bolinha -= 10
        self.y_bolinha += 15

        self._display_surf.fill(BOLINHA_COR, (self.x_bolinha, self.y_bolinha, BOLINHA_LARGURA, BOLINHA_ALTURA))

        pygame.display.update()

        return True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            self.mover_bolinha = True

            if event.key == pygame.K_LEFT:
                if self.x_jogador > CENARIO_LIMITE_ESQ:
                    self.mover_esquerda = True
            elif event.key == pygame.K_RIGHT:
                if self.x_jogador + JOGADOR_LARGURA < CENARIO_LIMITE_DIR:
                    self.mover_direita = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.mover_esquerda = False
            elif event.key == pygame.K_RIGHT:
                self.mover_direita = False

    def on_loop(self):
        clock = pygame.time.Clock()

        clock.tick(60)

        if self.mover_esquerda:
            if self.x_jogador > CENARIO_LIMITE_ESQ:
                self.x_jogador -= JOGADOR_VELOCIDADE
        elif self.mover_direita:
            if self.x_jogador + JOGADOR_LARGURA < CENARIO_LIMITE_DIR:
                self.x_jogador += JOGADOR_VELOCIDADE

        if self.mover_bolinha:
            if self.bolinha_esquerda:
                if self.x_bolinha > CENARIO_LIMITE_ESQ:
                    self.x_bolinha -= BOLINHA_VELOCIDADE
                else:
                    self.bolinha_esquerda = False
            else:
                if self.x_bolinha + BOLINHA_LARGURA < CENARIO_LIMITE_DIR:
                    self.x_bolinha += BOLINHA_VELOCIDADE
                else:
                    self.bolinha_esquerda = True

            if self.bolinha_baixo:
                if self.y_bolinha + BOLINHA_ALTURA < CENARIO_LIMITE_BAIXO:
                    self.y_bolinha += BOLINHA_VELOCIDADE
                else:
                    self.bolinha_baixo = False
            else:
                if self.y_bolinha > CENARIO_LIMITE_CIMA:
                    self.y_bolinha -= BOLINHA_VELOCIDADE
                else:
                    self.bolinha_baixo = True
        

        if self.y_bolinha + BOLINHA_ALTURA >= CENARIO_LIMITE_BAIXO:
            resposta = ctypes.windll.user32.MessageBoxW(0, 'Deseja jogar novamente?', 'Derrota!', 5)
            if resposta == 4:
                self.on_init() ## repetir = 4
            else:
                self._running = False
            
        
        rect_jogador = Rect(self.x_jogador, self.y_jogador, JOGADOR_LARGURA, JOGADOR_ALTURA)

        rect_bolinha = Rect(self.x_bolinha, self.y_bolinha, BOLINHA_LARGURA, BOLINHA_ALTURA)

        if rect_jogador.colliderect(rect_bolinha):
            self.bolinha_baixo = False

        y_bloco = 20
        x_bloco = 0


        ### 0<=indiceLinha<NUM_LINHAS
        
        ### 0<=indiceColunas<NUM_BLOCOS_POR_LINHA
        ganhou = True
        for indiceLinha in range(0,NUM_LINHAS) :
            for indiceColuna in range(0,NUM_BLOCOS_POR_LINHA):
                rect_bloco = Rect(x_bloco, y_bloco, JOGADOR_LARGURA, JOGADOR_ALTURA)
                if self.blocos[indiceLinha][indiceColuna]:
                    ganhou = False
                    if rect_bolinha.colliderect(rect_bloco):
                        self.blocos[indiceLinha][indiceColuna] = False
                        
                        self.bolinha_baixo = not self.bolinha_baixo

                x_bloco += JOGADOR_LARGURA

            x_bloco = 0
            y_bloco += JOGADOR_ALTURA
            
        if ganhou:
            resposta = ctypes.windll.user32.MessageBoxW(0, 'Deseja jogar novamente?', 'Vitória!', 5)
            if resposta:
                self.on_init()
            else:
                self._running = False


    def on_render(self):
        self._display_surf.fill(CENARIO_COR)

        self._display_surf.fill(JOGADOR_COR, (self.x_jogador, self.y_jogador, JOGADOR_LARGURA, JOGADOR_ALTURA))

        self._display_surf.fill(BOLINHA_COR, (self.x_bolinha, self.y_bolinha, BOLINHA_LARGURA, BOLINHA_ALTURA))

        indice_linha = 0
        y_bloco = 20
        x_bloco = 0
        for linha in self.blocos:
            for bloco in linha:
                if bloco:
                    if indice_linha == 0:
                        self._display_surf.fill(COR_BLOCO_VERMELHO, (x_bloco, y_bloco, JOGADOR_LARGURA, JOGADOR_ALTURA))
                    elif indice_linha == 1:
                        self._display_surf.fill(COR_BLOCO_LARANJA, (x_bloco, y_bloco, JOGADOR_LARGURA, JOGADOR_ALTURA))
                    elif indice_linha == 2:
                        self._display_surf.fill(COR_BLOCO_AMARELO, (x_bloco, y_bloco, JOGADOR_LARGURA, JOGADOR_ALTURA))
                    elif indice_linha == 3:
                        self._display_surf.fill(COR_BLOCO_VERDE, (x_bloco, y_bloco, JOGADOR_LARGURA, JOGADOR_ALTURA))
                    elif indice_linha == 4:
                        self._display_surf.fill(COR_BLOCO_AZUL, (x_bloco, y_bloco, JOGADOR_LARGURA, JOGADOR_ALTURA))

                x_bloco += JOGADOR_LARGURA

            x_bloco = 0
            y_bloco += JOGADOR_ALTURA

            indice_linha += 1

        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()