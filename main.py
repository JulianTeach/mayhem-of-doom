# 1 - import stuff
from pygame import *
from random import randint
import math
from random import choice
# 2 - create window + clock
WIDTH, HEIGHT = 800, 640
window = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
font.init()

# 3 - get base classes
class ImageSprite(sprite.Sprite):
    # constructor function. Runs ONCE every time a new object it's created
    def __init__(self, filename, pos, size):
        super().__init__()
        self.image = image.load(filename)
        self.image = transform.scale(self.image, size)
        self.rect = Rect(pos, size)
        self.initial_pos = pos
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)  
    def reset(self):
        self.rect.topleft = self.initial_pos
# 4 - create game classes
class PlayerSprite(ImageSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_d]:
            self.rect.x += 8
        if keys[K_a]:
            self.rect.x -= 8

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
    def shoot(self):
        b = BulletSprite(filename='bomb.png', pos=(0,0), size=(7,12)) # create a bullet
        b.rect.center = self.rect.midtop # place the bullet
        bullets.add(b) # add it to the group

class EnemySprite(ImageSprite):
    def __init__(self, filename, pos, size, speed):
        super().__init__(filename, pos, size)
        self.speed = Vector2(speed)
        self.angle = 0
    def update(self):
        self.rect.x += math.sin(self.angle) * 5
        self.rect.y += self.speed.y
        self.angle += 0.05
        # self.rect.topleft += self.speed
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
            self.rect.x = randint(0,WIDTH-self.rect.width)

class BulletSprite(ImageSprite):
    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()

class TextSprite():
    def __init__(self, text, color, pos, font_size):
        self.font = font.SysFont('mine.ttf', font_size)
        self.pos = pos
        self.color = color
        self.set_new_text(text)
    def set_new_text(self, new_text):
        self.image = self.font.render(new_text, True, self.color)
    def draw(self, surface):
        surface.blit(self.image, self.pos) 


score = 0
points_counter = TextSprite(
    text="Score: " + str(score), 
    color="hotpink", 
    pos=(50,50), 
    font_size=60)  


mixer.init()
# expl_sounds = []
# s = mixer.Sound('s1.ogg')
# expl_sounds.append(s)
# s = mixer.Sound('s2.ogg')
# expl_sounds.append(s)
# s = mixer.Sound('s3.ogg')
# expl_sounds.append(s)
mixer.music.load('blah.mp3')
mixer.music.play()

oof = mixer.Sound('s1.ogg')
expl_sounds = [mixer.Sound('s1.ogg'), mixer.Sound('s2.ogg'), mixer.Sound('s3.ogg')]



bg = ImageSprite(filename='bomb.png', pos=(0,0), size=(WIDTH, HEIGHT))
p1 = PlayerSprite(filename='cyborg.png', pos=(WIDTH/2,HEIGHT - 50), size=(40,40))

enemies = sprite.Group()
bullets = sprite.Group()

def create_enemy():
    y = -40
    x = randint(0,WIDTH-40) # 0 - 760
    sy = randint(2,4)
    e = EnemySprite(filename='cyborg.png', pos=(x,y), size=(40,40), speed=(0,sy))
    enemies.add(e)

for _ in range(50):
    create_enemy()

game_over = False
state = 'START'

# 5 - create loop
while not event.peek(QUIT):
    if not game_over:
        #region GAME
        for e in event.get(): # get the queue of events
            if e.type == KEYDOWN: # look for key down events
                if e.key == K_SPACE: # if the space key has been pressed
                    p1.shoot()
                    choice(expl_sounds).play()
        # 6 - draw bg
        bg.draw(window)
        window.fill('lightblue')

        enemies.update()
        enemies.draw(window)
        bullets.update()
        bullets.draw(window)

        player_hits = sprite.spritecollide(p1, enemies, True)
        for hit in player_hits:
            score -= 200
            points_counter.set_new_text( "Score: " + str(score) )
            create_enemy()

        enemy_hits = sprite.groupcollide(bullets, enemies, True, True)
        for hit in enemy_hits:
            create_enemy()
            score += 50
            points_counter.set_new_text( "Score: " + str(score) )
            # exp_sound.play()

        points_counter.draw(window)
        
        p1.update()
        p1.draw(window)
        #endregion GAME
        if score >= 10000:
            game_over = True
            state = "WIN"
        elif score <= -50000:
            game_over = True
            state = "L"
    else:
        if state == 'WIN':
            # win_img.draw(window)
            pass
        elif state == 'L':
            # lose_img.draw(window)
            pass
    # 7 - update display 
    display.update()
    # 8 - clock tick
    clock.tick(60)