import pygame
import random
import sys
import math
import time

pygame.init()

# Música de fundo
pygame.mixer.music.set_volume(0.60)
pygame.mixer.music.load('BoxCat Games - Victory.mp3')
pygame.mixer.music.play(-1)

# Tamanho da tela (fullscreen)
info_tela = pygame.display.Info()
largura = info_tela.current_w
altura = info_tela.current_h

tela = pygame.display.set_mode((largura, altura), pygame.FULLSCREEN)
pygame.display.set_caption("Jogo Matemática")

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 0, 0)

# Fontes
fonte = pygame.font.SysFont("Arial", 30)
fonte_creditos = pygame.font.SysFont("Arial", 20)
fonte_titulo = pygame.font.SysFont("Arial", 64)

# Botões da tela inicial
botao_largura = 200
botao_altura = 50
botao_rect = pygame.Rect((largura - botao_largura) // 2, altura // 2 - 60, botao_largura, botao_altura)
botao2_rect = pygame.Rect((largura - botao_largura) // 2, altura // 2, botao_largura, botao_altura)
botao3_rect = pygame.Rect((largura - botao_largura) // 2, altura // 2 + 60, botao_largura, botao_altura)

# Botão "Sair" na tela do jogo
botao_sair_largura = 120
botao_sair_altura = 40
botao_sair_rect = pygame.Rect(largura - botao_sair_largura - 20, altura - botao_sair_altura - 20, botao_sair_largura, botao_sair_altura)

# Função para desenhar texto centralizado
def desenhar_texto(surface, texto, y, tamanho=30, cor=preto):
    fonte_local = pygame.font.SysFont("Arial", tamanho)
    render = fonte_local.render(texto, True, cor)
    ret = render.get_rect(center=(largura // 2, y))
    surface.blit(render, ret)

# Tela de apresentação
def tela_apresentacao():
    clock = pygame.time.Clock()
    alpha = 0
    fade_surface = pygame.Surface((largura, altura))
    fade_surface.fill(branco)

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    esperando = False

        tela.fill(branco)

        if alpha < 255:
            alpha += 5
            fade_surface.set_alpha(255 - alpha)

        desenhar_texto(tela, "MATHLAB", altura // 4, 64)
        desenhar_texto(tela, "Criadores:", altura // 1.6, 24)
        desenhar_texto(tela, "João Vitor Dos Santos, Marina Rodrigues, Gabriel Tunello, Victor Biazin", altura // 1.5, 20)
        desenhar_texto(tela, "Pressione ESPAÇO para continuar", altura // 1.2, 22)

        tela.blit(fade_surface, (0, 0))
        pygame.display.update()
        clock.tick(60)

# Geração de perguntas
def gerar_pergunta(nivel):
    if nivel == "iniciante":
        operador = random.choice(['+', '-'])
        a = random.randint(1, 50)
        b = random.randint(1, 50)
        if operador == '-' and b > a:
            a, b = b, a
        pergunta = f"{a} {operador} {b}"
        resposta_correta = eval(pergunta)

    elif nivel == "amador":
        operador = random.choice(['*', '/'])
        if operador == '*':
            a = random.randint(2, 12)
            b = random.randint(2, 12)
            pergunta = f"{a} x {b}"
            resposta_correta = a * b
        else:
            b = random.randint(2, 12)
            resposta_correta = random.randint(2, 12)
            a = b * resposta_correta
            pergunta = f"{a} / {b}"

    elif nivel == "avancado":
        operador = random.choice(['**', '√'])
        if operador == '**':
            a = random.randint(2, 5)
            b = random.randint(2, 3)
            pergunta = f"{a} ^ {b}"
            resposta_correta = a ** b
        else:
            resposta_correta = random.randint(2, 12)
            a = resposta_correta ** 2
            pergunta = f"√{a}"

    return pergunta, resposta_correta

# Jogo com cronômetro e finalização
def jogar_nivel(nivel):
    perguntas = [gerar_pergunta(nivel) for _ in range(15)]
    indice = 0
    entrada = ''
    acertos = 0
    relogio = pygame.time.Clock()
    rodando = True
    tempo_limite = 60  # segundos
    tempo_inicial = time.time()
    fim_jogo = False
    venceu = False
    tempo_final = 0

    while rodando:
        tela.fill(branco)
        tempo_atual = time.time()
        tempo_decorrido = tempo_atual - tempo_inicial
        tempo_restante = max(0, tempo_limite - int(tempo_decorrido))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if fim_jogo:
                    if evento.key == pygame.K_ESCAPE:
                        rodando = False
                else:
                    if evento.key == pygame.K_RETURN:
                        if entrada:
                            try:
                                if float(entrada) == float(perguntas[indice][1]):
                                    acertos += 1
                            except:
                                pass
                            indice += 1
                            entrada = ''
                    elif evento.key == pygame.K_BACKSPACE:
                        entrada = entrada[:-1]
                    elif evento.unicode.isdigit() or evento.unicode in ['-', '.']:
                        entrada += evento.unicode

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_sair_rect.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

        if not fim_jogo:
            if tempo_restante == 0 and indice < len(perguntas):
                fim_jogo = True
                venceu = False
            elif indice >= len(perguntas):
                fim_jogo = True
                venceu = True
                tempo_final = int(tempo_decorrido)

        if fim_jogo:
            if venceu:
                desenhar_texto(tela, "Parabéns! Você concluiu todas as perguntas!", altura // 3, 38)
                desenhar_texto(tela, f"Tempo total: {tempo_final} segundos", altura // 3 + 70, 34)
                desenhar_texto(tela, f"Acertos: {acertos} de 15", altura // 3 + 130, 34)
            else:
                desenhar_texto(tela, "Game Over! O tempo acabou!", altura // 3 + 50, 40)
                desenhar_texto(tela, f"Acertos: {acertos} de 15", altura // 3 + 120, 35)

            desenhar_texto(tela, "Pressione ESC para voltar ou clique em Sair", altura // 3 + 190, 25)
        else:
            desenhar_texto(tela, f"Pergunta {indice + 1}/15:", altura // 4, 40)
            desenhar_texto(tela, perguntas[indice][0] + " =", altura // 4 + 50, 50)
            desenhar_texto(tela, entrada, altura // 4 + 130, 40)

        if not fim_jogo:
            cronometro = fonte.render(f"Tempo: {tempo_restante}s", True, preto)
            tela.blit(cronometro, (largura - 200, 20))

        pygame.draw.rect(tela, preto, botao_sair_rect)
        texto_sair = fonte.render("Sair", True, branco)
        tela.blit(texto_sair, texto_sair.get_rect(center=botao_sair_rect.center))

        pygame.display.flip()
        relogio.tick(30)

# Tela inicial com botões e explicações
def tela_inicial():
    tela.fill(branco)
    desenhar_texto(tela, "Escolha seu nível de dificuldade", altura // 10, 36)
    desenhar_texto(tela, "Iniciante: Adição e Subtração", altura // 10 + 60, 28)
    desenhar_texto(tela, "Amador: Multiplicação e Divisão", altura // 10 + 100, 28)
    desenhar_texto(tela, "Avançado: Potenciação e Raiz Quadrada", altura // 10 + 140, 28)

    pygame.draw.rect(tela, preto, botao_rect)
    pygame.draw.rect(tela, preto, botao2_rect)
    pygame.draw.rect(tela, preto, botao3_rect)

    texto_surface = fonte.render("iniciante", True, branco)
    texto2_surface = fonte.render("amador", True, branco)
    texto3_surface = fonte.render("avançado", True, branco)

    tela.blit(texto_surface, texto_surface.get_rect(center=botao_rect.center))
    tela.blit(texto2_surface, texto2_surface.get_rect(center=botao2_rect.center))
    tela.blit(texto3_surface, texto3_surface.get_rect(center=botao3_rect.center))

    pygame.display.update()

# === EXECUÇÃO ===
tela_apresentacao()

rodando = True
while rodando:
    tela_inicial()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if botao_rect.collidepoint(evento.pos):
                jogar_nivel("iniciante")
            elif botao2_rect.collidepoint(evento.pos):
                jogar_nivel("amador")
            elif botao3_rect.collidepoint(evento.pos):
                jogar_nivel("avancado")

pygame.quit()
