# Title: Summation of primes
# Problem Statement:
#
# The sum of the primes below 10 is 2 + 3 + 5 + 9 = 17.
#
# Find the sum of all the primes below two million.

def is_prime(num, prime_list):
	for i in range(len(prime_list)):
		if num % prime_list[i] == 0:
			return False
		else:
			if i == (len(prime_list) - 1):
				return True

def get_primes(num, prime_list):
	while True:	
		if is_prime(num, prime_list):
			prime_list.append(num)
			return prime_list
		else:
			num += 1

primes = []
compositions = []

for i in range(2, 2000000):
	primes.append(i)

p_index =  0
p = primes[p_index]

while p != primes[-1]:
	p = primes[p_index]
	print "p: %d" % p
	print "last num: %d" % primes[-1]

	for j in range(len(primes)):
		if primes[j] == p:
			pass
		elif primes[j] % p == 0:
			compositions.append(j)

	index_shift = 0

	if len(compositions) != 0:
		for k in range(len(compositions)):
			primes.pop((compositions[k] - index_shift))
			index_shift += 1

	compositions = []
	p_index += 1

p_sum = 0

for i in range(len(primes)):
	p_sum += primes[i]

print "number of primes found: %d" % len(primes)
print "sum of all primes found: %d" % p_sum