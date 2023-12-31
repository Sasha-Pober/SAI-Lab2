import random
import time
import psutil

N = 8

generated_nodes_ids = 0
generated_nodes_astar = 0

#goal = [1,3,5,7,2,0,6,4]

init_state = [5,3,5,7,2,1,6,4]

list = [0] * N

def initialize_state():
    return init_state
    # for i in range(N):
    #     list[i] = random.randint(0,N-1)
    # return list

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

    global generated_nodes_ids
    successors_states = successors(board)
    generated_nodes_ids += len(successors_states)
    for successor in successors_states:
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

    # print(len(successors))
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
        global generated_nodes_astar
        successors_states = successors(state)
        generated_nodes_astar += len(successors_states)
        for s in successors_states:
            if tuple(s) not in explored:
                frontier.append((heuristic(s) + len(explored), s))


    return None


state = initialize_state()
print('Початкові значення:', state)

print('IDS algorithm:')
start = time.perf_counter()
memory_before = psutil.virtual_memory().used /(1024)
result = ids(state)
memory_after = psutil.virtual_memory().used /(1024)
end = time.perf_counter()
if result is not None:
    print("Розв'язок знайдено:", result)
else:
    print("Розв'язок не знайдено.")

print('time:', end - start)
print('States generated:', generated_nodes_ids)
print(f'Memory used: {abs(memory_after - memory_before)} KB')

print('\nA* algorithm:')
start = time.perf_counter()
memory_before = psutil.virtual_memory().used /(1024*1024)
result = astar(state)
memory_after = psutil.virtual_memory().used /(1024*1024)
end = time.perf_counter()
if result is not None:
    print("Розв'язок знайдено:", result)
else:
    print("Розв'язок не знайдено.")

print('time:', end - start)
print('States generated:', generated_nodes_astar)
print(f'Memory used: {abs(memory_after - memory_before)} KB')





