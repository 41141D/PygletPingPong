import random
import pyglet
from pyglet import shapes
from pyglet.window import key
WINNING_SCORE = 5
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_SPEED=5
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, caption="Pong - Step 1")
batch = pyglet.graphics.Batch()
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_RADIUS = 12
right_paddle=shapes.Rectangle(x=(WINDOW_WIDTH-40),y=(WINDOW_HEIGHT-PADDLE_HEIGHT)/2,width=PADDLE_WIDTH, height=PADDLE_HEIGHT, batch=batch,color=(255,0,0))
left_paddle=shapes.Rectangle(x=40,y=(WINDOW_HEIGHT-PADDLE_HEIGHT)/2,width=PADDLE_WIDTH, height=PADDLE_HEIGHT, batch=batch)
ball = shapes.Circle(x=WINDOW_WIDTH/2,y=WINDOW_HEIGHT/2,batch=batch,color=(255,255,255),radius=BALL_RADIUS)
ball_dx = 240
ball_dy = 180

left_score = 0
right_score = 0
game_over = False

score_label = pyglet.text.Label(
    "0   -   0",
    font_size=28, x=WINDOW_WIDTH / 2, y=WINDOW_HEIGHT - 50,
    anchor_x="center", anchor_y="center", batch=batch,
)
message_label = pyglet.text.Label(
    "",
    font_size=20, x=WINDOW_WIDTH / 2, y=WINDOW_HEIGHT / 2 + 60,
    anchor_x="center", anchor_y="center", batch=batch,
)

keys = key.KeyStateHandler()
window.push_handlers(keys)
def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))
def ball_hits_paddle(paddle):
    ball_right = ball.x + BALL_RADIUS
    ball_left = ball.x - BALL_RADIUS
    ball_top = ball.y + BALL_RADIUS
    ball_bottom = ball.y - BALL_RADIUS
    paddle_left = paddle.x
    paddle_right = paddle.x + paddle.width
    paddle_bottom = paddle.y
    paddle_top = paddle.y + paddle.height

    return (
            ball_right >= paddle_left
            and ball_left <= paddle_right
            and ball_top >= paddle_bottom
            and ball_bottom <= paddle_top
    )
def reset_ball(direction):
    global ball_dx,ball_dy
    ball.x = WINDOW_WIDTH / 2
    ball.y = WINDOW_HEIGHT / 2
    ball_dx = 240 * direction
    ball_dy = random.uniform(-150,150)
def update_score_label():
     score_label.text =  f"{left_score} - {right_score}"
def update(dt):
    global ball_dx, ball_dy,left_score, right_score, game_over,WINNING_SCORE
    if game_over:
        return
    if keys[key.W]:
        left_paddle.y += PADDLE_SPEED
    if keys[key.S]:
        left_paddle.y -= PADDLE_SPEED

    if keys[key.UP]:
        right_paddle.y += PADDLE_SPEED
    if keys[key.DOWN]:
        right_paddle.y -= PADDLE_SPEED
    left_paddle.y = clamp(left_paddle.y, 0, WINDOW_HEIGHT - PADDLE_HEIGHT)
    right_paddle.y = clamp(right_paddle.y, 0, WINDOW_HEIGHT - PADDLE_HEIGHT)

    ball.x += ball_dx * dt
    ball.y += ball_dy * dt
    if ball_dx < 0 and ball_hits_paddle(left_paddle):
        ball_dx = -(ball_dx + 5.5)
    if ball_dx > 0 and ball_hits_paddle(right_paddle):
        ball_dx = -(ball_dx + 5.5)

    if ball.x + BALL_RADIUS >= WINDOW_WIDTH:
        right_score+=1
        update_score_label()
        if right_score >= WINNING_SCORE:
            game_over = True
            message_label.text = "LEFT PADDLE WON U LOST U BITCH U SUCK!!😂😂😂😂"
        else:
            reset_ball(direction=-1)
    if ball.x-BALL_RADIUS <= 0:
        left_score+=1
        update_score_label()
        if left_score >= WINNING_SCORE:
            game_over = True
            message_label.text = "RIGHT PADDLE WON U LOST U ASSHOLE!"
        else:
            reset_ball(direction=1)
    if ball.y + BALL_RADIUS >= WINDOW_HEIGHT:
        ball.y = WINDOW_HEIGHT - BALL_RADIUS
        ball_dy = -ball_dy
    if ball.y - BALL_RADIUS <= 0:
        ball.y=BALL_RADIUS
        ball_dy = -ball_dy
pyglet.clock.schedule_interval(update, 1 / 60)
@window.event
def on_draw():
    window.clear()
    batch.draw()
pyglet.app.run()
