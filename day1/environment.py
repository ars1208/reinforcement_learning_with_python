# State: セルの位置を表すクラス
class State():

    def __init__(self, row=-1, column=-1):
        self.row = row
        self.column = column

    def __repr__(self):
        return "<State: [{}, {}]>".format(self.row, self.column)

    def clone(self):
        return State(self.row, self.column)

    def __hash__(self):
        return hash((self.row, self.column))

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column

# Action: 行動を表すクラス
class Action(Enum):
    UP = 1
    DOWN = -1
    LEFT = 2
    RIGHT = -2

# Environment: 環境の実体を表すクラス
# environmentは迷路の定義(grid)を受け取り、迷路内のセルを状態とする(states)。
class Environment():

    def __init__(self, grid, move_prob=0.8):
        # gridは2次元の配列。それらのvalueは属性として扱う
        # 属性の種類は以下の通り
        # 0: 普通のセル
        # -1: damage cell(赤いセル：ゲーム終了)
        # 1: reward cell(緑のセル：ゲーム終了)
        # 9: block cell(黒いセル：移動できないブロック)
        self.grid = grid
        self.agent_state = State()
        # 報酬の初期値はマイナスの値。
        self.default_reward = -0.04
        # エージェントは遷移確率によって選択された動きができる
        #
        self.move_prob = move_prob
        self.reset()

    @property
    def row_length(self):
        return len(self.grid)

    @property
    def column_length(self):
        return len(self.grid[0])

    @property
    def actions(self):
        return [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]

    @property
    def states(self):
        states = list()
        for row in range(self.row_length):
            for column in range(self.column_length):
                # block cellはstateに含まれない
                if self.grid[row][column] != 9:
                    states.append(State(row, column))
        return states

    def transit_func(self, state, action):
        transition_probs = dict()
        if not self.can_action_at(state):
            return transition_probs

        opposite_direction = Action(action.value * -1)

        for a in self.actions:
            prob = 0
            if a == action:
                prob = self.move_prob
            elif a != opposite_direction:
                prob = (1 - self.move_prob) / 2

            next_state = self._move(state, a)
            if next_state not in transition_probs:
                transition_probs[next_state] = prob
            else:
                transition_probs[next_state] += prob

        return transition_probs

    def can_action_at(self, state):
        if self.grid[state.row][state.column] == 0:
            return True
        else:
            return False

    def _move(self, state, action):
        if not self.can_action_at(state):
            raise Exception("Can't move from here!")

        next_state = state.clone()

        # アクションの実行
        if action == Action.UP:
            next_state.row -= 1
        elif action == Action.DOWN:
            next_state.row += 1
        elif action == Action.LEFT:
            next_state -= 1
        elif action == Action.RIGHT:
            next_state += 1

        
