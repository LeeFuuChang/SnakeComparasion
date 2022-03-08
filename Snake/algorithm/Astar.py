from queue import PriorityQueue


def Astar_H(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)


def Find_Astar_Path(grid, obs, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.__setattr__("hash", set([start]))
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node:float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node:float("inf") for row in grid for node in row}
    f_score[start] = Astar_H(start.get_pos(), end.get_pos())

    while(not open_set.empty()):
        now = open_set.get()[2]
        open_set.hash.remove(now)

        if now == end:
            path = []
            while(now in came_from):
                path.insert(0, now)
                now = came_from[now]
            return path

        for neighbor in now.neighbors:
            if neighbor in obs:
                if not came_from.get(neighbor, False): continue
                steps = 0
                this = neighbor
                while(this in came_from):
                    steps += 1
                    this = came_from[this]
                if neighbor in obs[:-steps-1]: 
                    continue
            temp_g_score = g_score[now] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = now
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + Astar_H(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set.hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set.hash.add(neighbor)
    return False