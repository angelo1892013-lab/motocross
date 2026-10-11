import pygame
import random
import sys

pygame.init()

# Janela do jogo
LARGURA = 900
ALTURA = 500
ecra = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Motocross Game")

relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 28)

# Cores
VERDE = (50, 150, 50)
CASTANHO = (130, 80, 40)
PRETO = (20, 20, 20)
BRANCO = (255, 255, 255)
VERMELHO = (220, 30, 30)

# Mota
mota_x = 120
mota_y = 350
velocidade_y = 0
gravidade = 0.7
saltou = False

# Obstáculos
obstaculos = []
pontuacao = 0
velocidade_jogo = 6
chao = 400
game_over = False

def desenhar_mota(x, y):
    pygame.draw.circle(ecra, PRETO, (x, y + 25), 15)
    pygame.draw.circle(ecra, PRETO, (x + 55, y + 25), 15)
    pygame.draw.line(ecra, VERMELHO, (x, y + 25), (x + 25, y), 6)
    pygame.draw.line(ecra, VERMELHO, (x + 25, y), (x + 55, y + 25), 6)
    pygame.draw.line(ecra, PRETO, (x + 25, y), (x + 40, y - 12), 5)
    pygame.draw.circle(ecra, VERMELHO, (x + 28, y - 15), 12)

def criar_obstaculo():
    altura = random.randint(25, 55)
    obstaculos.append(
        pygame.Rect(LARGURA, chao - altura, 30, altura)
    )

temporizador = 0
a_correr = True

while a_correr:
    relogio.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            a_correr = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and not saltou and not game_over:
                velocidade_y = -13
                saltou = True

            if evento.key == pygame.K_r and game_over:
                mota_y = 350
                velocidade_y = 0
                obstaculos.clear()
                pontuacao = 0
                velocidade_jogo = 6
                game_over = False
                temporizador = 0

    teclas = pygame.key.get_pressed()

    if not game_over:
        if teclas[pygame.K_RIGHT]:
            velocidade_jogo = min(12, velocidade_jogo + 0.05)

        if teclas[pygame.K_LEFT]:
            velocidade_jogo = max(3, velocidade_jogo - 0.1)

        # Física do salto
        velocidade_y += gravidade
        mota_y += velocidade_y

        if mota_y >= 350:
            mota_y = 350
            velocidade_y = 0
            saltou = False

        # Criar obstáculos
        temporizador += 1
        if temporizador > random.randint(55, 95):
            criar_obstaculo()
            temporizador = 0

        # Mover obstáculos
        for obstaculo in obstaculos:
            obstaculo.x -= int(velocidade_jogo)

        obstaculos = [
            o for o in obstaculos if o.right > 0
        ]

        # Colisões
        caixa_mota = pygame.Rect(mota_x, mota_y - 20, 65, 55)

        for obstaculo in obstaculos:
            if caixa_mota.colliderect(obstaculo):
                game_over = True

        pontuacao += 1

    # Desenhar cenário
    ecra.fill((135, 206, 235))
    pygame.draw.circle(ecra, (255, 220, 50), (750, 75), 35)
    pygame.draw.rect(ecra, VERDE, (0, chao, LARGURA, 100))
    pygame.draw.line(ecra, CASTANHO, (0, chao), (LARGURA, chao), 5)

    # Desenhar mota e obstáculos
    desenhar_mota(mota_x, mota_y)

    for obstaculo in obstaculos:
        pygame.draw.rect(ecra, CASTANHO, obstaculo)

    texto = fonte.render(
        f"Pontuacao: {pontuacao // 10}", True, BRANCO
    )
    ecra.blit(texto, (20, 20))

    if game_over:
        mensagem = fonte.render(
            "FIM DO JOGO! Pressiona R para reiniciar",
            True, VERMELHO
        )
        ecra.blit(mensagem, (180, 220))

    pygame.display.update()

pygame.quit()
sys.exit()
