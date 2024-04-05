import pygame
from sys import exit
from random import randint, choice
import pickle


def get_high_score():
    try:
        with open('high_score.pkl', 'rb') as file:
            high_score = pickle.load(file)
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        high_score = 0
    return high_score


def update_high_score(new_high_score):
    with open('high_score.pkl', 'wb') as file:
        pickle.dump(new_high_score, file)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_3.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_4.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0

        player_duck_1 = pygame.image.load('graphics/player/player_duck_3.png').convert_alpha()
        player_duck_2 = pygame.image.load('graphics/player/player_duck_4.png').convert_alpha()
        self.player_duck = [player_duck_1, player_duck_2]
        self.duck_index = 0

        self.player_jump = pygame.image.load('graphics/player/jump_2.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.wav')
        self.jump_sound.set_volume(1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.bottom >= 300:
            self.gravity = -15
            self.jump_sound.play()
        elif keys[pygame.K_DOWN]:
            self.rect.y += 30

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        keys = pygame.key.get_pressed()
        if self.rect.bottom < 300:
            self.image = self.player_jump
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom).inflate(-20, -10)
        elif keys[pygame.K_DOWN]:
            self.duck_index += 0.1
            if self.duck_index >= len(self.player_duck):
                self.duck_index = 0
            self.image = self.player_duck[int(self.duck_index)]
            self.rect = self.image.get_rect(midbottom=(80, 300))
            self.rect.inflate_ip(-10, 0)


        elif self.rect.bottom == 300:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0.1
            self.image = self.player_walk[int(self.player_index)]
            self.rect = self.image.get_rect(midbottom=(80, 300))
            self.rect.inflate_ip(-10, 0)

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'Sodra':
            sodra_1 = pygame.image.load('graphics/Obstacles/Sodra_1.png').convert_alpha()
            sodra_2 = pygame.image.load('graphics/Obstacles/Sodra_2.png').convert_alpha()
            self.frames = [sodra_1, sodra_2]
            y_pos = 275
        elif type == 'C':
            c_1 = pygame.image.load('graphics/Obstacles/C_1.png').convert_alpha()
            c_2 = pygame.image.load('graphics/Obstacles/C_2.png').convert_alpha()
            self.frames = [c_1, c_2]
            y_pos = 300
        elif type == 'VMI':
            VMI_1 = pygame.image.load('graphics/Obstacles/VMI_1.png').convert_alpha()
            VMI_2 = pygame.image.load('graphics/Obstacles/VMI_2.png').convert_alpha()
            self.frames = [VMI_1, VMI_2]
            y_pos = 232
        elif type == 'Stock':
            Stock_1 = pygame.image.load('graphics/Obstacles/Stock_1.png').convert_alpha()
            Stock_2 = pygame.image.load('graphics/Obstacles/Stock_2.png').convert_alpha()
            self.frames = [Stock_1, Stock_2]
            y_pos = 300
        elif type == 'Netflix':
            Netflix_1 = pygame.image.load('graphics/Obstacles/Netflix_1.png').convert_alpha()
            Netflix_2 = pygame.image.load('graphics/Obstacles/Netflix_2.png').convert_alpha()
            Netflix_3 = pygame.image.load('graphics/Obstacles/Netflix_3.png').convert_alpha()
            Netflix_4 = pygame.image.load('graphics/Obstacles/Netflix_4.png').convert_alpha()
            self.frames = [Netflix_1, Netflix_2, Netflix_3, Netflix_4]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(850, 1000), y_pos))
        self.rect.inflate_ip(-20, 0)

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= obstacle_speed
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    font = pygame.font.Font('font/Pixeltype.ttf', 30)
    global high_score
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = font.render(f'High Score: {high_score}    Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(topright=(780, 10))
    screen.blit(score_surf, score_rect)

    return current_time


def collision_sprite():
    global music_started
    game_over_sound = pygame.mixer.Sound('audio/game_over.wav')
    game_over_sound.set_volume(3)
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        pygame.mixer.music.stop()
        music_started = False
        game_over_sound.play()
        obstacle_group.empty()
        pygame.display.update()
        pygame.time.wait(1000)
        return False
    else:
        return True


pygame.init()
pygame.mixer.music.load('audio/Run.wav')
music_started = False

screen = pygame.display.set_mode((800, 400))

pygame.display.set_caption('Recruitment Run')
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf', 50)
font_2 = pygame.font.Font('font/Pixeltype.ttf', 20)

game_name_1 = font.render('Recruitment Run', False, (111, 196, 169))
game_name_1_rect = game_name_1.get_rect(center=(400, 80))
game_name_2 = font.render('GAME OVER', False, (111, 196, 169))
game_name_2_rect = game_name_2.get_rect(center=(400, 80))

game_message_1 = font.render('Press < Enter > to find a job', False, (111, 196, 169))
game_message_1_rect = game_message_1.get_rect(center=(400, 330))
game_message_2 = font.render('Press < Enter > to run again', False, (111, 196, 169))
game_message_2_rect = game_message_2.get_rect(center=(400, 330))
game_credit = font_2.render('2024 - Art and Music by Paulius J.', False, (111, 196, 169))
game_credit_rect = game_credit.get_rect(center=(400, 380))

game_active = False
start_time = 0
score = 0
obstacle_speed = 5
last_speed_increase = 0
millis = 1500
sky_speed = 1
ground_speed = 4
sun_speed = 1
clouds_speed = 2

high_score = get_high_score()

player = pygame.sprite.GroupSingle()

player.add(Player())
obstacle_group = pygame.sprite.Group()

background = pygame.image.load('graphics/Sky/Background.png').convert_alpha()
background_rect = background.get_rect(topleft=(0, 0))

sky_surf_1 = pygame.image.load('graphics/Sky/Sky_1.png').convert_alpha()
sky_surf_2 = pygame.image.load('graphics/Sky/Sky_3.png').convert_alpha()
sky_rect_1 = sky_surf_1.get_rect(topleft=(1, 0))
sky_rect_2 = sky_surf_2.get_rect(topleft=(800, 0))

clouds_surf = pygame.image.load('graphics/Sky/Clouds.png').convert_alpha()
clouds_rect_1 = clouds_surf.get_rect(topleft=(0, 20))
clouds_rect_2 = clouds_surf.get_rect(topleft=(800, 20))

sun_surf = pygame.image.load('graphics/Sky/Sun.png').convert_alpha()
sun_rect = sun_surf.get_rect(topright=(800, 10))

ground_surf = pygame.image.load('graphics/Ground/Ground.png').convert()
ground_rect_1 = ground_surf.get_rect(topleft=(0, 300))
ground_rect_2 = ground_surf.get_rect(topleft=(811, 300))

player_stand = pygame.image.load('graphics/Player/player_stand_2.png').convert_alpha()

player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))
player_dead = pygame.image.load('graphics/Player/player_dead.png').convert_alpha()
player_dead = pygame.transform.rotozoom(player_dead, 0, 2)
player_dead_rect = player_dead.get_rect(center=(400, 200))

obstacle_timer = pygame.USEREVENT + 1

pygame.time.set_timer(obstacle_timer, millis)


def update_obstacle_speed():
    global obstacle_speed, start_time, last_speed_increase, millis, sky_speed, ground_speed, sun_speed, clouds_speed
    elapsed_time = pygame.time.get_ticks() - start_time
    if elapsed_time // 10000 > last_speed_increase:
        if obstacle_speed < 15:
            obstacle_speed += 1
            obstacle_speed = min(obstacle_speed, 15)

        last_speed_increase = elapsed_time // 10000

        if millis > 600:
            millis -= 100
            millis = max(millis, 500)

        if sky_speed < 5:
            sky_speed += 1
            sky_speed = min(sky_speed, 5)

        if ground_speed < 15:
            ground_speed += 1
            ground_speed = min(ground_speed, 15)

        pygame.time.set_timer(obstacle_timer, millis)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if not music_started:
                pygame.mixer.music.play(-1)
                music_started = True
            update_obstacle_speed()
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['Sodra', 'VMI', 'Netflix', 'Stock', 'C'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:

        screen.blit(background, background_rect)

        screen.blit(sun_surf, sun_rect)

        screen.blit(clouds_surf, clouds_rect_1)
        screen.blit(clouds_surf, clouds_rect_2)

        screen.blit(sky_surf_1, sky_rect_1)
        screen.blit(sky_surf_2, sky_rect_2)

        clouds_rect_2.x -= clouds_speed
        clouds_rect_1.x -= clouds_speed

        sun_rect.x -= sun_speed

        sky_rect_1.x -= sky_speed
        sky_rect_2.x -= sky_speed

        if sun_rect.right <= 0:
            sun_rect.x = 800
        if clouds_rect_1.right <= 0:
            clouds_rect_1.x = 800
        if clouds_rect_2.right <= 0:
            clouds_rect_2.x = 800
        if sky_rect_1.right <= 0:
            sky_rect_1.x = 800
        if sky_rect_2.right <= 10:
            sky_rect_2.x = 800

        screen.blit(ground_surf, ground_rect_1)
        screen.blit(ground_surf, ground_rect_2)
        ground_rect_1.x -= ground_speed
        ground_rect_2.x -= ground_speed
        if ground_rect_1.right <= 0:
            ground_rect_1.x = 811
        if ground_rect_2.right <= 0:
            ground_rect_2.x = 811

        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

        if not game_active and score > high_score:
            high_score = score
            update_high_score(high_score)

        # pygame.draw.rect(screen, (255, 0, 0), player.sprite.rect, 2)
        # for obstacle in obstacle_group:
        #     pygame.draw.rect(screen, (255, 0, 0), obstacle.rect, 2)

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        sky_rect_1 = sky_surf_1.get_rect(topleft=(1, 0))
        sky_rect_2 = sky_surf_2.get_rect(topleft=(800, 0))
        clouds_rect_1 = clouds_surf.get_rect(topleft=(0, 20))
        clouds_rect_2 = clouds_surf.get_rect(topleft=(800, 20))
        sun_rect = sun_surf.get_rect(topright=(800, 10))
        screen.blit(game_credit, game_credit_rect)

        obstacle_speed = 5
        last_speed_increase = 0
        millis = 1500
        sky_speed = 1
        ground_speed = 4
        sun_speed = 1
        clouds_speed = 2

        if score == 0:
            screen.blit(game_message_1, game_message_1_rect)
            screen.blit(game_name_1, game_name_1_rect)
            score_message = font.render(
                f'< up > to Jump                                             < down > to Duck', False,
                (111, 196, 169))
            score_message_rect = score_message.get_rect(center=(400, 200))
            screen.blit(score_message, score_message_rect)
        else:
            score_message = font.render(
                f'Your score: {score}                                       High score: {high_score}', False,
                (111, 196, 169))
            score_message_rect = score_message.get_rect(center=(400, 200))
            screen.blit(score_message, score_message_rect)
            screen.blit(player_dead, player_dead_rect)
            screen.blit(game_name_2, game_name_2_rect)
            screen.blit(game_message_2, game_message_2_rect)

    pygame.display.update()
    clock.tick(60)
