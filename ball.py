from tkinter import *
import random
import time


class Ball:

    def __init__(self, canvas_name, paddle_name, color):
        self.canvas = canvas_name
        self.paddle = paddle_name
        self.id = canvas.create_oval(0, 0, 15, 15, fill=color)
        self.canvas.move(self.id, 250, 200)
        self.x = random.choice([-3, -2, -1, 1, 2, 3])
        self.y = -3
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.hit_bottom = False
        self.hit = 0

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[0] >= paddle_pos[0] and pos[2] <= paddle_pos[2]:
            if paddle_pos[1] <= pos[3] <= paddle_pos[3]:
                self.hit += 1
                return True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos) is True:
            self.y = -3


class Paddle:

    def __init__(self, canvas_name, color):
        self.canvas = canvas_name
        self.id = self.canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all("<KeyPress-Left>", self.move_left)
        self.canvas.bind_all("<KeyPress-Right>", self.move_right)
        self.canvas.bind_all("<KeyRelease>", self.stop)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        if pos[2] >= self.canvas_width:
            self.x = 0

    def move_left(self, event):
        pos = self.canvas.coords(self.id)
        if pos[0] >= 0:
            self.x = - 3

    def move_right(self, event):
        pos = self.canvas.coords(self.id)
        if pos[2] <= self.canvas_width:
            self.x = 3

    def stop(self, event):
        self.x = 0


class Scores:
    def __init__(self, canvas_name, ball_name):
        self.canvas = canvas_name
        self.ball = ball_name
        self.text = self.canvas.create_text(450, 10, text="0")

    def display_scores(self):
        n = str(self.ball.hit)
        self.canvas.itemconfig(self.text, text=n)


tk = Tk()
tk.title("Игра")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", True)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

paddle = Paddle(canvas, "blue")
ball = Ball(canvas, paddle, "red")
scores = Scores(canvas, ball)


def start(event):
    while True:
        if ball.hit_bottom is False:
            ball.draw()
            paddle.draw()
            scores.display_scores()
        else:
            time.sleep(1.0)
            canvas.itemconfig(ball.id, state="hidden")
            canvas.itemconfig(paddle.id, state="hidden")
            canvas.create_text(250, 200, text="Вы проиграли", fill="red", font=("Times", 25))

        tk.update()
        time.sleep(0.02)


canvas.bind_all("<Button-1>", start)
tk.mainloop()
