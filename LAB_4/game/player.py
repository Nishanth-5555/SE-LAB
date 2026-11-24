import pygame

SPEED = 4
GRAVITY = 0.55
JUMP_VELOCITY = -13
MAX_FALL_SPEED = 12


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.y = float(y)  # sub-pixel vertical position
        self.vel_y = 0
        self.on_ground = False
        self.color = (60, 160, 220)

    def update(self, keys, platforms, width):
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = SPEED
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = JUMP_VELOCITY
            self.on_ground = False

        self.vel_y = min(self.vel_y + GRAVITY, MAX_FALL_SPEED)
        self.rect.x = max(0, min(width - self.rect.width, self.rect.x + dx))

        # Remember where the feet were BEFORE moving this frame.
        prev_bottom = self.rect.bottom
        self.y += self.vel_y
        self.rect.y = round(self.y)

        # One-way platforms: only land when falling AND the feet were at or
        # above the platform's top edge last frame and are at/below it now.
        # Jumping up through a platform from below never snaps the player.
        self.on_ground = False
        if self.vel_y >= 0:
            landing = None
            for p in platforms:
                overlaps_x = self.rect.right > p.left and self.rect.left < p.right
                crossed_top = prev_bottom <= p.top <= self.rect.bottom
                if overlaps_x and crossed_top and (landing is None or p.top < landing.top):
                    landing = p
            if landing is not None:
                self.rect.bottom = landing.top
                self.y = float(self.rect.y)
                self.vel_y = 0
                self.on_ground = True

    def draw(self, screen, cam_y):
        dr = self.rect.move(0, -int(cam_y))
        pygame.draw.rect(screen, self.color, dr, border_radius=6)
        pygame.draw.circle(screen, (255, 220, 180), (dr.centerx, dr.top + 8), 7)
