# Title: Largest product in a grid
# Problem Statement:
#
# The sequence of triangle numbers is generated by adding the natural numbers. So the 7th triangle numbers
# would be 1 + 2 + 3 + 4 + 5 + 6 + 7 = 28. The first ten terms would be: 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...
# Let us list the factors of the first seven triangle numbers:
#
#  1: 1
#  3: 1, 3
#  6: 1, 2, 3, 6
# 10: 1, 2, 5, 10
# 15: 1, 3, 5, 15
# 21: 1, 3, 7, 21
# 28: 1, 2, 4, 7, 14, 28
#
# We can see that 28 is the first triangle number to have over five divisors.
#
# What is the value of the first triangle number to have over five hundred divisors?

go = True

triangle_num = 1
n = 2
factors = 0

while go:

	triangle_num += n
	counter = 1
	bound = triangle_num
	done = False
	while not done:
		if triangle_num % counter == 0:
			bound = triangle_num / counter
			if bound == counter:
				factors += 1
			else:
				factors += 2
			counter += 1
		else:
			counter += 1
		if counter >= bound:
			done = True

	print "current triangle number: %d" % triangle_num
	print "number of factors: %d" % factors
	if factors > 500:
		go = False
		print "triangle number: %d" % triangle_num
		print "number of factors: %d" % factors

	n += 1
	factors = 0