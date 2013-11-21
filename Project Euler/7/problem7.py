# Title: 10001st prime
# Problem Statement:
#
# By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.
# What is the 10001st prime number?

def is_prime(num, primes_list):
	for i in range(len(primes_list)):
		if num % primes_list[i] == 0:
			return False
		else:
			if i == (len(primes_list) - 1):
				return True

def get_primes(num, primes_list):
	while True:
		if is_prime(num, primes_list):
			primes_list.append(num)
			return primes_list
		else:
			num += 1

primes = [2, 3, 5, 7]

while len(primes) <= 10001:
	primes = get_primes((primes[-1] + 1), primes )

print "number of primes found: %d" % (len(primes - 1)
print "%dst prime: %d" % (len(primes), primes[-1])