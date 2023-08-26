from threading import Thread
import os
def run():
  os.system(f"python web.py")
def run2():
  os.system("python python bot.py")
t1 = Thread(target=run)
t2 = Thread(target=run2)
t1.start();
t2.start();
t1.join();
t2.join();
try:
  t1.daemon = True
  t2.daemon = True
  print("root aktif")
except Exception as e:
  print(f"ROOT HATA\n\n{e}")
