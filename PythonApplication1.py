import pygame
from nesne import SpaceShip,Asteroid
from metodlar import get_random_position,resim_yukle,ekrana_bas_yazi


class Oyun:
    asteroidsGemiArasiMesafe=250
    def __init__(self):
        self._init_pygame()
        self.ekran=pygame.display.set_mode((800,800))
        self.arkaplan=resim_yukle("galaxywp.jpg",False)
        self.saat=pygame.time.Clock()
        self.font=pygame.font.Font(None,64)
        self.gosterilecek_mesaj=""

        self.asteroids=[]
        self.bullets=[]
        self.spaceship=SpaceShip((400,300),self.bullets.append)

        for k in range(6):
            while True:
                position=get_random_position(self.ekran)
                if(position.distance_to(self.spaceship.position)>self.asteroidsGemiArasiMesafe):
                    break
            self.asteroids.append(Asteroid(position,self.asteroids.append))

    def main_loop(self):
        while True:
            self._handle_input()
            self._oyun_gidisat()
            self._ciz()
    
    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks")

    def _handle_input(self):


        for girdi in pygame.event.get():

            if girdi.type==pygame.QUIT or(girdi.type==pygame.KEYDOWN and girdi.key== pygame.K_ESCAPE ):
                quit()

            elif(self.spaceship and girdi.type==pygame.KEYDOWN and girdi.key==pygame.K_SPACE):
                self.spaceship.shoot()

        hangi_tusa_basildi=pygame.key.get_pressed()

        if self.spaceship:
            if hangi_tusa_basildi[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif hangi_tusa_basildi[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            if hangi_tusa_basildi[pygame.K_UP]:
                self.spaceship.accelerate()


    def _oyun_gidisat(self):
        for game_object in self._get_game_objects():
            game_object.move(self.ekran)

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship=None
                    self.gosterilecek_mesaj="Kaybettiniz"
                    break

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break
        
        for bullet in self.bullets[:]:
            if not self.ekran.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)
        
        if not self.asteroids and self.spaceship:
            self.gosterilecek_mesaj="Kazandiniz"

    def _ciz(self):
        self.ekran.blit(self.arkaplan,(0,0))
        for game_object in self._get_game_objects():
            game_object.draw(self.ekran)

        if self.gosterilecek_mesaj:
            ekrana_bas_yazi(self.ekran,self.gosterilecek_mesaj,self.font)

        pygame.display.flip()
        self.saat.tick(60)

    def _get_game_objects(self):
        game_objects=[*self.asteroids,*self.bullets]
        if self.spaceship:
            game_objects.append(self.spaceship)
        
        return game_objects
    
