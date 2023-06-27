import pyxel
import math
import random


# 공 제어를 위한 Ball 클래스
class Ball:

    def __init__(self, game):
        self.game = game
        self.x = 0
        self.y = 0
        self.r = 5  # 반지름
        self.dx = 0
        self.dy = 0
        self.speed = 0
        self.max_speed = 7  # 공 최고속도
        self.color = 7
        self.can_move = False  # 공의 움직임 여부
        self.get_item = False  # 공이 아이템에 닿았을 때 여부
        self.player = 1  # 공을 친 사람을 구분하는 변수(아이템 사용자

    def initialize(self, x, y, r=5, color=7, speed=6, angle=-1):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.speed = speed

        angle = angle if angle >= 0 else random.randint(300, 420)
        self.dx = math.cos(math.radians(angle))
        self.dy = math.sin(math.radians(angle))
        self.can_move = True

    # 공이 아이템에 닿았을 때 실행
    def get_item(self, player):
        pass

    #  누군가 득점을 했을 때 실행
    def get_point(self, player):
        if player == 1:
            self.game.player.score += 1
        else:
            self.game.enemy.score += 1


class Bar:

    def __init__(self, game):
        self.game = game
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.color = 7

    def initialize(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def move(self):
        # 마우스 커서 따라다니기
        self.y = pyxel.mouse_y
        # 바가 화면에서 벗어나지 않도록 좌표 제한
        if self.y - self.height < 0:
            self.y = self.height
        if self.y + self.height > 360:
            self.y = 360 - self.height

    def collide(self):
        pass


class enemy_bar(Bar):

    def __init__(self, game):
        super().__init__(game)
        self.speed = 0

    def initialize(self, x, y, width, height, speed=5):
        super().initialize(x, y, width, height)
        self.speed = speed

    def move(self):
        if self.y > self.game.balls[0].y:
            self.y -= self.speed
        else:
            self.y += self.speed


class Item:

    def __init__(self, game):
        self.game = game

        pass

    def speed_ball(self):
        pass

    def fake_ball(self):
        pass

    def triple_ball(self):
        pass

    def yunepyoi(self):
        pass


class Player:
    def __init__(self, game):
        self.game = game
        self.score = 0

    def initialize(self):
        self.score = 0


class Game:

    def __init__(self):
        # 화면 크기
        pyxel.init(480, 360)

        # 초기화 파트
        self.player = Player(self)
        self.player.initialize()

        self.enemy = Player(self)
        self.enemy.initialize()

        self.bar = Bar(self)
        self.bar.initialize(50, 201, 6, 20)

        self.enemy_bar = enemy_bar(self)
        self.enemy_bar.initialize(430, 201, 6, 40, 3)

        self.balls = [Ball(self)]
        self.balls[0].initialize(250, self.bar.y, 5, 7, 10, -1)
        new_ball = Ball(self)
        new_ball.initialize(250, self.bar.y, 5, 7, 10, -1)
        self.balls.append(new_ball)

        # 플레이어가 클릭하면 True로 변경
        self.started = False

        # 컴퓨터가 특정 점수에 도달하면 활성화
        self.lose = False

        # 플레이어가 특정 점수에 도달하면 활성화
        self.win = False

        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.started and pyxel.btnp(pyxel.KEY_SPACE):
            self.started = True

        self.bar.move()
        self.enemy_bar.move()
        self.ball_move()

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.bar.x - self.bar.width, self.bar.y - self.bar.height, self.bar.width * 2, self.bar.height * 2,
                   self.bar.color)
        pyxel.rect(self.enemy_bar.x - self.enemy_bar.width, self.enemy_bar.y - self.enemy_bar.height,
                   self.enemy_bar.width * 2,
                   self.enemy_bar.height * 2, self.enemy_bar.color)
        for ball in self.balls:
            pyxel.circ(ball.x, ball.y, ball.r, ball.color)

        pyxel.text(85, 315, f'{self.balls[0].x}', 7)
        pyxel.text(85, 335, f'{self.balls[0].y}', 7)
        pyxel.text(170, 315, f'{self.player.score}', 7)
        pyxel.text(170, 335, f'{self.enemy.score}', 7)

        if not self.started:
            pyxel.text(85, 215, 'Press SPACE to Start', 7)

    def ball_move(self):
        for ball in self.balls:
            if ball.can_move:
                if self.started:
                    # 공이 상하 벽에 충돌할 경우
                    if ball.y - ball.r < 0:
                        ball.dy = abs(ball.dy)
                    if ball.y + ball.r > 360:
                        ball.dy = -abs(ball.dy)
                    # 공이 오른쪽 경계에 충돌할 경우
                    if ball.x + ball.r > 480:
                        ball.dx = -abs(ball.dx)
                        ball.get_point(1)
                    # 공이 왼쪽 경계에 충돌할 경우
                    if ball.x - ball.r < 0:
                        ball.dx = abs(ball.dx)
                        ball.get_point(2)
                    # 공이 플레이어 바에 충돌할 경우
                    if 45 < ball.x + ball.r < 60:
                        if self.bar.y - self.bar.height - ball.r < ball.y < self.bar.y + self.bar.height + ball.r:
                            # 공이 닿은 패드의 위치에 따라 튕기는 각도가 변함
                            ratio = (ball.y - (self.bar.y - self.bar.height)) / (2 * self.bar.height)
                            angle = int(300 + 120 * ratio)
                            ball.dx = math.cos(math.radians(angle))
                            ball.dy = math.sin(math.radians(angle))
                            ball.dx = abs(ball.dx)
                    # 공이 적 바에 충돌할 경우
                    if 435 > ball.x + ball.r > 420:
                        if self.enemy_bar.y - self.enemy_bar.height - ball.r < ball.y < self.enemy_bar.y + self.enemy_bar.height + ball.r:
                            ball.dx = -abs(ball.dx)
                    # 공 이동
                    ball.x += ball.dx * ball.speed
                    ball.y += ball.dy * ball.speed
                else:
                    ball.x = self.bar.x + self.bar.width + ball.r
                    ball.y = self.bar.y


Game()
