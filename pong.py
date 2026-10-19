"""Kétjátékos Pong Pygame-mel, szintetizált hanghatásokkal.

Irányítás:
  Bal játékos: W / S
  Jobb játékos: FEL / LE
  P: szünet
  R: új játék
  ESC: kilépés
"""

import math
import struct
import pygame

WIDTH = 900
HEIGHT = 600
FPS = 60
WHITE = (245, 245, 245)
BLACK = (15, 18, 28)
GRAY = (115, 125, 145)

PADDLE_W = 14
PADDLE_H = 100
PADDLE_SPEED = 7
BALL_RADIUS = 9
WIN_SCORE = 7


def wall_bounce(y, radius, velocity_y, screen_height):
    """Visszapattanás a felső vagy alsó falról. (új_y, új_vy) értéket ad."""
    if y - radius <= 0 and velocity_y < 0:
        return radius, abs(velocity_y)
    if y + radius >= screen_height and velocity_y > 0:
        return screen_height - radius, -abs(velocity_y)
    return y, velocity_y


def goal_scored(x, radius, screen_width):
    """'right', ha a jobb játékos szerez pontot; 'left', ha a bal."""
    if x + radius < 0:
        return "right"
    if x - radius > screen_width:
        return "left"
    return None


def paddle_bounce(ball_y, paddle_y, paddle_height, speed_x, speed_y,
                  direction):
    """Ütőütközés utáni sebesség. A direction értéke -1 vagy +1."""
    relative_hit = (ball_y - paddle_y) / (paddle_height / 2)
    relative_hit = max(-1.0, min(1.0, relative_hit))
    max_angle = math.radians(60)
    angle = relative_hit * max_angle
    speed = math.hypot(speed_x, speed_y)
    return direction * abs(speed * math.cos(angle)), speed * math.sin(angle)


def make_tone(frequency, duration=0.09, volume=0.35, sample_rate=22050):
    """16 bites mono hangminta előállítása, külső hangfájl nélkül."""
    sample_count = int(sample_rate * duration)
    samples = bytearray()
    fade_samples = max(1, int(sample_rate * 0.008))
    for i in range(sample_count):
        envelope = min(1.0, i / fade_samples, (sample_count - 1 - i) / fade_samples)
        value = int(32767 * volume * max(0.0, envelope)
                    * math.sin(2 * math.pi * frequency * i / sample_rate))
        samples.extend(struct.pack("<h", value))
    return bytes(samples)


def create_sounds():
    """Hangokat hoz létre; hibás/nem elérhető hangrendszernél néma módot használ."""
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
        return {
            "paddle": pygame.mixer.Sound(buffer=make_tone(720, 0.07)),
            "wall": pygame.mixer.Sound(buffer=make_tone(420, 0.06)),
            "score": pygame.mixer.Sound(buffer=make_tone(980, 0.18)),
        }
    except pygame.error:
        return {}


class Paddle:
    def __init__(self, x):
        self.rect = pygame.Rect(x, HEIGHT // 2 - PADDLE_H // 2,
                                PADDLE_W, PADDLE_H)

    def move(self, direction):
        self.rect.y += direction * PADDLE_SPEED
        self.rect.y = max(0, min(HEIGHT - PADDLE_H, self.rect.y))

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect, border_radius=5)


class Ball:
    def __init__(self):
        self.reset(1)

    def reset(self, direction=1):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.vx = 5 * direction
        self.vy = 2.5

    def rect(self):
        return pygame.Rect(round(self.x - BALL_RADIUS),
                           round(self.y - BALL_RADIUS),
                           BALL_RADIUS * 2, BALL_RADIUS * 2)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.y, self.vy = wall_bounce(self.y, BALL_RADIUS, self.vy, HEIGHT)

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (round(self.x), round(self.y)),
                           BALL_RADIUS)


def draw_text(screen, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    image = font.render(text, True, color)
    screen.blit(image, image.get_rect(center=(x, y)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Python Pong — Pygame")
    clock = pygame.time.Clock()
    sounds = create_sounds()

    left = Paddle(35)
    right = Paddle(WIDTH - 35 - PADDLE_W)
    ball = Ball()
    scores = {"left": 0, "right": 0}
    paused = False
    winner = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p and winner is None:
                    paused = not paused
                elif event.key == pygame.K_r:
                    scores = {"left": 0, "right": 0}
                    ball.reset(1)
                    winner = None
                    paused = False

        keys = pygame.key.get_pressed()
        if not paused and winner is None:
            left.move(int(keys[pygame.K_s]) - int(keys[pygame.K_w]))
            right.move(int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]))
            old_ball_vy = ball.vy
            ball.update()
            if ball.vy != old_ball_vy and "wall" in sounds:
                sounds["wall"].play()

            if ball.rect().colliderect(left.rect) and ball.vx < 0:
                ball.x = left.rect.right + BALL_RADIUS
                ball.vx, ball.vy = paddle_bounce(
                    ball.y, left.rect.centery, PADDLE_H, ball.vx, ball.vy, 1
                )
                if "paddle" in sounds:
                    sounds["paddle"].play()

            if ball.rect().colliderect(right.rect) and ball.vx > 0:
                ball.x = right.rect.left - BALL_RADIUS
                ball.vx, ball.vy = paddle_bounce(
                    ball.y, right.rect.centery, PADDLE_H, ball.vx, ball.vy, -1
                )
                if "paddle" in sounds:
                    sounds["paddle"].play()

            scorer = goal_scored(ball.x, BALL_RADIUS, WIDTH)
            if scorer:
                scores[scorer] += 1
                if "score" in sounds:
                    sounds["score"].play()
                if scores[scorer] >= WIN_SCORE:
                    winner = scorer
                else:
                    ball.reset(1 if scorer == "right" else -1)

        screen.fill(BLACK)
        pygame.draw.line(screen, GRAY, (WIDTH // 2, 0),
                         (WIDTH // 2, HEIGHT), 2)
        draw_text(screen, str(scores["left"]), 64, WIDTH // 4, 55)
        draw_text(screen, str(scores["right"]), 64, 3 * WIDTH // 4, 55)
        left.draw(screen)
        right.draw(screen)
        ball.draw(screen)

        if paused:
            draw_text(screen, "SZUNET - P a folytatashoz", 36,
                      WIDTH // 2, HEIGHT // 2)
        elif winner:
            player = "Bal jatekos" if winner == "left" else "Jobb jatekos"
            draw_text(screen, f"{player} nyert!  R: uj jatek", 38,
                      WIDTH // 2, HEIGHT // 2)
        else:
            draw_text(screen, "W/S", 24, 65, HEIGHT - 25, GRAY)
            draw_text(screen, "FEL/LE", 24, WIDTH - 65, HEIGHT - 25, GRAY)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
