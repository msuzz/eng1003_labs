# Program for computing the circumference and area of a circle

# For pi
import math

r = 2       # radius in cm

c = 2 * math.pi * r
print("Circumference of the circle is {0}cm.".format(c))

a = c**2 / 4 * math.pi
print("Area of the circle is {0}cm.".format(a))