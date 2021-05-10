import pygame
import random

pygame.init()
disp_width = 500
disp_height = 500
play_window = pygame.display.set_mode((disp_width, disp_height))
pygame.display.set_caption('Run boy')
icon = pygame.image.load('icon.jpg')
pygame.display.set_icon(icon)

barrier_img = [pygame.image.load('palka1.png'), pygame.image.load('palka2.png'), pygame.image.load('palka3.png')]
barrier_options = [20, 316, 20, 314, 25, 300]
cloud_img = [pygame.image.load('cloud1.png'), pygame.image.load('cloud2.png')]

person_img = [pygame.image.load('1.png'), pygame.image.load('2.png'), pygame.image.load('3.png'),
              pygame.image.load('4.png'), pygame.image.load('5.png'), pygame.image.load('6.png'),
              pygame.image.load('7.png')]

img_counter = 0

width = 50
height = 60
pos_x = 100
pos_y = 265


class Object:
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.speed = speed

    def move(self):
        if self.x >= - self.width:
            play_window.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            return False

    def return_barricade(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        play_window.blit(self.image, (self.x, self.y))


clock = pygame.time.Clock()

jump_counter = 30
jump = False

scores = 0
above_barrier = False


def run_game():
    flag = True
    global jump
    barrier_arr = []
    create_barrier(barrier_arr)
    land = pygame.image.load('land.png')
    cloud = open_random_object()
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            jump = True
        if keys[pygame.K_ESCAPE]:
            pause()
        if jump:
            make_jump()

        play_window.blit(land, (0, 0))
        print_text('Scores:' + str(scores), 400, 20)
        drow_array(barrier_arr)
        move_object(cloud)
        draw_person()
        scores_upd(barrier_arr)
        if check_push(barrier_arr):
            flag = False
        pygame.display.update()
        clock.tick(80)
    return gameover()


def make_jump():
    global pos_y, jump, jump_counter
    if jump_counter >= -30:
        pos_y -= jump_counter / 2.3
        jump_counter -= 1
    else:
        jump_counter = 30
        jump = False


def create_barrier(array):
    choice = random.randrange(0, 3)
    img = barrier_img[choice]
    width = barrier_options[choice * 2]
    height = barrier_options[choice * 2 + 1]
    array.append(Object(disp_width + 100, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = barrier_img[choice]
    width = barrier_options[choice * 2]
    height = barrier_options[choice * 2 + 1]
    array.append(Object(disp_width + 250, height, width, img, 4))

    choice = random.randrange(2, 3)
    img = barrier_img[choice]
    width = barrier_options[choice * 2]
    height = barrier_options[choice * 2 + 1]
    array.append(Object(disp_width + 500, height, width, img, 4))


def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x)
    if maximum < disp_width:
        radius = disp_width
        if radius - maximum < 50:
            radius += 150
    else:
        radius = maximum
    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(200, 250)

    return radius


def drow_array(array):
    for barrier in array:
        check = barrier.move()
        if not check:
            radius = find_radius(array)
            choice = random.randrange(0, 3)
            img = barrier_img[choice]
            width = barrier_options[choice * 2]
            height = barrier_options[choice * 2 + 1]
            barrier.return_barricade(radius, height, width, img)


def open_random_object():
    choice = random.randrange(0, 2)
    cloud_images = cloud_img[choice]
    cloud = Object(disp_width, 80, 90, cloud_images, 2)
    return cloud


def move_object(cloud):
    check = cloud.move()
    if not check:
        choice = random.randrange(0, 2)
        cloud_images = cloud_img[choice]
        cloud.return_barricade(disp_width, random.randrange(10, 200), cloud.width, cloud_images)


def draw_person():
    global img_counter
    if img_counter == 35:
        img_counter = 0
    play_window.blit(person_img[img_counter // 8], (pos_x, pos_y))
    img_counter += 1


def print_text(message, x, y, font_color=(0, 0, 0), font_type='regular.ttf', font_size=20):
    font_types = pygame.font.Font(font_type, font_size)
    text = font_types.render(message, True, font_color)
    play_window.blit(text, (x, y))


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
        print_text('PAUSED. PRESS ENTER TO CONTINUE', 100, 200)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()
        clock.tick(15)


def check_push(barriers):
    for barriery in barriers:
        if pos_y + height >= barriery.y:
            if barriery.x <= pos_x <= barriery.x + barriery.width:
                return True
            elif barriery.x <= pos_x + width <= barriery.x + barriery.width:
                return True
    return False


def gameover():
    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
        print_text('Game over!Press enter to play again,esc to exit', 40, 200)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            return False

        pygame.display.update()
        clock.tick(15)


def scores_upd(barriers):
    global scores
    for barrier in barriers:
        if barrier.x - 2 <= pos_x <= barrier.x + 1:
            scores += 1


while run_game():
    scores = 0
    jump = False
    jump_counter = 30
    pos_y = 265
pygame.quit()
quit()
