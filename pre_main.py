import random
import time
from turtle import *

# functions
def listenToKeypressed():
    screen.listen()
    screen.onkeypress(moveLeft, 'Left')
    screen.onkeypress(moveRight, 'Right')
    screen.onkeypress(handle_space, 'space')

def handle_space():
    global playing
    if playing:
        create_rocket()
    else:
        playing = True
        instruction.clear()

def create_rocket():
    global last_shoot
    # chỉ cho phép tạo ra tên lửa sau khi xong thời gian chờ
    if time.time() >= reload_time + last_shoot:
        # Tạo ra tên lửa nằm ngay tại vị trí của phi thuyền
        rocket = Turtle()
        rocket.shape('rocket.gif')
        rocket.penup()
        rocket.goto(spaceship.xcor(), spaceship.ycor() + 50)
        rockets.append(rocket) # thêm tên lửa vừa tạo vô danh sách tên lửa

        last_shoot = time.time()

def moveLeft():
    x, y = spaceship.pos()
    spaceship.goto(x - 10, y)

def moveRight():
    x, y = spaceship.pos()
    spaceship.goto(x + 10, y)

def create_screen():
    screen = Screen()
    screen.bgpic('bg.png') # cài đặt hình nền
    screen.setup(width=800, height=800)
    screen.title('Space invaders')
    screen.tracer(0)
    return screen

def create_space_ship():
    spaceship = Turtle()
    spaceship.shape('space-ship.gif')
    spaceship.penup()
    spaceship.goto(0, -200)
    return spaceship

def outside(rocket):
    if rocket.ycor() > screen.window_height() // 2:
        return True
    return False
def move_rockets():
    for rocket in rockets:
        rocket.goto(rocket.xcor(), rocket.ycor() + 0.1)
        if outside(rocket) == True:
            rocket.hideturtle()
            rockets.remove(rocket)

def create_alien():
    global last_spawn
    if time.time() >= last_spawn + spawn_time:
        alien = Turtle()
        alien.shape('alien.gif')
        alien.penup()
        x_random = random.randint(-300, 300)
        alien.goto(x_random, 300)
        aliens.append(alien)
        last_spawn = time.time()

def move_alien(alien):
    x, y = alien.pos()
    alien.goto(x, y - 0.1)

def move_aliens():
    global playing
    for alien in aliens:
        move_alien(alien)

        if alien.ycor() <= -300:
            # alien.hideturtle()
            # aliens.remove(alien)
            playing = False

def check_collision():
    global score
    for alien in aliens:
        # found = False
        for rocket in rockets:
            if alien.distance(rocket) <= 20:
                alien.hideturtle()
                rocket.hideturtle()
                aliens.remove(alien)
                rockets.remove(rocket)
                found = True
                score += 1
                break
        # if found:
            # break

def create_score():
    score_t = Turtle()
    score_t.color('White')
    score_t.hideturtle()
    score_t.up()
    score_t.goto(200, 300)
    return score_t


def write_score():
    score_t.clear()
    score_t.write(f'Score: {score}', font=('Courier', 30, 'normal'), align='center')

def reset():
    global aliens, rockets, score
    for alien in aliens:
        alien.hideturtle()
    for rocket in rockets:
        rocket.hideturtle()

    aliens = []
    rockets = []
    score = 0
    spaceship.goto(0, -200)

def create_instruction():
    instruction = Turtle()
    instruction.penup()
    instruction.hideturtle()
    instruction.color('white')
    return instruction

def write_instruction():
    instruction.write(f'Press space to play again', font=('Courier', 30, 'normal'), align='center')

register_shape('alien.gif')
register_shape('rocket.gif')
register_shape('space-ship.gif')

# Global variables
screen = create_screen()
spaceship = create_space_ship()
rockets = [] # chứa tất cả tên lửa mà tàu đã bắn
reload_time = 0
last_shoot = 0
aliens = []
spawn_time = 1
last_spawn = 0
score = 0
score_t = create_score()
playing = True
instruction = create_instruction()

listenToKeypressed()

while True: # lặp lại mãi mãi
    print(len(aliens))
    if playing:
        move_rockets()
        move_aliens()

        check_collision()
        write_score()

        create_alien()
    else:
        reset()
        write_instruction()

    screen.update() # cập nhật giao diện


