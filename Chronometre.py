





from machine import Timer
import time

chrono = Timer.Chrono()

chrono.start()
time.sleep(1.25) # simulate the first lap took 1.25 seconds
lap = chrono.read() # read elapsed time without stopping
time.sleep(1.5)


print()

print("  %f seconds in the first lap" % lap)



lap=chrono.read()
while (True):
  print(chrono.read())
  time.sleep(0.1)
  
print("  %f seconds in the first lap" % lap)
chrono.stop()










