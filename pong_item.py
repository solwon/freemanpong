import pyxel
import math
import random


# 공 제어를 위한 Ball 클래스
class Ball:

    def __init__(self, game, player):
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
        self.player = player  # 공을 친 사람을 구분하는 변수(아이템 사용자

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

    # 공의 이동 및 반사를 제어하는 함수
    def move(self):
        if self.can_move:
            if self.game.started:
                # 공이 상하 벽에 부딪힐 때(반지름을 포함해 공이 화면 밖에 걸치지 않도록 함)
                if self.y - self.r < 0:
                    self.dy = abs(self.dy)
                if self.y + self.r > 360:
                    self.dy = -abs(self.dy)
                # 공이 오른쪽 경계에 부딪힐 경우
                if self.x + self.r > 480:
                    self.dx = -abs(self.dx)
                    self.get_point(1)
                # 공이 왼쪽 경계에 부딪힐 경우
                if self.x - self.r < 0:
                    self.dx = abs(self.dx)
                    self.get_point(2)
                # 공이 플레이어 바에 걸칠 경우
                if self.x + self.r < 60:
                    if self.game.Bar.y - self.game.Bar.height - self.r < self.y < self.game.Bar.y + self.game.Bar.height + self.r:
                        # 공이 닿은 패드의 위치에 따라 튕기는 각도가 변함
                        ratio = (self.y - (self.game.Bar.y - self.game.Bar.height)) / (2 * self.game.Bar.height)
                        angle = int(300 + 120 * ratio)
                        self.dx = math.cos(math.radians(angle))
                        self.dy = math.sin(math.radians(angle))
                        self.dx = abs(self.dx)
                # 공이 AI 바에 걸칠 경우
                if self.x + self.r > 420:
                    if self.game.enemyBar.y - self.game.enemyBar.height - self.r < self.y < self.game.enemyBar.y + self.game.enemyBar.height + self.r:
                        # 공이 닿은 패드의 위치에 따라 튕기는 각도가 변함
                        self.dx = -abs(self.dx)
            # 공 이동
                self.x += self.dx * self.speed
                self.y += self.dy * self.speed
            else:
                self.x = self.game.Bar.x + self.game.Bar.width + self.r
                self.y = self.game.Bar.y

    # 공이 아이템에 닿았을 때 실행
    def get_item(self, player):
        pass

    #  누군가 득점을 했을 때 실행
    def get_point(self, player):
        pass


class Bar:

    def __init__(self, game, player):
        self.game = game
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.color = 7
        self.player = player
        self.ai_speed = 5

    def initialize(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def move(self):
        if self.player == 1:
            # 마우스 커서 따라다니기
            self.y = pyxel.mouse_y
            # 바가 화면에서 벗어나지 않도록 좌표 제한
            if self.y - self.height < 0:
                self.y = self.height
            if self.y + self.height > 360:
                self.y = 360 - self.height

        if self.player == 2:
            self.y += self.ai_speed
            if self.y - self.height < 0:
                self.ai_speed = 5
            if self.y + self.height > 360:
                self.ai_speed = -5

    def collide(self):
        pass


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

        self.Bar = Bar(self, 1)
        self.Bar.initialize(50, 201, 6, 20)

        self.enemyBar = Bar(self, 2)
        self.enemyBar.initialize(430, 201, 6, 100)

        self.Ball = Ball(self, 1)
        self.Ball.initialize(250, 250, 5, 7, 10, -1)

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

        self.Bar.move()
        self.enemyBar.move()
        self.Ball.move()

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.Bar.x - self.Bar.width, self.Bar.y - self.Bar.height, self.Bar.width * 2, self.Bar.height * 2,
                   self.Bar.color)
        pyxel.rect(self.enemyBar.x - self.enemyBar.width, self.enemyBar.y - self.enemyBar.height, self.enemyBar.width * 2,
                   self.enemyBar.height * 2, self.enemyBar.color)
        pyxel.circ(self.Ball.x, self.Ball.y, self.Ball.r, self.Ball.color)

        pyxel.text(85, 315, f'{self.Ball.x}', 7)
        pyxel.text(85, 335, f'{self.Ball.y}', 7)

        if not self.started:
            pyxel.text(85, 215, 'Press SPACE to Start', 7)

Game()
