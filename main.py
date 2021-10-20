import pygame,sys
from pygame.locals import *


pygame.init()

screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption('tugra bird')

beyaz = (255,255,255)

clock = pygame.time.Clock()

screen.fill(beyaz)


calistir = True

menücük = True


class Arkaplan():
    def __init__(self):
        self.arkaplan_resmi = pygame.image.load("arkaplannew.png")
        self.arkaplan_resmi = pygame.transform.scale(self.arkaplan_resmi,(1280,720))
        self.rectle = self.arkaplan_resmi.get_rect()

        self.bgx1 = 0
        self.bgy1 = 0

        self.bgx2 = self.rectle.height
        self.bgy2 = 0
        self.hareket_hizi = 4

    def güncelle(self):
        self.bgx1 -= self.hareket_hizi
        self.bgx2 -= self.hareket_hizi
        if self.bgx1 <= - self.rectle.height:
            self.bgx1 = self.rectle.height
        if self.bgx2 <= - self.rectle.height:
            self.bgx2 = self.rectle.height

    def render(self):
        screen.blit(self.arkaplan_resmi, (self.bgx1, self.bgy1))
        screen.blit(self.arkaplan_resmi, (self.bgx2, self.bgy2))

class Engel():
    def __init__(self,borux,boruy,boyut = "kucuk"):
        if  boyut == "kucuk":
            self.buyukengel = pygame.image.load("pipe.png")
            self.buyukengel = pygame.transform.scale(self.buyukengel,(140,305))
        if boyut == "buyuk":
            self.buyukengel = pygame.image.load("big_pipe.png")
            self.buyukengel = pygame.transform.scale(self.buyukengel,(140,400))

        self.boyut = boyut
        self.borux = borux
        self.boruy = boruy
        self.rect = self.buyukengel.get_rect()
        self.boruhizi = 4
        self.rect.y = boruy
        self.rect.x = borux
        
    def düzboruguncelleme(self):
        #yukarıdakiborular
        self.borux -= self.boruhizi
        if self.boyut == "kucuk":
            self.rect.x = self.borux
            self.rect.y = self.boruy
        if self.boyut == "buyuk":
            self.rect.x = self.borux - 1
            self.rect.y = self.boruy - 3

    
    def tersborugüncelleme(self):
        #aşağıdaki borular
        self.borux -= self.boruhizi
        if self.boyut == "kucuk":

            self.rect.x = self.borux
            self.rect.y = self.boruy



    def borurender(self):
        screen.blit(self.buyukengel,(self.borux,self.boruy))
        #pygame.draw.rect(screen,(0,0,255),self.rect,2)
    def tersborurender(self):
        sj = pygame.transform.flip(self.buyukengel,False,True)
        screen.blit(sj,(self.borux,self.boruy))
        #pygame.draw.rect(screen,(0,0,255),self.rect,2)

    def borureset(self):
        self.boyut = self.boyut
        self.borux = self.borux
        self.boruy = self.boruy
        self.rect = self.buyukengel.get_rect()
        self.boruhizi = 4
        self.rect.y = self.boruy
        self.rect.x = self.borux


        

class Kuş():
    def __init__(self):
        self.kus_resmi = pygame.image.load("yellowbird-midflap.png")
        self.kus_resmi = pygame.transform.scale(self.kus_resmi,(68,48))
        self.kus_resmi_alt = pygame.image.load("yellowbird-downflap.png")
        self.kus_resmi_alt = pygame.transform.scale(self.kus_resmi_alt,(68,48))
        self.kus_resmi_üst = pygame.image.load("yellowbird-upflap.png")
        self.kus_resmi_üst = pygame.transform.scale(self.kus_resmi_üst,(68,48))
        self.kusrect = self.kus_resmi.get_rect()
        self.kusx1 = 50
        self.kusy1 = 220
        self.hareket_kus = 5
        self.ziplama_hizi = 0.901
        self.kusrect.x = 50
        self.kusrect.y = 220

    def guncelle(self):
        self.kusy1 += self.hareket_kus
        self.kusrect.y = self.kusy1
        if self.kusy1 >= 532:
            self.hareket_kus = 0
        else:
            self.hareket_kus = 4

    def ziplama(self):

        tus = pygame.key.get_pressed()
        if tus[pygame.K_SPACE] or tus[pygame.K_UP]:
            if self.kusy1 >= 200:
                self.kusy1 *= 0.96
            else:
                self.kusy1 *= self.ziplama_hizi

    def kusreset(self):
        self.kusx1 = 50
        self.kusy1 = 220
        self.hareket_kus = 5
        self.ziplama_hizi = 0.901
        self.kusrect.x = 50
        self.kusrect.y = 220



    def render(self):
        tus = pygame.key.get_pressed()
        if tus[pygame.K_UP] or tus[pygame.K_SPACE]:
            screen.blit(self.kus_resmi_üst,(self.kusx1,self.kusy1))
        elif self.hareket_kus > 0:
            screen.blit(self.kus_resmi_alt,(self.kusx1,self.kusy1))
        else:
            screen.blit(self.kus_resmi,(self.kusx1,self.kusy1))
        #pygame.draw.rect(screen,(0,0,255),self.kusrect,2)

class Skor():
    def __init__(self):
        self.skorsayi = 0
        self.fontum = pygame.font.SysFont('Comic Sans MS', 30)
        self.ikincifont = pygame.font.SysFont("Comic Sans MS",30)

    def skorrender(self):
        self.yazi = self.fontum.render(f"Skor: {self.skorsayi}",False,(255,255,255))
        self.ikinciyazi = self.ikincifont.render(f"Skor: {self.skorsayi}",False,(0,0,0))

        screen.blit(self.ikinciyazi,(3,3))
        screen.blit(self.yazi,(0,0))



class Oyun_menu():
    def __init__(self,tür = "normal"):
        self.tür = tür
        if tür == "normal":


            self.menu_resim = pygame.image.load("menuresim.png")
            self.menux1 = 0
            self.menuy1 = 0

        if tür == "kapanış":
            self.menu_resim = pygame.image.load("game_over.png")
            self.menu_resim = pygame.transform.scale(self.menu_resim,(333,106))
            self.menux1 = 480
            self.menuy1 = 300

    def menugetir(self):
        tus = pygame.key.get_pressed()
        if tus[pygame.K_a]: 
            global menücük
            menücük = False
        else:
            screen.blit(self.menu_resim,(self.menux1,self.menuy1))
            
menüm = Oyun_menu()
kapanmamenü = Oyun_menu("kapanış")
sarikus = Kuş()
arkaplanim = Arkaplan()
boru1 = Engel(640,450,"kucuk")
boru2= Engel(640,0,"kucuk")
boru3 = Engel(1100,-100,"kucuk")
boru4 = Engel(1100,350,"buyuk")
boru5 = Engel(1600,-100,"buyuk")
boru6 = Engel(1600,450,"kucuk")
tablo = Skor()

gameover = False
kapanma = False

def oyunbitti():
    global menücük
    global kapanma
    arkaplanim.render()
    sarikus.render()
    boru1.borurender()
    boru2.tersborurender()
    boru3.tersborurender()
    boru4.borurender()
    boru5.tersborurender()
    boru6.borurender()
    tablo.skorsayi = 0
    tablo.skorrender()
    global gameover
    kapanma = True
    tus = pygame.key.get_pressed()
    if tus[pygame.K_a]:
        menücük = False
        kapanma = False
    else:
        sarikus.kusreset()
        boru1.borux = 640
        boru1.boruy = 450
        boru2.borux = 640
        boru2.boruy = 0
        boru3.borux = 1100
        boru3.boruy = -100
        boru4.borux = 1100
        boru4.boruy = 350
        boru5.borux = 1600
        boru5.boruy = -100
        boru6.borux = 1600
        boru6.boruy = 450


        menücük = True



def kontrol_et():
    for kadir in borularliste:
        if sarikus.kusrect.colliderect(kadir.rect):
            oyunbitti()

borularliste = [boru1,boru2,boru3,boru4,boru5,boru6]
skorboru = [boru1,boru3,boru5]

while calistir:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:sys.exit()
        if menücük == True and not kapanma:
            menüm.menugetir()
        if menücük == True and kapanma:
            kapanmamenü.menugetir()
        if not menücük and not gameover:

            sarikus.ziplama()
            arkaplanim.güncelle()
            arkaplanim.render()
            sarikus.guncelle()
            sarikus.render()
            boru1.tersborugüncelleme()
            boru1.borurender()
            boru2.tersborurender()
            boru2.düzboruguncelleme()
            boru3.tersborurender()
            boru3.düzboruguncelleme()
            boru4.düzboruguncelleme()
            boru4.borurender()
            boru5.tersborurender()
            boru5.düzboruguncelleme()
            boru6.düzboruguncelleme()
            boru6.borurender()
            tablo.skorrender()
            kontrol_et()
            for p in borularliste:
                if p.borux <= -200:
                    p.borux = 1300

        for skorliste in skorboru:
            if skorliste.borux == 48:

                tablo.skorsayi += 1
                tablo.skorrender()
        
        pygame.display.update()

