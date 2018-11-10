import sys
from collections import deque


class Node:
    def __init__(self, state, depth, operator=None, parent=None):
        self.state = state
        self.operator = operator
        self.children = []
        self.parent = parent
        self.depth = depth

    def state_string(self):
        return ','.join(str(x) for x in self.state)


class Algorithm:
    def __init__(self, method, name):
        self.method = method
        self.name = name


class TilePuzzle:
    def __init__(self, input_file):
        self.algorithm_num, self.size, self.root = self.parse_file(input_file)
        self.algorithms = {1: Algorithm(self._ids, 'IDS'), 2: Algorithm(self._bfs, 'BFS'),
                           3: Algorithm(self._a_star, 'A*')}
        self.goal = [x for x in range(1, self.size ** 2)]
        self.goal.append(0)

    def print_board(self):
        for i in range(0, self.size * self.size, self.size):
            print(self.root.state[i:i + self.size])

    def _successors(self, node):
        successors = []
        last_operator = 'G'  # node.operator
        z = node.state.index(0)
        length = self.size ** 2

        # Up
        if z + self.size < length and last_operator != 'D':
            state_copy = list(node.state)
            state_copy[z], state_copy[z + self.size] = state_copy[z + self.size], state_copy[z]
            successors.append(Node(state_copy, node.depth + 1, 'U', node))

        # Down
        if z - self.size >= 0 and last_operator != 'U':
            state_copy = list(node.state)
            state_copy[z], state_copy[z - self.size] = state_copy[z - self.size], state_copy[z]
            successors.append(Node(state_copy, node.depth + 1, 'D', node))

        # Left
        if z % self.size + 1 < self.size and last_operator != 'R':
            state_copy = list(node.state)
            state_copy[z], state_copy[z + 1] = state_copy[z + 1], state_copy[z]
            successors.append(Node(state_copy, node.depth + 1, 'L', node))

        # Right
        if z % self.size - 1 >= 0 and last_operator != 'L':
            state_copy = list(node.state)
            state_copy[z], state_copy[z - 1] = state_copy[z - 1], state_copy[z]
            successors.append(Node(state_copy, node.depth + 1, 'R', node))

        return successors

    def get_path_from_root(self, node):
        path = []
        current = node
        while current is not self.root:
            path.append(current.operator)
            current = current.parent
        path.reverse()
        return ''.join(path)

    @staticmethod
    def parse_file(input_file):
        with open(input_file, 'r') as f:
            lines = f.readlines()

        algorithm = int(lines[0])
        size = int(lines[1])
        initial_state = Node([int(x) for x in lines[2].split('-')], 0)

        return algorithm, size, initial_state

    def solve(self):
        if self.algorithm_num in self.algorithms:
            algorithm = self.algorithms[self.algorithm_num]
            print('Solving with ' + algorithm.name + '...')
            return algorithm.method()
        else:
            raise Exception('An algorithm with number ' + str(self.algorithm_num) + ' was not found.')

    def _ids(self):
        max_depth = 0
        while True:
            result = self._bfs(max_depth)
            if result[0]:
                return result[0], result[1], max_depth
            max_depth += 1

    def _bfs(self, max_depth=-1):
        queue = deque([self.root])
        counter = 0
        while queue:
            n = queue.popleft()
            counter += 1
            if n.state == self.goal:
                return self.get_path_from_root(n), counter, 0
            if n.depth == max_depth:
                return False, -1, -1
            successors = self._successors(n)
            queue.extend(successors)
        return False, -1, -1

    def _a_star(self):
        pass


if __name__ == '__main__':
    t = TilePuzzle(sys.argv[1])
    t.print_board()
    path, total_opened, depth = t.solve()
    result_string = path + ' ' + str(total_opened) + ' ' + str(depth)
    print(result_string)
    with open('output.txt', 'w') as f:
        f.write(result_string)
