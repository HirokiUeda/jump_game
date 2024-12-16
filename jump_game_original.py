import pyxel

class App:
    def __init__(self):
        # 画面サイズ設定
        pyxel.init(160, 120, title="Jump Game")
        # アセット読み込み
        pyxel.load("assets/jump_game_original.pyxres")

        # 初期値設定
        self.reset()

        # 障害物の位置、状態をリスト管理
        # x座標が0, 120の間隔で障害物を2つ作成
        self.floor = [(i * 120, pyxel.rndi(8, 104), True) for i in range(2)]

        # コインの位置、状態をリスト管理
        # x座標が0、80、160の間隔でコインを3つ作成
        self.coin = [(i * 80, pyxel.rndi(0, 104), True) for i in range(3)]

        # アプリ開始
        pyxel.run(self.update, self.draw)

    def update(self):
        # Qキーを押したらPyxelアプリ終了
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Playerの更新
        self.update_player()

        # 障害物の更新
        # enumerate関数でi:インデックス番号、v:要素を取得
        # *vはタプル（x,y,is_alive）展開
        for i, v in enumerate(self.floor):
            self.floor[i] = self.update_floor(*v)

        # コインの更新
        for i, v in enumerate(self.coin):
            self.coin[i] = self.update_coin(*v)

    def draw(self):
        # 背景色指定
        pyxel.cls(12)

        # Playerの描画
        pyxel.blt(self.player_x, self.player_y, 0, 0, 0, 16, 16, 12)

        # 障害物の描画
        for x, y, is_alive in self.floor:
            pyxel.blt(x, y, 0, 0, 16, 16, 16, 12)

        # コインの描画
        for x, y, is_alive in self.coin:
            if is_alive:
                pyxel.blt(x, y, 0, 16, 16, 16, 16, 12)

        # スコアの描画
        score = f"SCORE:{self.score:>4}"
        pyxel.text(5, 4, score, 1)
        pyxel.text(4, 4, score, 7)

    # Playerの更新
    def update_player(self):
        # 左右移動
        if pyxel.btn(pyxel.KEY_LEFT):
            # 画面左端が移動限界
            self.player_x = max(self.player_x - 2, 0)
        if pyxel.btn(pyxel.KEY_RIGHT):
            # 画面右端が移動限界
            self.player_x = min(self.player_x + 2, pyxel.width - 16)

        # ジャンプ移動
        if pyxel.btnp(pyxel.KEY_SPACE) and self.is_alive:
            self.player_dy = -2

        # 重力設定
        self.player_y += self.player_dy
        self.player_dy = min(self.player_dy + 0.1, 8)

        if self.player_y < 0:
            self.player_y = 0

        # Playerが画面の下に落下したら
        if self.player_y > pyxel.height:
            # Playerの状態が有効だったら無効になる
            if self.is_alive:
                self.is_alive = False
            # Playerがさらに深く落下したらすべて初期値にリセット
            if self.player_y > 600:
                self.reset()

    # 障害物の更新
    def update_floor(self, x, y, is_alive):
        # 障害物が有効
        if is_alive and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:
            # Playerを無効化
            self.is_alive = False
            self.player_dy = 5

        # 足場を左側へ移動
        x -= 2

        # 画面外へ移動したら右端へリセット
        if x < -40:
            x += 240
            y = pyxel.rndi(8, 104)
            is_alive = True
        return x, y, is_alive

    # コインの更新
    def update_coin(self, x, y, is_alive):
        if is_alive and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:
            # coinを無効化
            is_alive = False
            # 得点を加算
            self.score += 100

        # 移動
        x -= 2

        # 左端まで移動したら右端へ移動
        if x < -40:
            x += 240
            y = pyxel.rndi(0, 104)
            is_alive = True
        return x, y, is_alive

    # 初期値設定
    def reset(self):
        # スコアの初期値
        self.score = 0

        # Playerの初期位置
        self.player_x = 20
        self.player_y = 64

        # Playerのジャンプ力
        self.player_dy = 0

        # Playerの状態
        self.is_alive = True




App()
