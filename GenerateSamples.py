from Env import *
from Consts import *
from datetime import datetime, timedelta
import random

file_name = BASE_WORKING_DIR + "\Whatsapp\example" + ".pickle"
time = datetime.now()
for i in range(0,15):
    status = random.choice([True, False])
    if i == 0 or i == 15:
        status = False
    duration = random.choice([60,180,120])
    seconds_list = [1, 2, 3]
    for j in range(0, duration):
        sample = (time, status)
        Env.appendToPickle(file_name, sample)
        time+= timedelta(seconds=random.choice(seconds_list))
        print(time)

