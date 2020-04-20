import os
import time
import threading
import multiprocessing
from base import NUM_WORKERS

FILE = open('log/game_00014.log', 'r', encoding='latin-1')

file_data = FILE.readlines()
FILE.close()
regen_data = []
for line in file_data:
    new_line = line.encode('utf-8').decode('utf-8').replace('\x00', '')
    regen_data.append(new_line)
# print(regen_data)

def count_lines():

# variables for couting elements
    kill_lines = start_lines = end_lines = pconnect_lines = tchange_lines = 0
    idate_lines = iserver_lines = igame_lines = imath_lines = imap_lines = 0
    damage_lines = gloss_lines = ggain_lines = 0

    for l in regen_data:
        if 'INFO_DATE' in l:
            idate_lines += 1
        if 'INFO_GAME' in l:
            igame_lines += 1
        if 'INFO_MATCH' in l:
            imath_lines += 1
        if 'INFO_MAP' in l:
            imap_lines += 1
        if 'INFO_SERVER' in l:
            iserver_lines += 1
        if str(l).startswith('GAME_START'):
            start_lines += 1
        if str(l).startswith('PLAYER_CONNECT'):
            pconnect_lines += 1
        if str(l).startswith('PLAYER_TEAM_CHANGE'):
            tchange_lines += 1
        if str(l).startswith('KILL'):
            kill_lines += 1
        if str(l).startswith('GOLD_EARNED'):
            ggain_lines += 1
        if str(l).startswith('GOLD_LOST'):
            gloss_lines += 1
        if str(l).startswith('DAMAGE'):
            damage_lines += 1
    print('DAMAGE:', damage_lines,'GOLD_LOST:', gloss_lines,
          'GOLD_EARNED:', ggain_lines,'KILL:', kill_lines,
          'PLAYER_CONNECT:', pconnect_lines,
          'PLAYER_TEAM_CHANGE:', tchange_lines,
          'GAME_START:', start_lines,
          'INFO_SERVER', iserver_lines)



# perform multiprocessing
## Run tasks serially
start_time = time.time()
for _ in range(NUM_WORKERS):
    count_lines()
end_time = time.time()

print("Serial time=", end_time - start_time)

# Run tasks using threads
start_time = time.time()
threads = [threading.Thread(target=count_lines) for _ in range(NUM_WORKERS)]
[thread.start() for thread in threads]
[thread.join() for thread in threads]
end_time = time.time()

print("Threads time=", end_time - start_time)

# Run tasks using processes
start_time = time.time()
processes = [multiprocessing.Process(target=count_lines()) for _ in range(NUM_WORKERS)]
[process.start() for process in processes]
[process.join() for process in processes]
end_time = time.time()

print("Parallel time=", end_time - start_time)
