import pygame
from game.player import Player
from game.world import generate_platforms, draw_lava, SPRING_VELOCITY

WIDTH,HEIGHT=500,640
FPS=60
BG=(20,15,30)
GROUND_Y=HEIGHT+200

# lava speed / surge tuning
LAVA_MAX_RISE=1.2
FIRST_SURGE=360        # frames before the first surge (6 s)
SURGE_INTERVAL=600     # a surge every 10 s after that
SURGE_DURATION=120     # each surge lasts 2 s
SURGE_WARNING=90       # 1.5 s warning before a surge
SURGE_MULT=2.5         # lava rises this many times faster during a surge

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Lava Escape")
        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont("monospace",24,bold=True)
        self.big_font=pygame.font.SysFont("monospace",42,bold=True)
        self.reset()

    def reset(self):
        self.platforms=generate_platforms(WIDTH,GROUND_Y)
        self.player=Player(WIDTH//2-16,GROUND_Y-50)
        # start the camera on the player so the ground/start area is visible
        self.cam_y=self.player.rect.centery-int(HEIGHT*0.65)
        # give the player a few seconds before the lava reaches the ground
        self.lava_y=GROUND_Y+180
        self.lava_rise=0.4
        self.score=0
        self.game_over=False
        self.won=False
        self.top_y=self.platforms[-1].y
        self.frame=0
        self.next_surge=FIRST_SURGE
        self.surge_left=0
        self.current_rise=self.lava_rise

    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: return False
            if event.type==pygame.KEYDOWN and event.key==pygame.K_r: self.reset()
        return True

    def update(self):
        if self.game_over or self.won: return
        keys=pygame.key.get_pressed()
        self.player.update(keys,[p.rect for p in self.platforms],WIDTH)
        for p in self.platforms:
            if p.rect is self.player.landed_on:
                p.on_landed()
                if p.kind=="spring":
                    # high-velocity launch instead of a normal landing
                    self.player.vel_y=SPRING_VELOCITY
                    self.player.on_ground=False
            p.update()
        # crumbled platforms disappear for good
        self.platforms=[p for p in self.platforms if not p.gone]
        target=self.player.rect.centery-HEIGHT//2
        if target<self.cam_y: self.cam_y=target
        # periodic lava surges briefly multiply the rise speed
        if self.frame>=self.next_surge:
            self.surge_left=SURGE_DURATION
            self.next_surge+=SURGE_INTERVAL
        surging=self.surge_left>0
        if surging: self.surge_left-=1
        self.current_rise=self.lava_rise*(SURGE_MULT if surging else 1)
        self.lava_y-=self.current_rise
        self.lava_rise=min(LAVA_MAX_RISE,self.lava_rise+0.0003)
        self.score=max(0,(GROUND_Y-self.player.rect.y)//10)
        self.frame+=1
        if self.player.rect.bottom>=self.lava_y:
            self.game_over=True
        if self.player.rect.top<=self.top_y-20:
            self.won=True

    def draw(self):
        self.screen.fill(BG)
        for p in self.platforms:
            p.draw(self.screen,self.cam_y,self.frame)
        self.player.draw(self.screen,self.cam_y)
        draw_lava(self.screen,self.lava_y,self.cam_y,WIDTH,HEIGHT,self.frame,self.surge_left>0)
        self._draw_danger_hud()
        sc=self.font.render(f"Height: {self.score}m  R=Restart",True,(220,200,180))
        self.screen.blit(sc,(8,10))
        if self.game_over:
            self._msg("LAVA GOT YOU!",(220,80,40))
        if self.won:
            self._msg("ESCAPED!",(80,220,100))
        pygame.display.flip()

    def _draw_danger_hud(self):
        # vertical danger meter on the right: how fast the lava is rising right now
        x,y,w,h=WIDTH-34,50,18,200
        pygame.draw.rect(self.screen,(40,30,45),(x,y,w,h),border_radius=4)
        frac=min(1.0,self.current_rise/(LAVA_MAX_RISE*SURGE_MULT))
        fill=int(h*frac)
        if frac<0.35: col=(80,200,90)
        elif frac<0.6: col=(230,200,60)
        else: col=(235,70,40)
        pygame.draw.rect(self.screen,col,(x,y+h-fill,w,fill),border_radius=4)
        pygame.draw.rect(self.screen,(200,190,180),(x,y,w,h),1,border_radius=4)
        small=pygame.font.SysFont("monospace",14,bold=True)
        lbl=small.render("LAVA",True,(220,200,180))
        self.screen.blit(lbl,(x+w//2-lbl.get_width()//2,y+h+4))
        spd=small.render(f"x{self.current_rise/0.4:.1f}",True,col)
        self.screen.blit(spd,(x+w//2-spd.get_width()//2,y+h+20))
        # distance between the player's feet and the lava
        gap=max(0,int(self.lava_y-self.player.rect.bottom)//10)
        gcol=(235,70,40) if gap<15 else (220,200,180)
        g=self.font.render(f"Lava: {gap}m below",True,gcol)
        self.screen.blit(g,(8,38))
        # surge warning / active banner
        if self.game_over or self.won: return
        until=self.next_surge-self.frame
        text=None
        if self.surge_left>0:
            text="LAVA SURGE!"
        elif 0<until<=SURGE_WARNING:
            text="SURGE INCOMING"
        if text and (self.frame//8)%2==0:
            t=self.font.render(text,True,(255,90,40))
            self.screen.blit(t,(WIDTH//2-t.get_width()//2,72))

    def _msg(self,text,color):
        ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        ov.fill((0,0,0,150))
        self.screen.blit(ov,(0,0))
        m=self.big_font.render(text,True,color)
        s=self.font.render("Press R to Play Again",True,(200,200,200))
        self.screen.blit(m,(WIDTH//2-m.get_width()//2,HEIGHT//2-40))
        self.screen.blit(s,(WIDTH//2-s.get_width()//2,HEIGHT//2+20))

    def run(self):
        running=True
        while running:
            running=self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
