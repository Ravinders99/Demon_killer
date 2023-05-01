import pygame 
from pygame import mixer
pygame.font.init()
mixer.init()

back_music= pygame.mixer.Sound("music\\background_music.mp3")
hit = pygame.mixer.Sound("music\\hit.wav")
bullet = pygame.mixer.Sound("music\\bullet.wav")
back_music.play()
back_music.set_volume(0.5)


screen = pygame.display.set_mode((900,500))
clock = pygame.time.Clock()
#color of the button

#title of the game 
pygame.display.set_caption("Demon Killer")
walkleft =[pygame.image.load("hero\\L1.png"),pygame.image.load("hero\\L2.png"),pygame.image.load("hero\\L3.png"),pygame.image.load("hero\\L4.png"),pygame.image.load("hero\\L5.png"),pygame.image.load("hero\\L6.png"),pygame.image.load("hero\\L7.png"),pygame.image.load("hero\\L8.png"),pygame.image.load("hero\\L9.png")]
walkright =[pygame.image.load("hero\\R1.png"),pygame.image.load("hero\\R2.png"),pygame.image.load("hero\\R3.png"),pygame.image.load("hero\\R4.png"),pygame.image.load("hero\\R5.png"),pygame.image.load("hero\\R6.png"),pygame.image.load("hero\\R7.png"),pygame.image.load("hero\\R8.png"),pygame.image.load("hero\\R9.png")]

bg =pygame.image.load("background1.jpg")
throwspeed=0
class Player():
    def __init__(self,x,y,width,height,health):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.speed=5
        self.m =1  #mass of the object
        self.jumpheigh =10
        self.isjump = False
        self.left = False
        self.right= False
        self.standing =True
        self.hitscreen =(self.x+10,self.y+5, 80,80)
        self.visible =True
        self.health =health
    def draw(self,screen):
       
        screen.blit(bg,(0,0))
        if self.health>0:
            if self.walkcount +1>=27:
                self.walkcount=0
            if not self.standing :
                if self.left ==True:
                    screen.blit(walkleft[self.walkcount//3],(self.x,self.y))
                    self.walkcount+=1
                elif self.right ==True:
                    screen.blit(walkright[self.walkcount//3],(self.x,self.y))
                    self.walkcount+=1
            else:
                if self.left:
                    screen.blit(walkleft[0],(self.x,self.y))
                else:
                    screen.blit(walkright[0],(self.x,self.y))
                # screen.blit(stand,(self.x,self.y))
            self.hitscreen =(self.x+5,self.y+5, 55,62)
            health1= pygame.draw.rect(screen,(250,0,0),(self.hitscreen[0],self.hitscreen[1]-10,50,10))
            health2= pygame.draw.rect(screen,(250,250,0),(self.hitscreen[0],self.hitscreen[1]-10,self.health,10))
                
        # pygame.draw.rect(screen,"red",self.hitscreen,2)
    def hit(self):
        self.walkcount=0
        
        if self.health>0:
            
            self.health-=5
        else:
            self.visible=False
            font1 =pygame.font.SysFont('comicsans',20)
            text =font1.render("YOU DIE",1,"red","white")
            screen.blit(text,(400,200))
            pygame.display.update()
           

class Weapon(object):
    def __init__(self,x,y,facing,radius):
        self.x=x
        self.y=y   
        self.facing=facing
        self.radius=radius
        self.vel=8*facing
        
    def draw(self,screen):
        self.hitscreen =(self.x-5,self.y-5, 12,12)
        # pygame.draw.rect(screen,"white",self.hitscreen,2)
        
        pygame.draw.circle(screen,"red",(self.x,self.y),self.radius) 
       # screen.blit(pygame.image.load("fire.jpg"),(self.x,self.y))    #use image as a weapon 


class Enemy(object):      # enemy class
    walkleft1=[pygame.image.load("villian\\L1E.png"),pygame.image.load("villian\\L2E.png"),pygame.image.load("villian\\L3E.png"),pygame.image.load("villian\\L4E.png"),pygame.image.load("villian\\L5E.png"),pygame.image.load("villian\\L6E.png"),pygame.image.load("villian\\L7E.png"),pygame.image.load("villian\\L8E.png"),pygame.image.load("villian\\L9E.png"),pygame.image.load("villian\\L10E.png"),pygame.image.load("villian\\L11E.png")]
    walkright1=[pygame.image.load("villian\\R1E.png"),pygame.image.load("villian\\R2E.png"),pygame.image.load("villian\\R3E.png"),pygame.image.load("villian\\R4E.png"),pygame.image.load("villian\\R5E.png"),pygame.image.load("villian\\R6E.png"),pygame.image.load("villian\\R7E.png"),pygame.image.load("villian\\R8E.png"),pygame.image.load("villian\\R9E.png"),pygame.image.load("villian\\R10E.png"),pygame.image.load("villian\\R11E.png")]
    def __init__(self,x,y,width,height,end,health):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end =end
        self.path=[x,end]
        self.walkcount =0
        self.vel =3
        self.health=health 
        self.hitscreen =(self.x+10,self.y+5, 10,5)
        self.visible =True
       
    def draw(self,screen): #enemy design
        self.move()
        if self.visible:
            if self.walkcount+1>=33:
                self.walkcount=0
            if self.vel >0:
                screen.blit(self.walkright1[self.walkcount//3],(self.x,self.y))
                self.walkcount+=1
            else:
                screen.blit(self.walkleft1[self.walkcount//3],(self.x,self.y))
                self.walkcount+=1
            self.hitscreen =(self.x+10,self.y, 40,64)
        
            health1= pygame.draw.rect(screen,(250,0,0),(self.hitscreen[0],self.hitscreen[1]-10,50,10))
            health2= pygame.draw.rect(screen,(250,250,0),(self.hitscreen[0],self.hitscreen[1]-10,self.health+5,10))
            
        # pygame.draw.rect(screen,"red",self.hitscreen,2)   
    def move(self):
        if self.vel >0:
            if self.x<self.path[1]+self.vel :
                self.x+=self.vel
            else:
                self.vel  =self.vel *-1
                self.x+=self.vel
                self.walkcount=0
        else:
            if  self.x >self.path[0]-self.vel:
                self.x+=self.vel 
            else:
                self.vel  =self.vel *-1
                self.x+=self.vel 
                self.walkcount=0
    def hit(self):
        if self.health>0:
            
            self.health-=5
        else:
            self.visible=False
            
shalin=Player(30,400,10,20,50)
enemy=Enemy(80,405,10,10,800,50)
fires =[]
def display():
    shalin.draw(screen)
    enemy.draw(screen)
    for fire in fires:
        fire.draw(screen)
    pygame.display.flip()
    pygame.display.update()
    
running = True
while running:
    clock.tick(40.5)
    if throwspeed>0:
        throwspeed+=1
    if throwspeed>10:
        throwspeed=0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if enemy.visible==True:
        if shalin.hitscreen[1]  < enemy.hitscreen[1] +enemy.hitscreen[3] and shalin.hitscreen[1] +shalin.hitscreen[3]>enemy.hitscreen[1]:
            if shalin.hitscreen[0]  <enemy.hitscreen[0] +enemy.hitscreen[2] and shalin.hitscreen[0] +shalin.hitscreen[2]>enemy.hitscreen[0]:
                shalin.hit()

    for fire in fires:
        if enemy.visible==True:
            if fire.hitscreen[1] + round(fire.hitscreen[3]/2) > enemy.hitscreen[1] and fire.hitscreen[1] + round(fire.hitscreen[3]/2) < enemy.hitscreen[1] +enemy.hitscreen[3]:
                    if fire.hitscreen[0] + fire.hitscreen[2] >enemy.hitscreen[0] and fire.hitscreen[0] + fire.hitscreen[2]< enemy.hitscreen[0] +enemy.hitscreen[2]:
                        enemy.hit()
                        fires.pop(fires.index(fire))
                        hit.play()
        else : 
            hit.stop()
        if fire.x<850 and fire.x>30:
                fire.x+=fire.vel
        else:
                fires.pop(fires.index(fire))
        
    keys = pygame.key.get_pressed()
    if shalin.visible==True:
        if keys[pygame.K_LCTRL] and throwspeed==0:
            bullet.play()
            bullet.set_volume(0.3)
            if shalin.left==True:
                facing =-1
            else: 
                facing =1
            if len(fires)<5:
                # fires.append(Weapon(round(shalin.x+shalin.width//2),round(shalin.y+shalin.height//2),60,60,facing))
                fires.append(Weapon(round(shalin.x+shalin.width//2 +30),round(shalin.y+shalin.height//2+25),facing,4))
            throwspeed =1
    
            
            
        if keys[pygame.K_LEFT] and shalin.x > shalin.speed+20:
            shalin.x-=shalin.speed
            shalin.left=True 
            shalin.right=False
            shalin.standing=False
        elif keys[pygame.K_RIGHT]  and shalin.x <830-shalin.width-shalin.speed:
            shalin.x+=shalin.speed
            shalin.right=True
            shalin.left=False
            shalin.standing=False
        else:
            shalin.standing=True
            shalin.walkcount=0
        if shalin.isjump ==False:
            if keys[pygame.K_SPACE]:
                shalin.isjump= True
                if shalin.right:
                    screen.blit(walkleft[0],(shalin.x,shalin.y))
                else:
                    screen.blit(walkright[0],(shalin.x,shalin.y))
                shalin.walkcount=0
        if shalin.isjump :
            # calculate force (F). F = 1 / 2 * mass * velocity ^ 2.
            F =(1 / 2)*shalin.m*(shalin.jumpheigh**2)
            # change in the y co-ordinate
            shalin.y-= F 
            # decreasing velocity while going up and become negative while coming down
            shalin.jumpheigh = shalin.jumpheigh-1  
            # object reached its maximum height
            if shalin.jumpheigh<0:
                
                # negative sign is added to counter negative velocity
                shalin.m =-1
            if shalin.jumpheigh ==-11: 
                shalin.isjump = False
                shalin.jumpheigh = 10
                shalin.m = 1
    display()
   
pygame.quit()
            