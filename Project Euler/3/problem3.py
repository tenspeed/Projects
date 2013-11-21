# Title: Largest prime factor
# Problem Statement:
#
# The prime factors of 13195 are 5, 7, 13, and 29.
#
# What is the largest prime factor of the number 600851475143?

def get_primes(num, prime_list):
	for i in range(500):
		if is_prime(num, prime_list):
			prime_list.append(num)
		else:
			num += 1
	return prime_list

def is_prime(num, prime_list):
	for i in range(len(prime_list)):
		if num % prime_list[i] == 0:
			break
		else:
			if i == (len(prime_list) - 1):
				return True
			else:
				pass
	return False

p_factors = []
primes = [2, 3, 5, 7]
quotient = 600851475143
p_found = False
go = True

for i in range(15):
	primes = get_primes((primes[-1] + 1), primes)

while go:
	for element in primes:
		if (quotient % element == 0) and (quotient != element):
			quotient /= element
			p_found = True
			p_factors.append(element)
			if is_prime(quotient, primes):
				p_factors.append(quotient)
				go = False
		else:
			pass

	if (p_found == False):
		primes = get_primes((primes[-1] + 1), primes)
	else:
		p_found == False

print p_factors