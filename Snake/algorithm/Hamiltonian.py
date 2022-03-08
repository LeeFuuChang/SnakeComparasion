import random
def Find_Hamiltonian_Cycle(cst, ava): #cst = 固定的節點順序 / ava = 可用的節點
    """
    找出把每個節點都走一次
    並且開頭與結尾相同 (無窮迴圈路徑)
    的路徑
    """
    def recursion(tar, now, ava):
        if len(ava)==0:
            if tar in now[-1].neighbor:
                return now
            else:
                return False
        if all(node in now for node in now[-1].neighbor): return False
        neighbors = list(now[-1].neighbor)
        random.shuffle(neighbors)
        for node in neighbors:
            if node in now: continue
            n_ava = ava[:]
            n_ava.remove(node)
            result = recursion(tar, [*now, node], n_ava)
            if result: return result
        return False

    return recursion(cst[0], cst[:], ava[:])