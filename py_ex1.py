import datetime
import sys
from collections import deque


class Node:
    def __init__(self, state, operator=None, parent=None, g=float('inf'), h=float('inf')):
        self.state = state
        self.operator = operator
        self.parent = parent
        self.g = g
        self.h = h

    @property
    def f(self):
        return self.g + self.h

    def __hash__(self):
        return hash(self.state_string())

    def __eq__(self, other):
        return self.state == other.state

    def __repr__(self):
        return '<' + self.state_string() + '>'

    def __lt__(self, other):
        return self.h + self.g < other.h + other.g

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
        self.length = self.size ** 2

    def print_board(self):
        print('Initial State:')
        for i in range(0, self.size * self.size, self.size):
            print('  '.join([str(x) for x in self.root.state[i:i + self.size]]))
        print('')

    def _successors(self, node):
        successors = []
        z = node.state.index(0)

        # Up
        if z + self.size < self.length:
            state_copy = list(node.state)
            state_copy[z], state_copy[z + self.size] = state_copy[z + self.size], state_copy[z]
            successors.append(Node(state_copy, 'U', node))

        # Down
        if z - self.size >= 0:
            state_copy = list(node.state)
            state_copy[z], state_copy[z - self.size] = state_copy[z - self.size], state_copy[z]
            successors.append(Node(state_copy, 'D', node))

        # Left
        if z % self.size + 1 < self.size:
            state_copy = list(node.state)
            state_copy[z], state_copy[z + 1] = state_copy[z + 1], state_copy[z]
            successors.append(Node(state_copy, 'L', node))

        # Right
        if z % self.size - 1 >= 0:
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
        if len(path) == 0:
            return 'NOTHING'
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
            start_time = datetime.datetime.today()
            print(str(start_time) + ': Solving with ' + algorithm.name + '...')
            result = algorithm.method()
            end_time = datetime.datetime.today()
            print (str(end_time) + ': Finished in ' + str(end_time - start_time) + '.')
            return result
        else:
            raise Exception('An algorithm with number ' + str(self.algorithm_num) + ' was not found.')

    def _ids(self):
        max_depth = 0
        while True:
            found, remaining = self._dls(self.root, max_depth)
            if found:
                return self.get_path_from_root(found), remaining, max_depth + 1
            elif not remaining:
                return None
            max_depth += 1

    def _dls(self, node, depth):
        """
        Depth Limited Search
        :param node:
        :param depth:
        :return:
        """
        if depth == 0:
            if node.state == self.goal:
                return node, 0
            else:
                # Not found, but may have successors
                return None, 1

        current = 0
        for s in self._successors(node):
            found, remaining = self._dls(s, depth - 1)
            current += remaining
            if found:
                return found, current + 1
        return None, current

    def _bfs(self):
        queue = deque([self.root])
        counter = 0
        while queue:
            n = queue.popleft()
            counter += 1
            if n.state == self.goal:
                return self.get_path_from_root(n), counter, 0
            successors = self._successors(n)
            queue.extend(successors)
        return False, -1, -1

    def _array_index_to_row_col(self, i):
        """
        Calculates row and column indices.
        :param i: An index in a 1-dim array.
        :return: A 2-tuple of (row, column) of a square matrix of size self.size.
        """
        return int(i / self.size), i % self.size

    def _manhattan_distance(self, state_as_list):
        distances_sum = 0
        for current_index, n in enumerate(state_as_list):
            if n == 0:
                continue
            current_row, current_column = self._array_index_to_row_col(current_index)
            goal_row, goal_column = self._array_index_to_row_col(self.goal.index(n))
            distances_sum += abs(goal_row - current_row) + abs(goal_column - current_column)

        return distances_sum

    def _a_star(self):
        from heapq import heappush, heappop
        opened = []
        self.root.g = 0
        self.root.h = self._manhattan_distance(self.root.state)
        heappush(opened, (self.root.f, self.root))
        closed = set()

        while opened:
            n = heappop(opened)[1]

            if n.state == self.goal:
                path = self.get_path_from_root(n)
                return path, len(closed), len(path)

            if n in closed:
                continue

            for s in self._successors(n):
                s.g = n.g + 1
                s.h = self._manhattan_distance(s.state)
                heappush(opened, (s.f, s))
            closed.add(n)
        return False, len(closed), -1


if __name__ == '__main__':
    t = TilePuzzle(sys.argv[1])
    t.print_board()
    path, total_opened, depth = t.solve()
    if path:
        result_string = path + ' ' + str(total_opened) + ' ' + str(depth)

        formatted_path = path[0:4]
        for i in range(4, len(path), 4):
            formatted_path += '-' + path[i:i + 4]
        print (formatted_path)
    else:
        result_string = 'No Solution'

    print(result_string)
    with open('output.txt', 'w') as f:
        f.write(result_string)
