import multiprocessing
work_load = [["huhu", "hehe"], ["huhu", "huhu"],["huhu", "haha"],["huhu", "hoho"],["huhu", "hihi"],]

def worker(procnum):
    return procnum[0] + procnum[1]

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes = 3)
    print(pool.map(worker, work_load))
