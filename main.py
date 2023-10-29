from queue import PriorityQueue
import random
import time

N = 8

#goal = [1,3,5,7,2,0,6,4]

init_state = [7,3,5,7,2,7,6,4]

list = [0] * N

def initialize_state():
    # return init_state
    for i in range(N):
        list[i] = random.randint(0,N-1)
    return list

def is_goal(board):
    # Перевірка, чи досягнуто цільового стану
    for i in range(N):
        for j in range(i + 1, N):
            # Перевірка на один рядок, стовпець або діагональ
            if (board[i] == board[j]) or (abs(board[i] - board[j]) == abs(i - j)):
                return False
    return True


def ids(board):
    depth = 0
    while True:
        result = dfs(board, depth)
        if result is not None:
            return result
        depth += 1

def dfs(board, depth):
    # Перевірка, чи досягнуто максимальної глибини
    if depth == 0:
        if is_goal(board):
            return board
        return None

    for successor in successors(board):
        result = dfs(successor, depth - 1)
        if result is not None:
            return result

    return None

def successors(board):
    # Генерація наступників для даного стану
    successors = []

    for i in range(N):
        for j in range(i + 1, N):
            # Копіюємо стан та переставляємо ферзя
            if board[i] == board[j]:
                board[i] = get_empty(board)
            new_board = board[:]
            new_board[i], new_board[j] = new_board[j], new_board[i]
            successors.append(new_board)

    return successors


def get_empty(board):
    for i in range(N):
        if i not in board:
            return i
    return None


def heuristic(board):
    count = 0
    for i in range(N):
        for j in range(i + 1, N):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                count += 1
    return count

def astar(initial_state):
    frontier = [(heuristic(initial_state), initial_state)]
    explored = set()

    while frontier:
        frontier.sort()
        _, state = frontier.pop(0)

        if is_goal(state):
            return state

        explored.add(tuple(state))
        successors_states = successors(state)
        # print(len(successors_states))

        for s in successors_states:
            if tuple(s) not in explored:
                frontier.append((heuristic(s) + len(explored), s))

    return None

# print(initialize_state(init_state))
state = initialize_state()
print('Початкові значення:', state)

start = time.perf_counter()
result = ids(state)
end = time.perf_counter()
if result is not None:
    print("Розв'язок знайдено:", result)
else:
    print("Розв'язок не знайдено.")

print('time:', end - start)

start = time.perf_counter()
result = astar(state)
end = time.perf_counter()
if result is not None:
    print("Розв'язок знайдено:", result)
else:
    print("Розв'язок не знайдено.")

print('time:', end - start)


