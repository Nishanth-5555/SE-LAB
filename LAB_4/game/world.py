import math
import random

import pygame

PLATFORM_COLOR = (100, 80, 50)
CRUMBLE_COLOR = (150, 110, 90)
SPRING_COLOR = (70, 200, 120)
LAVA_COLOR = (220, 60, 20)

CRUMBLE_CHANCE = 0.22
CRUMBLE_FRAMES = 45  # ~0.75 s of shaking before the platform disintegrates
SPRING_CHANCE = 0.15
SPRING_VELOCITY = -19  # vs. -13 for a normal jump


class Platform:
    """A platform with a type: 'normal', 'crumble' or 'spring'."""

    def __init__(self, rect, kind="normal"):
        self.rect = rect
        self.kind = kind
        self.crumble_timer = None  # counts down once a crumbling platform is stepped on
        self.gone = False
        self.bounce_anim = 0  # frames of spring compression animation left

    @property
    def y(self):
        return self.rect.y

    def on_landed(self):
        if self.kind == "crumble" and self.crumble_timer is None:
            self.crumble_timer = CRUMBLE_FRAMES
        if self.kind == "spring":
            self.bounce_anim = 12

    def update(self):
        if self.bounce_anim > 0:
            self.bounce_anim -= 1
        if self.crumble_timer is not None:
            self.crumble_timer -= 1
            if self.crumble_timer <= 0:
                self.gone = True

    def draw(self, screen, cam_y, frame):
        dr = self.rect.move(0, -int(cam_y))
        if self.kind == "crumble":
            color = CRUMBLE_COLOR
            if self.crumble_timer is not None:
                # shake harder and fade as it is about to break
                left = self.crumble_timer / CRUMBLE_FRAMES
                amp = 1 + int((1 - left) * 4)
                dr.x += random.randint(-amp, amp)
                dr.y += random.randint(-amp // 2, amp // 2)
                color = tuple(int(c * (0.45 + 0.55 * left)) for c in CRUMBLE_COLOR)
            pygame.draw.rect(screen, color, dr, border_radius=4)
            # cracks so fragile platforms are recognisable before stepping on them
            for cx in range(dr.left + 14, dr.right - 8, 26):
                pygame.draw.line(screen, (60, 40, 30), (cx, dr.top + 2), (cx + 5, dr.centery), 2)
                pygame.draw.line(screen, (60, 40, 30), (cx + 5, dr.centery), (cx - 2, dr.bottom - 2), 2)
        elif self.kind == "spring":
            # coil on top of a green pad; it squashes briefly after launching
            squash = self.bounce_anim // 2
            pygame.draw.rect(screen, SPRING_COLOR, dr, border_radius=4)
            coil_h = max(4, 12 - squash)
            for cx in range(dr.left + 12, dr.right - 8, 22):
                pts = [(cx + (6 if k % 2 else 0), dr.top - k * coil_h // 4) for k in range(5)]
                pygame.draw.lines(screen, (230, 230, 120), False, pts, 2)
                pygame.draw.line(screen, (230, 230, 120), (cx - 2, dr.top - coil_h), (cx + 8, dr.top - coil_h), 3)
        else:
            pygame.draw.rect(screen, PLATFORM_COLOR, dr, border_radius=4)


def generate_platforms(width, base_y, count=30):
    plats = [Platform(pygame.Rect(0, base_y, width, 20))]  # ground
    y = base_y - 110
    for i in range(count):
        w = random.randint(80, 200)
        x = random.randint(0, width - w)
        kind = "normal"
        # keep the first couple of platforms and the final (goal) platform safe
        if 2 <= i < count - 1:
            r = random.random()
            if r < CRUMBLE_CHANCE:
                kind = "crumble"
            elif r < CRUMBLE_CHANCE + SPRING_CHANCE:
                kind = "spring"
        plats.append(Platform(pygame.Rect(x, y, w, 16), kind))
        y -= random.randint(80, 130)
    return plats


def draw_lava(screen, lava_y, cam_y, width, height, frame):
    ly = int(lava_y - cam_y)
    if ly < height:
        # lava surface wave
        pts = [(0, ly)]
        for x in range(0, width + 20, 20):
            pts.append((x, ly + int(math.sin(x * 0.08 + frame * 0.1) * 8)))
        pts.append((width, height))
        pts.append((0, height))
        pygame.draw.polygon(screen, LAVA_COLOR, pts)
        # glow
        s = pygame.Surface((width, 30), pygame.SRCALPHA)
        for i in range(15):
            pygame.draw.line(s, (255, 100, 0, max(0, 60 - i * 4)), (0, i), (width, i), 1)
        screen.blit(s, (0, ly - 15))
