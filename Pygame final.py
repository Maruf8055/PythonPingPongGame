import csv
import pygame
import pygame_menu
import random
from database import Database

SCR_WID, SCR_HEI = 640, 480


class Player:
    _counter = 0
    padWid, padHei = 8, 64

    def __init__(self, x, num):
        Player._counter += 1
        self.id = Player._counter
        self.num = num
        if num == 2:
            self.x = SCR_WID - self.padWid
        else:
            self.x = x
        self.y = SCR_HEI / 2
        self.speed = 3
        self.score = 0
        self.score2 = 0
        self.scoreFont = pygame.font.SysFont("Arial", 24)
        self.name = ""

    def scoring(self):
        player_text = f"Player {self.num}"
        score_blit = self.scoreFont.render(f"{player_text}: {self.score}", 1, (255, 255, 255))
        screen.blit(score_blit, (32 if self.num == 1 else SCR_WID - 32 - self.scoreFont.size(f"{player_text}: {self.score}")[0], 16))
        if self.score == 10 or enemy.score == 10:
            print(f"{player_text} wins!")
            pygame.quit()
            exit()

    def movement(self):
        keys = pygame.key.get_pressed()
        if self.num == 1:
            if keys[pygame.K_w]:
                self.y -= self.speed
            elif keys[pygame.K_s]:
                self.y += self.speed
            if self.y <= 0:
                self.y = 0
            elif self.y >= SCR_HEI - 64:
                self.y = SCR_HEI - 64
        if self.num == 2:
            if keys[pygame.K_UP]:
                self.y -= self.speed
            elif keys[pygame.K_DOWN]:
                self.y += self.speed
            if self.y <= 0:
                self.y = 0
            elif self.y >= SCR_HEI - 64:
                self.y = SCR_HEI - 64

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.padWid, self.padHei))


class Ball:
    def __init__(self):
        self.x, self.y = SCR_WID / 2, SCR_HEI / 2
        self.speed_x = random.choice([-3, 3])
        self.speed_y = random.choice([-3, 3])
        self.size = 8

    def movement(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.y <= 0 or self.y >= SCR_HEI - self.size:
            self.speed_y *= -1

        if self.x <= 0:
            self.__init__()
            player.score2 += 1
            pygame.mixer.music.load("player2.mp3")
            pygame.mixer.music.play()
        elif self.x >= SCR_WID - self.size:
            self.__init__()
            self.speed_x = 3
            player.score += 1
            pygame.mixer.music.load("player1.mp3")
            pygame.mixer.music.play()

        if (self.y + self.size >= player.y) and (self.y <= player.y + player.padHei):
            if (self.x <= player.x + player.padWid):
                self.speed_x *= -1
                pygame.mixer.music.load("drama1.mp3")
                pygame.mixer.music.play()

        if (self.y + self.size >= enemy.y) and (self.y <= enemy.y + enemy.padHei):
            if (self.x >= enemy.x - enemy.padWid):
                self.speed_x *= -1
                pygame.mixer.music.load("drama2.mp3")
                pygame.mixer.music.play()

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.size, self.size))


class HorizontalPaddle:
    padWid, padHei = 64, 8

    def __init__(self):
        self.x = SCR_WID / 2 - self.padWid / 2
        self.y = 10
        self.speed = 2

    def movement(self):
        if self.x + self.padWid / 2 < ball.x:
            self.x += self.speed
        elif self.x + self.padWid / 2 > ball.x:
            self.x -= self.speed

        if self.x <= 0:
            self.x = 0
        elif self.x >= SCR_WID - self.padWid:
            self.x = SCR_WID - self.padWid

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.padWid, self.padHei))


pygame.init()
screen = pygame.display.set_mode((SCR_WID, SCR_HEI))
pygame.display.set_caption("Ping Pong Game")
clock = pygame.time.Clock()
FPS = 60
player = None
ball = None
enemy = None
horizontal_paddle = None

background_img = pygame.image.load("download.png")
background_img = pygame.transform.scale(background_img, (SCR_WID, SCR_HEI))

def write_game_data_to_csv(player1_name, player2_name, player1_score, player2_score, game_duration_minutes):
    data = [
        ['Player 1 Name', 'Player 2 Name', 'Player 1 Score', 'Player 2 Score', 'Game Duration (minutes)'],
        [player1_name, player2_name, player1_score, player2_score, game_duration_minutes]
    ]

    with open('game_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def set_player_names(value, name):
    global player1_name, player2_name
    if name == 'Player 1 Name: ':
        player1_name = value
    elif name == 'Player 2 Name: ':
        player2_name = value

def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Resume game on 'P' key press
                    paused = False

        # Display 'Paused' text on the screen
        paused_font = pygame.font.SysFont("Arial", 36)
        paused_text = paused_font.render("Paused", True, (255, 255, 255))
        screen.blit(paused_text, (SCR_WID // 2 - paused_text.get_width() // 2, SCR_HEI // 2 - paused_text.get_height() // 2))

        pygame.display.flip()
        clock.tick(FPS)

def start_the_game():
    global difficulty_level, current_round, player1_name, player2_name
    difficulty_level = 1
    current_round = 1
    player1_name = player1_name if player1_name.strip() else 'Player 1'
    player2_name = player2_name if player2_name.strip() else 'Player 2'
    main()

def main_menu():
    global player1_name, player2_name
    menu = pygame_menu.Menu('Ping Pong', SCR_WID, SCR_HEI, theme=pygame_menu.themes.THEME_GREEN)

    menu.add.text_input('Player 1: ', default='Player 1',
                        onchange=lambda value, name=' ': set_player_names(value, name))
    menu.add.text_input('Player 2: ', default='Player 2',
                        onchange=lambda value, name=' ': set_player_names(value, name))
    menu.add.button('Start', start_the_game)
    menu.add.button('Pause', pause_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(screen)

player1_name = ''
player2_name = ''

def main():
    global player, ball, enemy, horizontal_paddle, current_round

    player = Player(16, 1)
    player.name = player1_name
    enemy = Player(SCR_WID / 2 - 4, 2)
    enemy.name = player2_name

    ball = Ball()
    horizontal_paddle = HorizontalPaddle()

    db = Database()
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Pausing game on 'P' key press
                        pause_game()

            screen.blit(background_img, (0, 0))
            ball.movement()
            player.movement()
            enemy.movement()
            horizontal_paddle.movement()
            ball.draw()
            player.draw()
            enemy.draw()
            horizontal_paddle.draw()

            player.scoring()

            # added Display 'Pause: P' on the game screen
            pause_font = pygame.font.SysFont("ComicSans", 20)
            pause_text = pause_font.render("Pause: P", True, (255, 255, 255))
            screen.blit(pause_text, (10, 10))

            player1_score_text = f"{player.name}: {player.score}"
            player2_score_text = f"{enemy.name}: {player.score2}"
            player.scoreFont = pygame.font.SysFont("Arial", 24)
            score_blit_player = player.scoreFont.render(player1_score_text, 1, (255, 255, 255))
            score_blit_enemy = player.scoreFont.render(player2_score_text, 1, (255, 255, 255))
            screen.blit(score_blit_player, (32, 16))
            screen.blit(score_blit_enemy,
                        (SCR_WID - 32 - player.scoreFont.size(player2_score_text)[0], 16))

            pygame.display.flip()
            clock.tick(FPS)

    except KeyboardInterrupt:
        pygame.quit()

main_menu()
