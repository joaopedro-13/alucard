import pygame
import random
import sys
import re

# Initialize pygame
pygame.init()
pygame.mixer.init()


# Sound functions
def tocar_musica(caminho, volume=0.5):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(caminho)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)


def carregar_sons():
    sons = {
        'moeda': pygame.mixer.Sound('sons/moedasom.mp3'),
        'dano_cacador': pygame.mixer.Sound('sons/danocacador.mp3'),
        'dano_boss': pygame.mixer.Sound('sons/danoboss.mp3'),
        'level_up': pygame.mixer.Sound('sons/levelup.mp3'),
        'congelar': pygame.mixer.Sound('sons/congelar.mp3'),
        'vida': pygame.mixer.Sound('sons/vida.mp3'),
        'boss_secreto': pygame.mixer.Sound('sons/boss_secreto.mp3')
    }
    for som in sons.values():
        som.set_volume(0.5)
    return sons


# Screen setup
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("King Alucard")
clock = pygame.time.Clock()

# Fonts
FONT = pygame.font.SysFont('arial', 50)
FONT_LOBBY = pygame.font.SysFont('arial', 80)
FONT_PEQUENA = pygame.font.SysFont('arial', 36)


# Load images
def carregar_imagem(caminho, escala=None):
    try:
        img = pygame.image.load(caminho).convert_alpha()
        if escala:
            img = pygame.transform.scale(img, escala)
        return img
    except:
        print(f"Erro ao carregar imagem: {caminho}")
        return pygame.Surface((100, 100))  # Return blank surface if image fails to load


# Load all assets
background_img = carregar_imagem('imagens/castelo1920.png', (WIDTH, HEIGHT))
lobby_background = carregar_imagem('imagens/lobby.jpg', (WIDTH, HEIGHT))
cenario_boss = carregar_imagem('imagens/cenarioboss.pngd', (WIDTH, HEIGHT))
barco_sprite_img = carregar_imagem('imagens/caçador1.png', (120, 120))
barco_sprite_img_flipped = pygame.transform.flip(barco_sprite_img, True, False)
img_ouro = carregar_imagem('imagens/vampiraoo.png', (120, 120))
img_prata = carregar_imagem('imagens/esqueleto.png', (80, 80))
img_bronze = carregar_imagem('imagens/zumbib.png', (80, 80))
img_bomba = carregar_imagem('imagens/estaca_amaldiçoada.png', (80, 80))
img_boss = carregar_imagem('imagens/boss.png', (250, 250))
img_vida = carregar_imagem('imagens/vidablack.png', (40, 40))
img_congelamento = carregar_imagem('imagens/aguabenta.png', (80, 80))
img_biblia = carregar_imagem('imagens/biblia.png', (100, 100))
img_coracao = carregar_imagem('imagens/coracao.png', (40, 40))
img_vampirinho = carregar_imagem('imagens/vampirinho.png', (40, 40))
img_estaca = carregar_imagem('imagens/estaca.png', (40, 40))

# Load sounds
sons = carregar_sons()

# Game constants
plataforma_rect = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)
VALOR_MOEDAS = {'ouro': 10, 'prata': 5, 'bronze': 1}


class Loja:
    def __init__(self):
        self.melhorias = {
            "vida": {"custo": 50, "nivel": 0, "max": 3},
            "velocidade": {"custo": 30, "nivel": 0, "max": 5},
            "carga": {"custo": 40, "nivel": 0, "max": 3}
        }
        self.ativo = False

    def mostrar(self, pontos):
        self.ativo = True
        while self.ativo:
            screen.fill((0, 0, 0))
            titulo = FONT.render("LOJA - Pontos: " + str(pontos), True, (255, 0, 0))
            screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 100))

            y = 200
            for nome, dados in self.melhorias.items():
                texto = FONT.render(
                    f"{nome.capitalize()} (Nv. {dados['nivel']}): Custo {dados['custo']}",
                    True, (255, 255, 255) if dados['nivel'] < dados['max'] else (128, 128, 128)
                )
                screen.blit(texto, (WIDTH // 2 - texto.get_width() // 2, y))
                y += 60

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 and self.melhorias["vida"]["nivel"] < self.melhorias["vida"][
                        "max"] and pontos >= self.melhorias["vida"]["custo"]:
                        pontos -= self.melhorias["vida"]["custo"]
                        self.melhorias["vida"]["nivel"] += 1
                        sons['level_up'].play()
                    elif event.key == pygame.K_2 and self.melhorias["velocidade"]["nivel"] < \
                            self.melhorias["velocidade"]["max"] and pontos >= self.melhorias["velocidade"]["custo"]:
                        pontos -= self.melhorias["velocidade"]["custo"]
                        self.melhorias["velocidade"]["nivel"] += 1
                        sons['level_up'].play()
                    elif event.key == pygame.K_3 and self.melhorias["carga"]["nivel"] < self.melhorias["carga"][
                        "max"] and pontos >= self.melhorias["carga"]["custo"]:
                        pontos -= self.melhorias["carga"]["custo"]
                        self.melhorias["carga"]["nivel"] += 1
                        sons['level_up'].play()
                    elif event.key == pygame.K_RETURN:
                        self.ativo = False
        return pontos


def menu_principal():
    tocar_musica('sons/musica_lobby.mp3')
    selecionado = "JOGAR"
    avaliacao = 0
    dificuldade = 1

    while True:
        screen.blit(lobby_background, (0, 0))

        titulo = FONT_LOBBY.render("King Alucard", True, (255, 0, 0))
        jogar = FONT.render("-> JOGAR" if selecionado == "JOGAR" else "   JOGAR", True, (128, 128, 128))
        som = FONT.render("-> SOM " if selecionado == "SOM" else "   SOM ", True, (128, 128, 128))
        avaliar = FONT.render(
            f"-> AVALIAR [{avaliacao}/5]" if selecionado == "AVALIAR" else f"   AVALIAR [{avaliacao}/5]", True,
            (128, 128, 128))
        dificuldade_text = FONT.render(f"DIFICULDADE: {dificuldade} (← →)", True, (255, 255, 255))

        screen.blit(titulo, (100, 100))
        screen.blit(jogar, (100, 250))
        screen.blit(som, (100, 350))
        screen.blit(avaliar, (100, 450))
        screen.blit(dificuldade_text, (100, 550))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selecionado == "AVALIAR":
                        selecionado = "SOM"
                    elif selecionado == "SOM":
                        selecionado = "JOGAR"
                elif event.key == pygame.K_DOWN:
                    if selecionado == "JOGAR":
                        selecionado = "SOM"
                    elif selecionado == "SOM":
                        selecionado = "AVALIAR"
                elif event.key == pygame.K_LEFT:
                    if selecionado == "AVALIAR" and avaliacao > 0:
                        avaliacao -= 1
                    elif selecionado != "AVALIAR" and dificuldade > 1:
                        dificuldade -= 1
                elif event.key == pygame.K_RIGHT:
                    if selecionado == "AVALIAR" and avaliacao < 5:
                        avaliacao += 1
                    elif selecionado != "AVALIAR" and dificuldade < 5:
                        dificuldade += 1
                elif event.key == pygame.K_RETURN:
                    if selecionado == "JOGAR":
                        return dificuldade
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def obter_nome():
    nome = ""
    entrada_ativa = True
    while entrada_ativa:
        screen.fill((0, 0, 0))
        texto = FONT_PEQUENA.render("Digite seu nome e pressione ENTER:", True, (255, 0, 0))
        nome_surface = FONT_PEQUENA.render(nome, True, (255, 0, 0))
        screen.blit(texto, (WIDTH // 2 - texto.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(nome_surface, (WIDTH // 2 - nome_surface.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and nome.strip() != "":
                    entrada_ativa = False
                elif event.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    if re.match(r"[a-zA-Z0-9 _\\-]", event.unicode):
                        nome += event.unicode
    return nome.strip()


def configurar_dificuldade(nivel, dificuldade):
    qtd = min(10 + nivel * 2 + dificuldade, 30)
    v_min = 3 + nivel + dificuldade
    v_max = 5 + nivel * 1.5 + dificuldade
    return qtd, v_min, v_max


def checar_easter_egg(pontos, barco):
    if pontos == 0 and barco.vidas <= 0:
        sons['boss_secreto'].play()
        return True
    return False


class Barco(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = barco_sprite_img
        self.original_image = barco_sprite_img
        self.flipped_image = barco_sprite_img_flipped
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 50))
        self.speed = 8
        self.carga = 0
        self.max_carga = 100
        self.vidas = 3
        self.bombas_coletadas = 0
        self.facing_right = True
        self.dano_temporario = 0

    def update(self, keys_pressed):
        if self.dano_temporario > 0:
            self.dano_temporario -= 1
            if self.dano_temporario % 5 == 0:
                self.image.fill((255, 0, 0, 100), special_flags=pygame.BLEND_ADD)

        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if self.facing_right:
                self.image = self.flipped_image
                self.facing_right = False
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if not self.facing_right:
                self.image = self.original_image
                self.facing_right = True

        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WIDTH)

    def levar_dano(self):
        self.dano_temporario = 30
        self.vidas -= 1
        sons['dano_cacador'].play()

    def voltar_ao_porto(self):
        self.rect.midbottom = (WIDTH // 2, HEIGHT - 50)
        self.carga = 0


class Objeto(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo, v_min, v_max):
        super().__init__()
        imagens = {'ouro': img_ouro, 'prata': img_prata, 'bronze': img_bronze, 'bomba': img_bomba}
        self.tipo = tipo
        self.image = imagens[tipo]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.v_min = v_min
        self.v_max = v_max
        self.speed = random.uniform(v_min, v_max)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -10)
            self.speed = random.uniform(self.v_min, self.v_max)


class Vampirinho(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = img_vampirinho
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 6

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class Estaca(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = img_estaca
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -12

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


class Boss(pygame.sprite.Sprite):
    def __init__(self, dificuldade):
        super().__init__()
        self.image = img_boss
        self.rect = self.image.get_rect(midtop=(WIDTH // 2, 20))
        self.speed = 6
        self.direcao = 1
        self.vida = 10 + dificuldade * 2
        self.estado = "normal"
        self.tempo_ataque_especial = 0

    def update(self):
        if self.estado == "furioso" and pygame.time.get_ticks() - self.tempo_ataque_especial > 5000:
            self.estado = "normal"
            self.speed = 6

        if self.estado == "normal":
            self.rect.x += self.speed * self.direcao
            if self.rect.right >= WIDTH or self.rect.left <= 0:
                self.direcao *= -1
            if self.vida <= 5:
                self.estado = "furioso"
                self.speed = 10
                self.tempo_ataque_especial = pygame.time.get_ticks()


class Coracao(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = img_coracao
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 4

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


def iniciar_musica_boss():
    tocar_musica('sons/musica_boss.mp3')


def iniciar_musica_normal():
    tocar_musica('sons/musica_fase.mp3')


def jogo_principal():
    dificuldade = menu_principal()
    nome_jogador = obter_nome()
    loja = Loja()

    nivel = 1
    pontos = 0
    barco = Barco()
    objetos = pygame.sprite.Group()
    todas_sprites = pygame.sprite.Group()
    vampirinhos = pygame.sprite.Group()
    estacas = pygame.sprite.Group()
    coracoes = pygame.sprite.Group()

    boss = None
    modo_boss = False
    easter_egg_ativado = False
    estacas_disponiveis = 10
    tempo_ultima_estaca = pygame.time.get_ticks()
    tempo_spawn_vampirinho = pygame.time.get_ticks()
    biblia_ativa = False
    congelado = False
    tempo_congelamento = 0

    qtd_objetos, v_min, v_max = configurar_dificuldade(nivel, dificuldade)

    def criar_objetos():
        objetos.empty()
        for _ in range(qtd_objetos):
            tipo = random.choices(['ouro', 'prata', 'bronze', 'bomba'], weights=[3, 2, 1, 3])[0]
            x = random.randint(0, WIDTH - 80)
            y = random.randint(-100, -10)
            objetos.add(Objeto(x, y, tipo, v_min, v_max))

    criar_objetos()
    iniciar_musica_normal()

    running = True
    while running:
        clock.tick(60)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    if modo_boss:
                        agora = pygame.time.get_ticks()
                        if estacas_disponiveis > 0:
                            estaca = Estaca(barco.rect.centerx, barco.rect.top)
                            estacas.add(estaca)
                            estacas_disponiveis -= 1
                            tempo_ultima_estaca = agora
                    elif not congelado:
                        congelado = True
                        tempo_congelamento = pygame.time.get_ticks()
                        sons['congelar'].play()
                        for obj in objetos:
                            obj.speed /= 2

        if pygame.time.get_ticks() - tempo_ultima_estaca > 10000:
            estacas_disponiveis = 10

        if congelado and pygame.time.get_ticks() - tempo_congelamento > 5000:
            congelado = False
            for obj in objetos:
                obj.speed *= 2

        screen.fill((0, 0, 0))

        if modo_boss:
            screen.blit(cenario_boss, (0, 0))
            pygame.draw.rect(screen, (60, 60, 60), plataforma_rect)
            barco.update(keys)
            boss.update()
            vampirinhos.update()
            estacas.update()
            coracoes.update()

            screen.blit(barco.image, barco.rect)
            screen.blit(boss.image, boss.rect)
            vampirinhos.draw(screen)
            estacas.draw(screen)
            coracoes.draw(screen)

            for estaca in pygame.sprite.spritecollide(boss, estacas, True):
                boss.vida -= 1
                sons['dano_boss'].play()

            for vamp in pygame.sprite.spritecollide(barco, vampirinhos, True):
                barco.levar_dano()
                if barco.vidas <= 0:
                    running = False

            if pygame.time.get_ticks() - tempo_spawn_vampirinho > 1200:
                vampirinho = Vampirinho(boss.rect.centerx, boss.rect.bottom)
                vampirinhos.add(vampirinho)
                tempo_spawn_vampirinho = pygame.time.get_ticks()

            screen.blit(FONT_PEQUENA.render(f'Estacas: {estacas_disponiveis}', True, (255, 255, 255)), (10, 10))
            screen.blit(FONT_PEQUENA.render(f'Vida do Boss: {boss.vida}', True, (255, 0, 0)), (10, 50))

            for i in range(barco.vidas):
                screen.blit(img_vida, (WIDTH - (i + 1) * 50, 10))
            texto_nome = FONT_PEQUENA.render(f"{nome_jogador}", True, (255, 255, 255))
            screen.blit(texto_nome, (WIDTH - texto_nome.get_width() - 20, 60))

            if boss.vida <= 0:
                modo_boss = False
                nivel += 1
                sons['level_up'].play()
                qtd_objetos, v_min, v_max = configurar_dificuldade(nivel, dificuldade)
                criar_objetos()
                barco.voltar_ao_porto()
                pontos = loja.mostrar(pontos)
                iniciar_musica_normal()
        else:
            barco.update(keys)
            objetos.update()
            coracoes.update()
            screen.blit(background_img, (0, 0))
            pygame.draw.rect(screen, (60, 60, 60), plataforma_rect)
            objetos.draw(screen)
            coracoes.draw(screen)
            screen.blit(barco.image, barco.rect)

            screen.blit(FONT_PEQUENA.render(f"Pontos: {pontos}", True, (255, 255, 255)), (10, 80))
            screen.blit(FONT_PEQUENA.render(f'Moedas: {barco.carga}/{barco.max_carga}', True, (255, 255, 255)),
                        (10, 10))
            screen.blit(FONT_PEQUENA.render(f'Nível: {nivel}', True, (255, 255, 255)), (10, 50))

            for i in range(barco.vidas):
                screen.blit(img_vida, (WIDTH - (i + 1) * 50, 10))
            texto_nome = FONT_PEQUENA.render(f"{nome_jogador}", True, (255, 255, 255))
            screen.blit(texto_nome, (WIDTH - texto_nome.get_width() - 20, 60))

            if congelado:
                screen.blit(img_congelamento, (WIDTH - 80, HEIGHT - 80))
            if pontos >= 150:
                biblia_ativa = True
                screen.blit(img_biblia, (WIDTH - 190, HEIGHT - 100))

            colisoes = pygame.sprite.spritecollide(barco, objetos, True)
            for obj in colisoes:
                if obj.tipo == 'bomba':
                    barco.levar_dano()
                    if barco.vidas <= 0:
                        running = False
                else:
                    ganho = VALOR_MOEDAS[obj.tipo]
                    if biblia_ativa:
                        ganho *= 2
                    barco.carga += ganho
                    pontos += ganho
                    sons['moeda'].play()

            for coracao in pygame.sprite.spritecollide(barco, coracoes, True):
                barco.vidas = min(barco.vidas + 1, 5)
                sons['vida'].play()

            if random.random() < 0.002:
                coracao = Coracao(random.randint(0, WIDTH), -40)
                coracoes.add(coracao)

            while len(objetos) < qtd_objetos:
                tipo = random.choices(['ouro', 'prata', 'bronze', 'bomba'], weights=[3, 2, 1, 3])[0]
                x = random.randint(0, WIDTH - 80)
                y = random.randint(-100, -10)
                objetos.add(Objeto(x, y, tipo, v_min, v_max))

            if barco.carga >= barco.max_carga:
                if nivel % 3 == 0:
                    modo_boss = True
                    boss = Boss(dificuldade)
                    vampirinhos.empty()
                    estacas.empty()
                    estacas_disponiveis = 10
                    iniciar_musica_boss()
                else:
                    nivel += 1
                    sons['level_up'].play()
                    qtd_objetos, v_min, v_max = configurar_dificuldade(nivel, dificuldade)
                    criar_objetos()
                    pontos = loja.mostrar(pontos)
                barco.voltar_ao_porto()

        if not easter_egg_ativado and barco.vidas <= 0 and pontos == 0:
            if checar_easter_egg(pontos, barco):
                boss = Boss(10)  # Boss ultra-difícil
                modo_boss = True
                easter_egg_ativado = True
                screen.blit(cenario_boss, (0, 0))

        pygame.display.flip()

    # Tela de game over
    pygame.mixer.music.stop()
    screen.fill((0, 0, 0))

    if easter_egg_ativado:
        texto1 = FONT.render("VOCÊ ATIVOU O BOSS SECRETO!", True, (255, 0, 0))
    elif barco.vidas <= 0:
        texto1 = FONT.render("VOCÊ PERECEU!", True, (255, 0, 0))
    else:
        texto1 = FONT.render(f"Fim de jogo, {nome_jogador}!", True, (255, 0, 0))

    texto2 = FONT.render(f"Pontuação final: {pontos}", True, (255, 0, 0))
    screen.blit(texto1, (WIDTH // 2 - texto1.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(texto2, (WIDTH // 2 - texto2.get_width() // 2, HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.wait(5000)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    jogo_principal()