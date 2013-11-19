# Title: Special Pythagorean triplet
# Problem Statement:
#
# A Pythagorean triplet is a set of three natural numbers, a<b<c, for which a^2 + b^2 = c^2
# For example, 3^2 + 4^2 = 9 + 16 = 25 = 5^2
#
# There exists exactly one Pythagorean triplet for which a + b + c = 1000.
# Find the product a*b*c
import math

for a in range(1, 999):
	for b in range((a + 1), 1000):
		c = math.sqrt((a**2) + (b**2))
		c_floor = math.floor(c)
		error = c - c_floor
		if error <= math.pow(10, -9):
			if (a + b + c) == 1000.0:
				print "a: %f" % a
				print "b: %f" % b
				print "c: %f" % c
				print "sum: %f" % (a+b+c)
				print "product: %f" % (a*b*c)
			else:
				pass
		else:
			pass