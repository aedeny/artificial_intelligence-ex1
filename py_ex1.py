import sys
from collections import deque


class Node:
    def __init__(self, state, operator=None, parent=None):
        self.state = state
        self.operator = operator
        self.children = []
        self.parent = parent

    def state_string(self):
        return ''.join(str(x) for x in self.state)


class TilePuzzle:
    def __init__(self, input_file):
        self.algorithm_num, self.size, self.root = self.parse_file(input_file)
        self.algorithms = {1: self._ids, 2: self._bfs, 3: self._a_star}
        self.goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    def print_board(self):
        for i in range(0, self.size * self.size, self.size):
            print(self.root.state[i:i + self.size])

    def _successors(self, node):
        successors = []
        last_operator = node.operator
        z = node.state.index(0)
        length = self.size ** 2

        # Up
        if z + self.size < length and last_operator != 'D':
            state_copy = list(node.state)
            state_copy[z], state_copy[z + self.size] = state_copy[z + self.size], state_copy[z]
            successors.append(Node(state_copy, 'U', node))

        # Down
        if z - self.size >= 0 and last_operator != 'U':
            state_copy = list(node.state)
            state_copy[z], state_copy[z - self.size] = state_copy[z - self.size], state_copy[z]
            successors.append(Node(state_copy, 'D', node))

        # Left
        if z % self.size + 1 < self.size and last_operator != 'R':
            state_copy = list(node.state)
            state_copy[z], state_copy[z + 1] = state_copy[z + 1], state_copy[z]
            successors.append(Node(state_copy, 'L', node))

        # Right
        if z % self.size - 1 >= 0 and last_operator != 'L':
            state_copy = list(node.state)
            state_copy[z], state_copy[z - 1] = state_copy[z - 1], state_copy[z]
            successors.append(Node(state_copy, 'R', node))

        return successors

    def get_path_from_root(self, node):
        path = []
        current = node
        while current is not self.root:
            path.append(current.operator)
            current = current.parent
        path.reverse()
        return path

    @staticmethod
    def parse_file(input_file):
        with open(input_file, 'r') as f:
            lines = f.readlines()

        algorithm = int(lines[0])
        size = int(lines[1])
        initial_state = Node([int(x) for x in lines[2].split('-')])

        return algorithm, size, initial_state

    def solve(self):
        if self.algorithm_num in self.algorithms:
            return self.algorithms[self.algorithm_num]()
        else:
            raise Exception("An algorithm with number " + str(self.algorithm_num) + " was not found.")

    def _ids(self):
        print("Solving with IDS...")
        pass

    def _bfs(self):
        print("Solving with BFS...")
        closed = set()
        opened = {self.root.state_string()}
        queue = deque([self.root])
        while queue:
            current_node = queue.popleft()
            closed.add(current_node.state_string())
            successors = self._successors(current_node)
            current_node.children = successors
            for s in successors:
                if s.state_string() not in opened or s.state_string() in closed:
                    if s.state == self.goal:
                        return self.get_path_from_root(s)
                    opened.add(s.state_string())
                    queue.append(s)
        return False

    def _a_star(self):
        print("Solving with A*...")
        pass


if __name__ == '__main__':
    t = TilePuzzle(sys.argv[1])
    t.print_board()
    print(t.solve())
