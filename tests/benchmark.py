from figure8 import figure8
from orbit import orbit
from pythagorean import pythagorean
from slingshot import slingshot

iters = int(input("Enter iterations: "))
test = int(input("Enter the test to run (1-figure8, 2-orbit, 3-pythagorean, 4-slingshot): "))

func = figure8

if test == 1:
    func = figure8
elif test == 2:
    func = orbit
elif test == 3:
    func = pythagorean
elif test == 4:
    func = slingshot

fps = 0

for x in range(iters):
    print("Test", x+1)
    fps += func(True)

print("Average FPS:", int(fps/iters))