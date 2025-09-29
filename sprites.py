import pygame
import os
import constantes as cons

diretorio_img = os.path.join(os.getcwd(),"imagens")

class Agente(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        super().__init__()
        self.vel = cons.VEL_PLAYER
        self.gravidade = cons.GRAVIDADE
        self.forca_pulo = cons.FORCA_PULO
        self.dx, self.dy = 0, 0
        self.direcao = 1
        self.virar = False
        self.lado = 1
        self.mundo = False
        self.trocando = False

        spritesheet_agente = pygame.image.load(os.path.join(diretorio_img, "sptitesheet_player.png")).convert_alpha()

        self.img = []
        for i in range(6):
            for j in range(9):
                img = spritesheet_agente.subsurface((j*24+2, i*48+10), (20, 30))
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                self.img.append(img)

        self.index = 0
        self.image = self.img[self.index]    
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x,y)


    def update(self):
        if self.mundo:
            self.glith = 27
        else:
            self.glith = 0

        if not self.trocando:    
            if self.dx == 0 and self.dy == 0:
                if self.index < self.glith or self.index > 5+self.glith:
                    self.index = 0+self.glith
                self.index += 0.25

            elif self.dx != 0 and self.dy == 0:
                if self.index < 6+self.glith:
                    self.index = 6+self.glith
                elif self.index > 15+self.glith:
                    self.index = 6+self.glith
                self.index += 0.4 * (self.vel/cons.VEL_PLAYER)

            else:
                if self.dy < 0:
                    self.index = 16+self.glith
                elif self.dy > 0:
                    self.index = 17+self.glith

        else:
            if self.index < 18+self.glith:
                self.index = 18+self.glith
            elif self.index > 24+self.glith:
                self.index = 24+self.glith

            self.index += 0.4

        self.image = self.img[int(self.index)]
        self.image = pygame.transform.flip(self.image, self.virar, self.mundo)


    def movimento(self, objetos, caixas, botoes, porta):
        self.tecla = pygame.key.get_pressed()
        self.dx = 0

        if not self.trocando:
            if self.tecla[pygame.K_a]:
                self.dx = -self.vel
                self.virar = True
                self.direcao = -1

            if self.tecla[pygame.K_d]:
                self.dx = self.vel
                self.virar = False
                self.direcao = 1

        self.colisao_geral = pygame.sprite.Group(objetos, caixas, porta)

        self.rect.x += self.dx
        self.colisao_x()

        self.dy += self.gravidade
        self.rect.y += self.dy
        self.colisao_y(botoes)


    def colisao_x(self):
        self.colisao = pygame.sprite.spritecollide(self, self.colisao_geral, False)

        for bloco in self.colisao:
            if isinstance(bloco, Porta) and bloco.aberta:
                continue

            if self.dx >= 0:
                self.rect.right = bloco.rect.left

            elif self.dx < 0:
                self.rect.left = bloco.rect.right


    def colisao_y(self, botoes):
        self.colisao = pygame.sprite.spritecollide(self, self.colisao_geral, False)
        self.apertando = [b for b in botoes if self.rect.colliderect(b.hitbox)]

        for bloco in self.colisao:
            if isinstance(bloco, Porta) and bloco.aberta:
                continue

            if self.dy > 0:
                self.rect.bottom = bloco.rect.top
                self.dy = 0
            elif self.dy < 0:
                self.rect.top = bloco.rect.bottom
                self.dy = 0

        for botao in self.apertando:
            if botao:
                if self.rect.y < 320:
                    self.rect.bottom = botao.hitbox.top
                    self.dy = 0
                elif self.rect.y > 320:
                    self.rect.top = botao.hitbox.bottom
                    self.dy = 0


    def pular(self, botoes, porta):
        self.rect.y += self.lado
        colisao = self.colisao_geral.copy()
        colisao.remove(porta)
        self.colisao = pygame.sprite.spritecollide(self, colisao, False)
        self.apertando = [b for b in botoes if self.rect.colliderect(b.hitbox)]
        self.rect.y -= self.lado
        
        if (self.colisao or self.apertando) and not self.trocando:
            self.dy = self.forca_pulo


    def borda(self, paredes):
        self.rolar = pygame.sprite.spritecollide(self, paredes, False)
        if self.rolar:
            self.rect.x -= self.dx
            return -self.dx
        return 0


    def troca_mundo(self, objetos):
        self.rect.y += self.lado
        self.colisao = pygame.sprite.spritecollide(self, objetos, False)
        self.rect.y -= self.lado        

        if self.tecla[pygame.K_SPACE] and self.colisao:
            self.trocando = True
        
        if self.trocando == True:
            if int(self.index) >= 22 + self.glith:
                self.lado *= -1
                self.mundo = not self.mundo
                self.rect.bottom = cons.ALTURA - self.rect.top
                self.gravidade *= -1
                self.forca_pulo *= -1
                self.trocando = False
                return True
        return False
    

    def morre(self, perigo):
        bateu = pygame.sprite.spritecollide(self, perigo, False)
        return bateu 


    def passa_fase(self, teleporte):
        passou = pygame.sprite.spritecollide(self, teleporte, False)
        return passou
    

    def ganhou(self, cards):
        ganhou = pygame.sprite.spritecollide(self, cards, False)

        for card in ganhou:
            if card:
                return [card, card.frase]


class Plataforma_arbritaria(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura):
        super().__init__()
        self.image = pygame.Surface((largura, altura))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()   
        self.rect.topleft = (x, y)


class Plataforma(pygame.sprite.Sprite):
    def __init__(self, image, coord):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()   
        self.rect.topleft = (coord[0], coord[1])


class BackGround(pygame.sprite.Sprite):
    def __init__(self, x, y, imgs):
        super().__init__()
        self.bg = imgs
        self.index = 0
        self.image = self.bg[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


    def update(self):
        if self.index > len(self.bg)-1:
            self.index = 0
        self.index += 0.25
        self.image = self.bg[int(self.index)]


class Mundo_desligado(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((cons.LARGURA, cons.ALTURA//2))
        self.image.fill(cons.PRETO)
        self.image.set_alpha(100)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, cons.MEIO_Y)


class Caixa(pygame.sprite.Sprite):
    def __init__(self, img, coord, vel_player, gravidade):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = (coord[0], coord[1])
        self.vel = vel_player
        self.dx, self.dy = 0, 0
        self.gravidade = gravidade


    def movimento(self, objetos, caixas, agente, botoes, porta):
        self.tecla = pygame.key.get_pressed()
        self.dx = 0
        
        self.rect.x += 1
        self.empurrado = pygame.sprite.spritecollide(self, agente, False)
        self.rect.x -= 1

        if self.tecla[pygame.K_a] and self.empurrado:
            self.dx = -self.vel

        self.rect.x -= 1
        self.empurrado = pygame.sprite.spritecollide(self, agente, False)
        self.rect.x += 1

        if self.tecla[pygame.K_d] and self.empurrado:
            self.dx = self.vel

        self.colisao_geral = pygame.sprite.Group(objetos, caixas, agente, porta)

        self.rect.x += self.dx
        self.colisao_x()

        self.dy += self.gravidade
        self.rect.y += self.dy
        self.colisao_y(botoes)


    def colisao_x(self):
        self.colisao = pygame.sprite.spritecollide(self, self.colisao_geral, False)

        for bloco in self.colisao:
            if isinstance(bloco, Porta) and bloco.aberta:
                continue

            if self.dx >= 0:
                self.rect.right = bloco.rect.left

            elif self.dx < 0:
                self.rect.left = bloco.rect.right


    def colisao_y(self, botoes):
        self.colisao = pygame.sprite.spritecollide(self, self.colisao_geral, False)
        self.apertando = [b for b in botoes if self.rect.colliderect(b.hitbox)]

        for bloco in self.colisao:
            if isinstance(bloco, Porta) and bloco.aberta:
                continue

            if self.dy > 0:
                self.rect.bottom = bloco.rect.top
                self.dy = 0
            elif self.dy < 0:
                self.rect.top = bloco.rect.bottom
                self.dy = 0

        for botao in self.apertando:
            if botao:
                if self.rect.y < 320:
                    self.rect.bottom = botao.hitbox.top
                    self.dy = 0
                elif self.rect.y > 320:
                    self.rect.top = botao.hitbox.bottom
                    self.dy = 0


    def morre(self, perigo):
        self.bateu = pygame.sprite.spritecollide(self, perigo, False)
        return self.bateu


class Botao(pygame.sprite.Sprite):
    def __init__(self, imgs, coord, real, ajuste, mata):
        super().__init__()
        self.imgs = imgs
        self.index = 0
        self.image = self.imgs[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (coord[0], coord[1])
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, cons.TAMANHO_BLOCO, 10)
        self.hitbox.topleft = (coord[0], coord[1] + ajuste)
        self.real = real
        self.mata = mata


    def apertou(self, caixas, agente):
        self.hitbox.y -= 1
        self.apertado = pygame.sprite.spritecollide(self, pygame.sprite.Group(caixas, agente), False)
        self.hitbox.y += 1
        self.hitbox.y += 1
        self.apertado = pygame.sprite.spritecollide(self, pygame.sprite.Group(caixas, agente), False)
        self.hitbox.y -= 1
            
        if self.apertado:
            self.index = 1
        else:
            self.index = 0

        self.image = self.imgs[self.index]

        self.hitbox.x = self.rect.x

        if self.apertado and self.mata: return "mata"
        elif not self.real: return None
        return self.apertado


class Porta(pygame.sprite.Sprite):
    def __init__(self, imgs, coord, permanente, botoes):
        super().__init__()
        self.imgs = imgs
        self.index = 0
        self.image = self.imgs[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (coord[0], coord[1])
        self.abrindo = False
        self.aberta = False
        self.permanente = permanente
        self.num_botoes = botoes


    def abrir(self, ativo):
        if ativo == None:
            return
        
        if ativo:
            self.abrindo = True
        if not ativo and not self.permanente:
            self.abrindo = False

        if self.abrindo:
            self.index += 0.1/self.num_botoes

        elif not self.permanente:
            self.index -= 0.1*self.num_botoes

        if self.index >= len(self.imgs)-1:
            self.index = len(self.imgs)-1
            self.aberta = True

        elif self.index < 0:
            self.index = 0

        else:
            if not self.permanente:
                self.aberta = False

        self.image = self.imgs[int(self.index)]

    
class Card(pygame.sprite.Sprite):
    def __init__(self, imgs, coord, bom, frase):
        super().__init__()
        self.imgs = imgs
        self.index = 0
        self.image = self.imgs[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (coord[0], coord[1])
        self.bom = bom
        self.frase = frase


    def update(self): 
        if self.index > len(self.imgs)-1:
            self.index = 0
        self.index += 0.2
        self.image = self.imgs[int(self.index)]