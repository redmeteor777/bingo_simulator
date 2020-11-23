import random
import copy
import collections
import matplotlib.pyplot as plt

class BingoSimulator():

    # 試行回数(変更可)
    STEPS = 1000000

    # 定数
    B_LIST = list(range(1,16))
    I_LIST = list(range(16,31))
    N_LIST = list(range(31,46))
    G_LIST = list(range(46,61))
    O_LIST = list(range(61,76))
    BALLS = list(range(1,76))

    PIPE = " | "
    LINE = "----------------------------"

    # BINGO達成までの積先回数を格納するリスト
    times_to_bingo_list = []
   
    def print_card(self):
        """BINGOカード出力用関数"""
        print(self.LINE)
        for i in range(5):
            print(self.PIPE + '{:>2}'.format(self.card[0][i]) + self.PIPE +\
                str(self.card[1][i]) + self.PIPE + str(self.card[2][i]) +\
                self.PIPE + str(self.card[3][i]) + self.PIPE + str(self.card[4][i]) + self.PIPE)
            print(self.LINE)

    def simulator(self):
        """1ゲーム単位のシミュレートを行う関数"""
    
        # 1-75番までのボールをセット
        tmp_balls = copy.deepcopy(self.BALLS)

        # 各縦列に入る値をランダムに5個取得
        self.card = [
            random.sample(self.B_LIST, 5),
            random.sample(self.I_LIST, 5),
            random.sample(self.N_LIST, 5),
            random.sample(self.G_LIST, 5),
            random.sample(self.O_LIST, 5),
        ]

        # 真ん中をフリーに置換
        self.card[2][2] = " F"

        # 取り出し済みボールのリスト
        self.popped_list = []
        
        # 穴が開いた座標を格納するリスト(初期値はフリー部分)
        self.punched_pos_list = [(2, 2)]

        # BINGO達成するまで処理をループ
        while len(tmp_balls) > 1:

            # ボールを1個取り出し
            pop_num = tmp_balls.pop(random.randint(0, len(tmp_balls)-1))

            # ボールに書かれた番号がカード内に存在するか確認
            for i in range(len(self.card)):
                if pop_num in self.card[i]:
                    # 存在した場合は座標を取得して穴開け
                    self.punched_pos_list.append((i, self.card[i].index(pop_num)))
            
            # 取り出したボールを取り出し済みのリストに格納
            self.popped_list.append(pop_num)

            # BINGO達成確認
            if self.judge_bingo() == True:
                break

        # BINGO達成していたら、取り出したボールの数をリストに格納して記録する
        self.times_to_bingo_list.append(len(self.popped_list))
    
    def judge_bingo(self):
        """BINGO達成判定を行う関数"""

        # n行目BINGO判定
        for i in range(5):
            if (i, 0) in self.punched_pos_list and\
                    (i, 1) in self.punched_pos_list and\
                    (i, 2) in self.punched_pos_list and\
                    (i, 3) in self.punched_pos_list and\
                    (i, 4) in self.punched_pos_list:
                return True
        
        # n列目BINGO判定
        for i in range(5):
            if (0, i) in self.punched_pos_list and\
                    (1, i) in self.punched_pos_list and\
                    (2, i) in self.punched_pos_list and\
                    (3, i) in self.punched_pos_list and\
                    (4, i) in self.punched_pos_list:
                return True
        
        # ナナメBINGO判定-1
        if (0, 0) in self.punched_pos_list and\
                (1, 1) in self.punched_pos_list and\
                (2, 2) in self.punched_pos_list and\
                (3, 3) in self.punched_pos_list and\
                (4, 4) in self.punched_pos_list:
            return True

        # ナナメBINGO判定-2
        if (0, 4) in self.punched_pos_list and\
                (1, 3) in self.punched_pos_list and\
                (2, 2) in self.punched_pos_list and\
                (3, 1) in self.punched_pos_list and\
                (4, 0) in self.punched_pos_list:
            return True
        
        return False

    def simulator_main(self):
        """ループ処理と結果出力を行う関数"""
        for i in range(self.STEPS):
            self.simulator()

        # 結果を取り出し
        collect = collections.Counter(self.times_to_bingo_list)

        print(collect)

        # 取り出した結果をkey順に並べ替え
        result = sorted(collect.items())

        times_list = []
        count_list = []

        # key順に並べ替えた結果をリストに格納
        for i in result:
            times_list.append(i[0])
            count_list.append(i[1])
        
        # グラフ表示
        plt.plot(times_list, count_list)
        plt.show()


def main():
    """メイン関数"""
    bingo_obj = BingoSimulator()
    bingo_obj.simulator_main()


if __name__ == "__main__":
    main()