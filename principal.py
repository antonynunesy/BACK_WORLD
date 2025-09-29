import pygame
import constantes as cons
import sprites as spr
import os
import csv


class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.tela = pygame.display.set_mode((cons.LARGURA, cons.ALTURA))
        pygame.display.set_caption(cons.TITULO_JOGO)
        self.clock = pygame.time.Clock()
        self.rodando = True
        self.fonte = pygame.font.match_font(cons.FONTE)
        self.carregar_arquivos()


    def carregar_arquivos(self):
        self.diretorio_img = os.path.join(os.getcwd(),"imagens")
        self.diretorio_aud = os.path.join(os.getcwd(), "audios")
        self.spritesheet = pygame.image.load(os.path.join(self.diretorio_img, "spritesheet.png")).convert_alpha()
        self.spritecards = pygame.image.load(os.path.join(self.diretorio_img, "card.png")).convert_alpha()
        spritesheet_bg = pygame.image.load(os.path.join(self.diretorio_img, "BackGrounds/fundo_invert.png")).convert_alpha()
        spritesheet_divisao = pygame.image.load(os.path.join(self.diretorio_img, "divisao_central.png")).convert_alpha()
        spritesheet_teleport = pygame.image.load(os.path.join(self.diretorio_img, "teleporte.png")).convert_alpha()

        self.musica_fundo = os.path.join(self.diretorio_aud, "background_sound.mp3")
        self.musica_bom = os.path.join(self.diretorio_aud, "bom.mp3")
        self.musica_over = os.path.join(self.diretorio_aud, "over_sound.mp3")

        self.jogo_start_logo = os.path.join(self.diretorio_img, "logo.png")

        self.back_ground = []
        for i in range(1, 6):
            img = pygame.image.load(os.path.join(self.diretorio_img, f"BackGrounds/{i}.png")).convert_alpha()
            self.back_ground.append(img)
        for i in range(3):
            img = spritesheet_bg.subsurface((i*960, 0), (cons.LARGURA, cons.MEIO_Y))
            self.back_ground.append(img)
        for i in range(2):
            img = spritesheet_divisao.subsurface((0, i*16), (cons.LARGURA, 16))
            self.back_ground.append(img)

        self.img_list = []
        for i in range(4):
            for j in range(5):
                img = self.spritesheet.subsurface((j*32, i*32), (32, 32))
                self.img_list.append(img)
        for i in range(5):
            img = pygame.transform.scale((self.spritesheet.subsurface((i*32, 128), (32, 128))), (64, 256))
            self.img_list.append(img)

        self.img_list.append(pygame.image.load(os.path.join(self.diretorio_img, "spritesheet.png")).convert_alpha())

        for i in range(3):
            img = spritesheet_teleport.subsurface((i*32, 0), (32, 320))
            self.img_list.append(img)
        for i in range(2):
            for j in range(8):
                img = self.spritecards.subsurface((j*24, i*24), (24, 24))
                img = pygame.transform.scale(img, (32, 32))
                self.img_list.append(img)


    def start(self):
        esperando = True
        mostrar_texto = True
        ultima_toggle = pygame.time.get_ticks()

        logo = pygame.image.load(self.jogo_start_logo).convert_alpha()
        logo = pygame.transform.scale(logo, (cons.LARGURA, cons.ALTURA))
        logo_rect = logo.get_rect(center=(cons.MEIO_X, cons.MEIO_Y))
        
        pygame.mixer.music.load(self.musica_fundo)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)        

        while esperando and self.rodando:
            self.clock.tick(cons.FPS)

            self.tela.fill(cons.PRETO)

            self.tela.blit(logo, logo_rect)

            agora = pygame.time.get_ticks()
            if agora - ultima_toggle > 500:
                mostrar_texto = not mostrar_texto
                ultima_toggle = agora
            if mostrar_texto:
                self.mostrar_texto("Pressione uma tecla para jogar", 32, cons.BRANCO, cons.MEIO_X, cons.MEIO_Y + 180)

                self.jogando = False
            self.mostrar_texto("Desenvolvido por Victor Rafael e Antony Nunes", 20, cons.CINZA, cons.MEIO_X, cons.ALTURA - 40)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    esperando = False
                    self.rodando = False
                if event.type == pygame.KEYUP:
                    esperando = False


    def pausar_jogo(self):
        pausado = True
        frame_congelado = self.tela.copy()
        mostrar_texto = True
        ultima_toggle = pygame.time.get_ticks()

        mini_logo_path = os.path.join(self.diretorio_img, "mini.png")
        mini_logo = pygame.image.load(mini_logo_path).convert_alpha()
        mini_logo = pygame.transform.scale(mini_logo, (cons.LARGURA // 5, cons.ALTURA // 8))
        mini_logo_rect = mini_logo.get_rect(center=(cons.MEIO_X, 120))

        while pausado:
            self.clock.tick(cons.FPS)

            self.tela.blit(frame_congelado, (0, 0))

            overlay = pygame.Surface((cons.LARGURA, cons.ALTURA), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.tela.blit(overlay, (0, 0))

            self.tela.blit(mini_logo, mini_logo_rect)

            agora = pygame.time.get_ticks()
            if agora - ultima_toggle > 600:
                mostrar_texto = not mostrar_texto 
                ultima_toggle = agora
            if mostrar_texto:
                self.mostrar_texto("JOGO PAUSADO", 54, cons.VERMELHO, cons.MEIO_X, cons.MEIO_Y - 40)

            self.mostrar_texto("Pressione ESC para continuar", 28, cons.BRANCO, cons.MEIO_X, cons.MEIO_Y + 30)
            self.mostrar_texto("Pressione R para reiniciar", 28, cons.BRANCO, cons.MEIO_X, cons.MEIO_Y + 70)
            self.mostrar_texto("Pressione Q para sair", 28, cons.BRANCO, cons.MEIO_X, cons.MEIO_Y + 110)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pausado = False
                    self.jogando = False
                    self.rodando = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pausado = False
                    elif event.key == pygame.K_q:
                        pausado = False
                        self.jogando = False
                        self.rodando = False
                    elif event.key == pygame.K_r:
                        pausado = False
                        self.reiniciar_jogo()


    def reiniciar_jogo(self):
        self.jogando = False
        
        self.agente.kill()
        if self.nivel != 13:
            self.teleporte.kill()

        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.musica_fundo)
        pygame.mixer.music.play(-1)
        
        self.comeca_fase()
    

    def mostrar_texto(self, texto, tamanho, cor, x, y):
        fonte = pygame.font.SysFont("comicsansms", tamanho, bold=True)
        superficie = fonte.render(texto, True, cor)
        rect = superficie.get_rect()
        rect.midtop = (x, y)
        self.tela.blit(superficie, rect)


    def esperar_jogador(self):
        esperando = True
        while esperando:
            self.clock.tick(cons.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    esperando = False
                    self.rodando = False
                if event.type == pygame.KEYUP:
                    esperando = False


    def novo_jogo(self):
        self.tela_rolar = 0
        self.back_grounds = pygame.sprite.Group()
        self.sprites_fixas = pygame.sprite.Group()
        self.limites = pygame.sprite.Group()

        self.sprites_dinamicas = pygame.sprite.Group()
        self.colisao_cenario = pygame.sprite.Group()
        self.colisao_caixas = pygame.sprite.Group()
        self.colisao_botoes = pygame.sprite.Group()
        self.cards = pygame.sprite.Group()

        sensor_esq = spr.Plataforma_arbritaria(cons.LIXO-32, -160, 32, cons.ALTURA + 2*160)
        sensor_dir = spr.Plataforma_arbritaria(cons.LARGURA-cons.LIXO, -160, 32, cons.ALTURA + 2*160)
        self.tela_desligada = spr.Mundo_desligado()
        self.divisao = spr.BackGround(0, cons.MEIO_Y-8, [self.back_ground[8+i] for i in range(2)])
        back_ground_invert = spr.BackGround(0, cons.MEIO_Y, [self.back_ground[5+i] for i in range(3)])

        self.back_grounds.add(back_ground_invert)
        self.sprites_fixas.add(self.tela_desligada, self.divisao)
        self.limites.add(sensor_esq,sensor_dir)

        self.nivel = 1
        self.comeca_fase()
        

    def comeca_fase(self):
        self.sprites_dinamicas.empty()
        self.colisao_cenario.empty()
        self.colisao_caixas.empty()
        self.colisao_botoes.empty()
        self.tela_desligada.rect.topleft = (0, cons.MEIO_Y)
        self.passada_bg = 0

        self.ler_layout()
        self.criar_mundo()

        self.rodar()
        self.game_over()


    def ler_layout(self):
        self.layout = []
        for linha in range(cons.LINHAS):
            l = [-1]*cons.COLUNAS
            self.layout.append(l)
        
        with open(os.path.join(os.getcwd(),f"niveis/niveis - fase{self.nivel}.csv"), newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")

            for x, linha in enumerate(reader):
                for y, bloco in enumerate(linha):
                    self.layout[x][y] = bloco


    def criar_mundo(self):
        for y, linha in enumerate(self.layout):
            for x, celula in enumerate(linha):
                X = x*cons.TAMANHO_BLOCO
                Y = y*cons.TAMANHO_BLOCO
                celula = str(celula)
                if celula.isdigit():
                        celula = int(celula)
                        img = self.img_list[celula]
                        img_rect = img.get_rect()

                        if celula <= 9:
                            img_rect.topleft = (X, Y)
                            bloco = spr.Plataforma(img, img_rect)
                            self.colisao_cenario.add(bloco)
                            self.sprites_dinamicas.add(bloco)

                        elif celula <= 11:
                            img_rect.topleft = (X, Y)

                            GRAVIDADE = cons.GRAVIDADE
                            if celula == 11:
                                GRAVIDADE *= -1
                            
                            caixa = spr.Caixa(img, img_rect, cons.VEL_PLAYER, GRAVIDADE)
                            self.colisao_caixas.add(caixa)
                            self.sprites_dinamicas.add(caixa)
                    
                        elif celula >= 16 and celula <= 19:
                            img_rect.topleft = (X, Y)
                            if Y > 320:
                                img = pygame.transform.flip(img, False, True)
                            placa = spr.Plataforma(img, img_rect)
                            self.sprites_dinamicas.add(placa)
                  
                        elif celula == 25:
                            self.agente = spr.Agente(X, Y, 2)
                            self.sprites_fixas.add(self.agente)
                
                        elif celula == 26:
                            self.teleporte = spr.BackGround(X, -64, [self.img_list[celula+i] for i in range(3)])
                            self.sprites_dinamicas.add(self.teleporte)
                      
                        elif celula >= 27:
                            img_rect.topleft = (X, Y)

                            if celula == 27:
                                celula = 29
                                BOM = True
                                FRASE = "VOCÊ SALVOU O MUNDO!!"
                            elif celula == 28:
                                celula = 37
                                BOM = False
                                FRASE = "VOCÊ DOMINOU O MUNDO!!"

                            card = spr.Card([self.img_list[celula+i] for i in range(8)], img_rect, BOM, FRASE)
                            self.cards.add(card)
                            self.sprites_dinamicas.add(card)


                elif celula != "-1":
                    celula = celula.split(":")
                    celula[0] = int(celula[0])
               
                    if celula[0] <= 13:
                        img_rect.topleft = (X, Y)

                        AJUSTE = 22
                        if celula[0] == 13:
                            AJUSTE = 0

                        CLICAVEL = False
                        MATA = False
                        if celula[1] == "C":
                            CLICAVEL = True
                        elif celula[1] == "D":
                            MATA = True

                        botao = spr.Botao([self.img_list[celula[0]], self.img_list[celula[0]+2]], img_rect, CLICAVEL, AJUSTE, MATA)
                        self.colisao_botoes.add(botao)
                        self.sprites_dinamicas.add(botao)
                 
                    elif celula[0] == 20:
                        img_rect.topleft = (X, Y)
                        celula[2] = int(celula[2])
                        
                        if celula[1] == "P":
                            PERMANENTE = True
                        elif celula[1] == "N":
                            PERMANENTE = False
                        
                        self.porta = spr.Porta([self.img_list[celula[0]+i] for i in range(5)], img_rect, PERMANENTE, celula[2])
                        self.sprites_dinamicas.add(self.porta)


    def rodar(self):
        self.jogando = True
        while self.jogando:
            self.clock.tick(cons.FPS)
            self.eventos()
            self.atualizar()
            self.desenhar_sprites()


    def eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.jogando:
                    self.jogando = False
                self.rodando = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.agente.pular(self.colisao_botoes, self.porta)
                if event.key == pygame.K_ESCAPE:
                    self.pausar_jogo()

        
    def atualizar(self):
        self.back_grounds.update()
        self.sprites_fixas.update()
        self.sprites_dinamicas.update()
        self.colisao_cenario.update()
        self.colisao_caixas.update()
        self.colisao_botoes.update()
        self.divisao.update()
        if self.nivel != 13:
            self.teleporte.update()

        self.agente.movimento(self.colisao_cenario, self.colisao_caixas, self.colisao_botoes, self.porta)
        self.tela_rolar = self.agente.borda(self.limites)

        if self.agente.troca_mundo(self.colisao_cenario):
            self.tela_desligada.rect.y = (self.tela_desligada.rect.y + cons.MEIO_Y) % cons.ALTURA

        for bloco in self.sprites_dinamicas:
            bloco.rect.x += self.tela_rolar

        for caixa in self.colisao_caixas:
            caixas_temp = self.colisao_caixas.copy()
            caixas_temp.remove(caixa)
            caixa.movimento(self.colisao_cenario, caixas_temp, [self.agente], self.colisao_botoes, self.porta)
            if caixa.morre([self.divisao]):
                caixa.kill()

        for botao in self.colisao_botoes:
            ativou = botao.apertou(self.colisao_caixas, self.agente)
            if ativou == "mata":
                self.jogando = False
            else:
                self.porta.abrir(ativou)

        if self.agente.morre([self.divisao]):
            self.jogando = False

        if self.nivel != 13 and self.agente.passa_fase([self.teleporte]):
            self.nivel += 1
            self.agente.kill()
            self.teleporte.kill()

            self.comeca_fase()

        if self.nivel == 13:
            if self.agente.ganhou(self.cards):
                self.vitoria(self.agente.ganhou(self.cards)[1])


    def desenhar_sprites(self):
        self.tela.fill(cons.BRANCO)    

        for x in range(2):
            for bg in range(5):
                self.tela.blit(self.back_ground[bg], (x*576 - x, -4))
 
        self.back_grounds.draw(self.tela)
        self.sprites_dinamicas.draw(self.tela)
        self.sprites_fixas.draw(self.tela)

        pygame.display.flip()


    def game_over(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.musica_over)
        pygame.mixer.music.play(0)
        esperando = True
        mostrar_texto = True
        game_over_logo = os.path.join(self.diretorio_img, "gameover.png")
        gameover_logo = pygame.image.load(game_over_logo).convert_alpha()
        ultima_toggle = pygame.time.get_ticks()

        largura = int(cons.LARGURA * 0.66)
        escala = largura / gameover_logo.get_width()
        novo_tamanho = (int(gameover_logo.get_width() * escala), int(gameover_logo.get_height() * escala))
        gameover_logo = pygame.transform.scale(gameover_logo, novo_tamanho)
        logo_rect = gameover_logo.get_rect(center=(cons.MEIO_X, cons.MEIO_Y - 50))

        while esperando and self.rodando:
            self.clock.tick(cons.FPS)

            self.tela.fill(cons.PRETO)
            self.tela.blit(gameover_logo, logo_rect)

            agora = pygame.time.get_ticks()
            if agora - ultima_toggle > 600:
                mostrar_texto = not mostrar_texto
                ultima_toggle = agora

            if mostrar_texto:
                self.mostrar_texto("Pressione R para Reiniciar", 32, cons.BRANCO, cons.MEIO_X, cons.MEIO_Y + 150)
                self.mostrar_texto("Pressione Q para Sair", 32, cons.BRANCO, cons.MEIO_X, cons.MEIO_Y + 200)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    esperando = False
                    self.rodando = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        esperando = False
                        self.reiniciar_jogo()
                    elif event.key == pygame.K_q:
                        esperando = False
                        self.jogando = False
                        self.rodando = False


    def vitoria(self, frase):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.musica_bom)
        pygame.mixer.music.play(-1)


        esperando = True
        mostrar_texto = True
        ultima_toggle = pygame.time.get_ticks()

        logo_path = os.path.join(self.diretorio_img, "mini.png")
        victory_logo = pygame.image.load(logo_path).convert_alpha()

        max_width = int(cons.LARGURA * 0.6)
        escala = max_width / victory_logo.get_width()
        new_size = (int(victory_logo.get_width() * escala),
                    int(victory_logo.get_height() * escala))
        victory_logo = pygame.transform.scale(victory_logo, new_size)
        logo_rect = victory_logo.get_rect(center=(cons.MEIO_X, cons.MEIO_Y - 100))

        while esperando and self.rodando:
            self.clock.tick(cons.FPS)

            self.tela.fill(cons.PRETO)

            self.tela.blit(victory_logo, logo_rect)

            agora = pygame.time.get_ticks()
            if agora - ultima_toggle > 600:
                mostrar_texto = not mostrar_texto
                ultima_toggle = agora
            if mostrar_texto:
                self.mostrar_texto("PARABÉNS!", 48, cons.AMARELO, cons.MEIO_X, cons.MEIO_Y + 70)
                self.mostrar_texto(frase, 28, cons.AMARELO, cons.MEIO_X, cons.MEIO_Y + 130)

            self.mostrar_texto("Obrigado por jogar BACK WORLD", 28, cons.BRANCO, cons.MEIO_X, cons.ALTURA - 120)
            self.mostrar_texto("Pressione Q para sair", 28, cons.CINZA, cons.MEIO_X, cons.ALTURA - 60)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.rodando = False
                    esperando = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        esperando = False
                        self.jogando = False
                        self.rodando = False                        
                        

g = Game()
g.start()

while g.rodando:
    g.novo_jogo()
