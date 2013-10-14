# Title: 10001st prime
# Problem Statement:
#
# By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.
# What is the 10001st prime number?

primes = 6
num = 14
while primes <= 30:
	if num % 2 == 0:
		num += 1
	elif num % 3 == 0:
		num += 1
	elif num % 5 == 0:
		num += 1
	elif num % 7 == 0:
		num += 1
	else:
		primes += 1
		num += 1

print """
The %dst prime number: %d
""" % (primes, num - 1)