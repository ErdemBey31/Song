from threading import Thread
import os
def run(file):
  os.system(f"python {file}")

t1 = Thread(target=run, args=('web.py'))
t2 = Thread(target=run, args=('bot.py'))
t1.start();
t2.start();
t1.join();
t2.join();
