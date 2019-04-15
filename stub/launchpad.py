import launchpad_py
import time

lp = launchpad_py.Launchpad()

print(lp.Check(number=0,name="Launchpad Mini MIDI 1"))
print(lp.Open(number=0,name="Launchpad Mini MIDI 1"))

lp.LedAllOn()

while True:
    print(lp.EventRaw())
    time.sleep(0.5)

lp.Close()
