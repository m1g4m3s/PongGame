import pygame
import random

pygame.init()

largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Pong")

preto = (0, 0, 0)
branco = (255, 255, 255)
fonte = pygame.font.Font(None, 50)

class Bola:
    def __init__(self):
        self.largura = 20
        self.altura = 20
        self.x = largura_tela // 2 - self.largura // 2
        self.y = altura_tela // 2 - self.altura // 2
        self.velocidade_x = 6 * random.choice([1, -1])
        self.velocidade_y = 6 * random.choice([1, -1])

    def mover(self):
        self.x += self.velocidade_x
        self.y += self.velocidade_y

        if self.y <= 0 or self.y >= altura_tela - self.altura:
            self.velocidade_y *= -1

    def desenhar(self):
        pygame.draw.ellipse(tela, branco, (self.x, self.y, self.largura, self.altura))

class Raquete:
    def __init__(self, lado):
        self.largura = 20
        self.altura = 100
        self.velocidade = 7
        if lado == 'esquerda':
            self.x = 50
        else:
            self.x = largura_tela - 50 - self.largura
        self.y = altura_tela // 2 - self.altura // 2

    def mover(self, direcao):
        if direcao == 'up' and self.y - self.velocidade >= 0:
            self.y -= self.velocidade
        if direcao == 'down' and self.y + self.velocidade <= altura_tela - self.altura:
            self.y += self.velocidade

    def desenhar(self):
        pygame.draw.rect(tela, branco, (self.x, self.y, self.largura, self.altura))

def exibir_pontuacao(pontos_esquerda, pontos_direita):
    texto = fonte.render(f"{pontos_esquerda} - {pontos_direita}", True, branco)
    tela.blit(texto, (largura_tela // 2 - texto.get_width() // 2, 20))

def modo_single_player():
    bola = Bola()
    raquete_esquerda = Raquete('esquerda')
    raquete_direita = Raquete('direita')

    pontos_jogador = 0
    pontos_ia = 0
    fase = 1

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w]:
            raquete_esquerda.mover('up')
        if teclas[pygame.K_s]:
            raquete_esquerda.mover('down')

        if bola.y < raquete_direita.y + raquete_direita.altura // 2:
            if fase == 1:
                raquete_direita.y -= 4 
            elif fase == 2:
                raquete_direita.y -= 5
            else:
                raquete_direita.y -= 7 
        if bola.y > raquete_direita.y + raquete_direita.altura // 2:
            if fase == 1:
                raquete_direita.y += 4  
            elif fase == 2:
                raquete_direita.y += 5
            else:
                raquete_direita.y += 7  

        bola.mover()

        if (raquete_esquerda.x + raquete_esquerda.largura > bola.x and
            raquete_esquerda.y < bola.y < raquete_esquerda.y + raquete_esquerda.altura):
            bola.velocidade_x *= -1

        if (raquete_direita.x < bola.x + bola.largura and
            raquete_direita.y < bola.y < raquete_direita.y + raquete_direita.altura):
            bola.velocidade_x *= -1

        if bola.x <= 0:
            pontos_ia += 1
            bola = Bola()

        if bola.x >= largura_tela:
            pontos_jogador += 1
            bola = Bola()

        if (fase == 1 and pontos_jogador >= 2) or (fase == 2 and pontos_jogador >= 2) or (fase == 3 and pontos_jogador >= 7):
            if fase < 3:
                fase += 1
                pontos_jogador = 0
                pontos_ia = 0
                bola.velocidade_x += 1  
                bola.velocidade_y += 1
            else:
                rodando = False 

        tela.fill(preto)
        bola.desenhar()
        raquete_esquerda.desenhar()
        raquete_direita.desenhar()
        exibir_pontuacao(pontos_jogador, pontos_ia)

        texto_fase = fonte.render(f"Fase: {fase}", True, branco)
        tela.blit(texto_fase, (10, 10))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

def modo_multiplayer():
    bola = Bola()
    raquete_esquerda = Raquete('esquerda')
    raquete_direita = Raquete('direita')

    pontos_esquerda = 0
    pontos_direita = 0
    velocidade_incremento = 0.01

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w]:
            raquete_esquerda.mover('up')
        if teclas[pygame.K_s]:
            raquete_esquerda.mover('down')
        if teclas[pygame.K_UP]:
            raquete_direita.mover('up')
        if teclas[pygame.K_DOWN]:
            raquete_direita.mover('down')

        bola.mover()

        bola.velocidade_x += velocidade_incremento * (1 if bola.velocidade_x > 0 else -1)
        bola.velocidade_y += velocidade_incremento * (1 if bola.velocidade_y > 0 else -1)

        if (raquete_esquerda.x + raquete_esquerda.largura > bola.x and
            raquete_esquerda.y < bola.y < raquete_esquerda.y + raquete_esquerda.altura):
            bola.velocidade_x *= -1

        if (raquete_direita.x < bola.x + bola.largura and
            raquete_direita.y < bola.y < raquete_direita.y + raquete_direita.altura):
            bola.velocidade_x *= -1

        if bola.x <= 0:
            pontos_direita += 1
            bola = Bola()

        if bola.x >= largura_tela:
            pontos_esquerda += 1
            bola = Bola()

        tela.fill(preto)
        bola.desenhar()
        raquete_esquerda.desenhar()
        raquete_direita.desenhar()
        exibir_pontuacao(pontos_esquerda, pontos_direita)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

def menu():
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    modo_single_player()
                if evento.key == pygame.K_2:
                    modo_multiplayer()

        tela.fill(preto)
        texto_titulo = fonte.render("PONG", True, branco)
        texto_single = fonte.render("1 - Single Player", True, branco)
        texto_multi = fonte.render("2 - Multiplayer", True, branco)
        tela.blit(texto_titulo, (largura_tela // 2 - texto_titulo.get_width() // 2, 100))
        tela.blit(texto_single, (300, 300))
        tela.blit(texto_multi, (300, 400))

        pygame.display.flip()

menu()
pygame.quit()
