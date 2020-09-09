from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.lang import Builder


class PongPaddle(Widget):
    score = NumericProperty()

    # Bouncing the ball when touches the paddle with .collide_widget(ball)
    def bounce(self, ball):
        if self.collide_widget(ball):
            speedup = 1.1
            offset = 0.1 * Vector(0, ball.center_y - self.center_y)
            ball.velocity = speedup * (offset - ball.velocity)


class PongBall(Widget):
    velocity_x = NumericProperty()
    velocity_y = NumericProperty()
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # how to move the ball
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty()
    player1 = ObjectProperty()
    player2 = ObjectProperty()

    # kickoff give a vel to move()
    def serve(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel
    
    def update(self, frame):
        self.ball.move()
        self.player1.bounce(self.ball)
        self.player2.bounce(self.ball)

        # Ball bouncing from TOP and BOTTOM
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        # Keeping Scores
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve(vel=(-4, 0))

    # Move Paddles
    def on_touch_move(self, touch):
        if touch.x < self.width/2:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width/2:
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game


if __name__ == '__main__':
    PongApp().run()
