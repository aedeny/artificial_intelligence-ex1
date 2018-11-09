import sys


class TilePuzzle:
    def __init__(self, input_file):
        self.algorithm_num, self.size, self.board = self.parse_file(input_file)
        self.algorithms = {1: self._ids, 2: self._bfs, 3: self._a_star}

    def print_board(self):
        for i in range(0, self.size * self.size, self.size):
            print(self.board[i:i + self.size])

    @staticmethod
    def parse_file(input_file):
        with open(input_file, 'r') as f:
            lines = f.readlines()
            algorithm = int(lines[0])
            size = int(lines[1])
            start_state = [int(x) for x in lines[2].split('-')]
        f.close()
        return algorithm, size, start_state

    def solve(self):
        if self.algorithm_num in self.algorithms:
            self.algorithms[self.algorithm_num]()
        else:
            raise Exception("An algorithm with number " + str(self.algorithm_num) + " was not found.")

    def _ids(self):
        print("Solving with IDS...")
        pass

    def _bfs(self):
        print("Solving with BFS...")
        pass

    def _a_star(self):
        print("Solving with A*...")
        pass


if __name__ == '__main__':
    t = TilePuzzle(sys.argv[1])
    t.print_board()
    t.solve()
