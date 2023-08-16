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
        self.max_speed = 15  # 공 최고속도
        self.color = 7
        self.time = 0
        self.item = False
        self.fake = False
        self.can_move = False  # 공의 움직임 여부
        self.player = 'player'  # 공을 친 사람을 구분하는 변수(아이템 사용자)

    def initialize(self, x, y, r=5, color=7, speed=10, angle=-1):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.speed = speed

        if not angle >= 0:
            if self.player == 'player':
                angle = random.randint(300, 420)
            elif self.player == 'enemy':
                angle = random.randint(120, 240)

        self.dx = math.cos(math.radians(angle))
        self.dy = math.sin(math.radians(angle))
        self.can_move = True

    def move(self):
        if self.can_move:
            if self.game.started:
                if self.time == 0:
                    # 공이 상하 벽에 충돌할 경우
                    if self.y - self.r < 0:
                        self.dy = abs(self.dy)
                    if self.y + self.r > 360:
                        self.dy = -abs(self.dy)
                    # 공이 왼쪽/오른쪽 경계에 충돌할 경우 포인트 획득, 공 중앙 이동&각도 초기화
                    if self.x + self.r > 480 or self.x - self.r < 0:
                        self.get_point()
                        if not self.item:
                            self.ori_location()
                    # 공이 플레이어 바에 충돌할 경우
                    if 45 < self.x + self.r < 65:
                        if self.game.bar.y - self.game.bar.height - self.r < self.y < self.game.bar.y \
                                + self.game.bar.height + self.r:
                            # 공이 닿은 패드의 위치에 따라 튕기는 각도가 변함
                            ratio = (self.y - (self.game.bar.y - self.game.bar.height)) / (2 * self.game.bar.height)
                            angle = int(300 + 120 * ratio)
                            self.dx = math.cos(math.radians(angle))
                            self.dy = math.sin(math.radians(angle))
                            self.dx = abs(self.dx)
                            # 플레이어 변경, 아이템 생성 시도, 아이템 공 제거
                            if not self.item:
                                self.game.item.create_item()
                                self.change_player('player')
                            else:
                                self.game.balls.remove(self)
                    # 공이 적 바에 충돌할 경우
                    if 440 > self.x + self.r > 420:
                        if self.game.enemy_bar.y - self.game.enemy_bar.height - self.r < self.y < self.game.enemy_bar.y \
                                + self.game.enemy_bar.height + self.r:
                            self.dx = -abs(self.dx)
                            # 플레이어 변경, 아이템 생성 시도, 아이템 공 제거
                            if not self.item:
                                self.game.item.create_item()
                                self.change_player('enemy')
                            else:
                                self.game.balls.remove(self)
                    # 공 이동
                    self.x += self.dx * self.speed
                    self.y += self.dy * self.speed
                else:
                    self.time -= 1
            else:
                self.x = self.game.bar.x + self.game.bar.width + self.r + 5
                self.y = self.game.bar.y

    #  누군가 득점을 했을 때 실행
    def get_point(self):
        if not self.fake:
            if self.player == 'player':
                self.game.player.score += 1
            elif self.player == 'enemy':
                self.game.enemy.score += 1

        if self.item:
            self.game.balls.remove(self)

    def ori_location(self):
        self.x = 240
        self.y = 180
        self.time = 30
        angle = 0

        if self.player == 'player':
            angle = random.randint(120, 240)
            self.change_player('enemy')
        elif self.player == 'enemy':
            angle = random.randint(300, 420)
            self.change_player('player')

        self.dx = math.cos(math.radians(angle))
        self.dy = math.sin(math.radians(angle))

    def change_player(self, player):
        self.player = player


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


class enemy_bar(Bar):

    def __init__(self, game):
        super().__init__(game)
        self.speed = 0
        self.near_ball_x = 0
        self.near_ball_y = 0

    def initialize(self, x, y, width, height, speed=5):
        super().initialize(x, y, width, height)
        self.speed = speed

    def move(self):
        if self.y > self.near_ball_y:
            if self.speed > self.y - self.near_ball_y:
                self.y = self.near_ball_y
            else:
                self.y -= self.speed
        else:
            if self.speed > self.near_ball_y - self.y:
                self.y = self.near_ball_y
            else:
                self.y += self.speed
        self.near_ball_x = 0


class Item:

    def __init__(self, game):
        self.game = game
        self.x = 0
        self.y = 0
        self.r = 20
        self.type = 0
        self.color = 0
        self.use_count = 0
        self.time = 0
        self.player = 'player'  # 아이템 획득한 사람을 구별
        self.existence = False
        self.active = False

    def create_item(self):
        if not self.existence:
            if not self.active:
                # 아이템 등장 확률 설정
                if random.randint(1, 3) == 1:
                    self.existence = True
                    # 아이템 좌표 랜덤 선택
                    self.x = random.randint(150, 330)
                    self.y = random.randint(50, 310)
                    # 아이템 종류 랜덤 선택
                    self.type = random.randint(1, 3)
                    if self.type == 1:  # 트리플
                        self.color = 8
                    elif self.type == 2:  # 스피드
                        self.color = 9
                    elif self.type == 3:  # 페이크
                        self.color = 10

    def detect_collision(self, ball: Ball):
        if self.game.started:
            if self.existence:
                if not ball.item:
                    if (self.x - self.r - ball.r < ball.x < self.x + self.r + ball.r) and \
                            (self.y - self.r - ball.r < ball.y < self.y + self.r + ball.r):
                        self.active = True
                        self.existence = False
                        self.player = ball.player
                        self.time = pyxel.frame_count

    def speed_ball(self, ball: Ball):
        if (pyxel.frame_count - self.time) == 300:
            ball.speed = 10
            self.active = False
        else:
            if self.player == 'player':
                if ball.player == 'player':
                    ball.speed = ball.max_speed
                else:
                    ball.speed = 10
            else:
                if ball.player == 'player':
                    ball.speed = 10
                else:
                    ball.speed = ball.max_speed

    def fake_ball(self, ball: Ball):
        if (pyxel.frame_count - self.time) % 60 == 0:
            if self.use_count == 3:
                self.use_count = 0
                self.active = False
            else:
                self.use_count += 1
                for i in range(0, 40):
                    new_ball = Ball(self.game)
                    if i >= 20:
                        new_ball.player = 'enemy'
                    new_ball.initialize(ball.x, ball.y, random.randint(3, 8), 10, random.randint(5, 15))
                    new_ball.item = True
                    new_ball.fake = True
                    self.game.balls.append(new_ball)

    def triple_ball(self, ball: Ball):
        ball.can_move = False
        if (pyxel.frame_count - self.time) % 30 == 0:
            if self.use_count == 3:
                self.use_count = 0
                ball.can_move = True
                self.active = False
            else:
                self.use_count += 1
                # 아이템 공 추가
                new_ball = Ball(self.game)
                if ball.player == 'enemy':
                    new_ball.player = 'enemy'
                new_ball.initialize(ball.x, ball.y, 5, 8, 10)
                new_ball.item = True
                self.game.balls.append(new_ball)

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
        self.enemy_bar.initialize(430, 201, 6, 40, 5)

        self.item = Item(self)

        self.balls = [Ball(self)]
        self.balls[0].initialize(250, self.bar.y, 5, 7, 10, -1)

        # 메인 화면 난이도 선택
        self.main_started = 1

        # 플레이어가 클릭하면 True로 변경
        self.started = False

        # 게임이 끝났을 때 활성화
        self.game_over = False

        # 승리 점수
        self.win_score = 3

        # 플레이어가 특정 점수에 도달하면 활성화
        self.win = False

        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.started:
            self.difficult_select()
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.started = True

        if not self.game_over:
            self.bar.move()
            for ball in self.balls:
                if not ball.fake:
                    if ball.x >= self.enemy_bar.near_ball_x:
                        self.enemy_bar.near_ball_x = ball.x
                        self.enemy_bar.near_ball_y = ball.y
            self.enemy_bar.move()

            for ball in self.balls:
                ball.move()
                self.item.detect_collision(ball)
                if self.item.active:
                    if not ball.item:
                        if self.item.type == 1:
                            self.item.triple_ball(ball)
                        elif self.item.type == 2:
                            self.item.speed_ball(ball)
                        elif self.item.type == 3:
                            self.item.fake_ball(ball)

        if self.player.score == self.win_score or self.enemy.score == self.win_score:
            self.game_over = True
            self.started = False
            if self.player.score == self.win_score:
                self.win = True

    def draw(self):
        pyxel.cls(0)
        if not self.game_over:
            pyxel.rect(self.bar.x - self.bar.width, self.bar.y - self.bar.height, self.bar.width * 2,
                       self.bar.height * 2,
                       self.bar.color)
            pyxel.rect(self.enemy_bar.x - self.enemy_bar.width, self.enemy_bar.y - self.enemy_bar.height,
                       self.enemy_bar.width * 2, self.enemy_bar.height * 2, self.enemy_bar.color)
            for ball in self.balls:
                pyxel.circ(ball.x, ball.y, ball.r, ball.color)

            if not self.started:
                pyxel.text(195, 190, 'hard mode', 7 if self.main_started != 3 else 10)
                pyxel.text(195, 200, 'normal mode', 7 if self.main_started != 2 else 10)
                pyxel.text(195, 210, 'easy mode', 7 if self.main_started != 1 else 10)
                pyxel.text(195, 180, 'Press SPACE to Start', 7)
            else:
                if self.item.existence:
                    pyxel.circ(self.item.x, self.item.y, self.item.r, self.item.color)

                pyxel.text(205, 20, f'{self.player.score}', 15)
                pyxel.text(265, 20, f'{self.enemy.score}', 15)
                pyxel.text(233, 20, f'{int(pyxel.frame_count / 30)}', 7)
                if self.item.active:
                    if self.item.type == 1:
                        pyxel.text(233, 35, f'{90 - (pyxel.frame_count - self.item.time)}', 5)
                    elif self.item.type == 2:
                        pyxel.text(233, 35, f'{300 - (pyxel.frame_count - self.item.time)}', 5)
                    elif self.item.type == 3:
                        pyxel.text(233, 35, f'{180 - (pyxel.frame_count - self.item.time)}', 5)
        else:
            if self.win:
                pyxel.text(215, 180, 'You Win', 7)
            else:
                pyxel.text(215, 180, 'You Lose', 7)

    def difficult_select(self):

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.enemy_bar.speed = self.main_started * 3
        else:
            if pyxel.btnp(pyxel.KEY_UP):
                self.main_started += 1
            elif pyxel.btnp(pyxel.KEY_DOWN):
                self.main_started -= 1

            if self.main_started > 3:
                self.main_started = 1
            elif self.main_started < 1:
                self.main_started = 3


Game()
