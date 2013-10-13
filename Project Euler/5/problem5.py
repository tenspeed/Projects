# Title: Smallest multiple
# Problem Statement: 2520 is the smallest number that can be divided by each of the numbers
# 1 to 10 without any remainder.
#
# What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?

def is_multiple(num):
	for j in range(2, 21):
		if num % j != 0:
			return 0
		elif j == 20:
			return num
		else:
			pass

stop = 0
i = 40

while stop == 0:
	stop = is_multiple(i)
	i += 2
print stop