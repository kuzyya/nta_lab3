from itertools import *
import random
import math
import sys
import numpy as np
rand = random.SystemRandom()
import time
from lab2 import full_gcd, inverse, canonical_factorization
#from lab1 import solovei_shtrassen

def is_prime(a):
    if a < 2:
        return False
    if a == 2 or a == 3:
        return True
    if a % 2 == 0 or a % 3 == 0:
        return False
    i = 5
    while i * i <= a:
        if a % i == 0 or a % (i + 2) == 0:
            return False
        i += 6
    return True

def get_primes(n):
    c = 3.38
    primes = []
    B = int(c * math.exp(1 / 2 * (math.log2(n) * math.log2(math.log2(n))) ** (1 / 2)))

    sieve = [True] * B
    sieve[0] = sieve[1] = False

    for i in range(2, int(math.sqrt(B)) + 1):
        if sieve[i]:
            for j in range(i * i, B, i):
                sieve[j] = False

    for i in range(2, B):
        if sieve[i] and is_prime(i):
            primes.append(i)

    return primes

def decompose(n, prime_numbers):
    factor_counts = canonical_factorization(n)
    decomposition = []
    for factor, count in factor_counts.items():
        if factor in prime_numbers:
            decomposition += [prime_numbers.index(factor)] * count
        else:
            return []
    return decomposition

def smoothness(a, b, n, prime_numbers, k, keys, keys3):
    if len(decompose((b * pow(a, k, n)) % n, prime_numbers)) > 0:
        keys.append(k)
        keys3.append([b, k])
        return keys, keys3
    else:
        return keys, keys3

def system_of_linear_equations(a,b,b1,n,prime_numbers,keys,keys3):
    system = []
    lenght = len(keys)
    i = 0
 
    while i < len(keys):
        if(b1 == 1 ):
            power =pow(a,keys[i],n)
            if (power == b):
                sys.exit(print("random success, answer is: ", keys[i] ))
        else:
            power = (b1*pow(a,keys[i],n))%n
        if (power == b):
           sys.exit(print("random success, answer is: ", keys[i] ))
        var = decompose(power,prime_numbers)
        if(len(var)==0):
            keys.pop(i)
            if(len(keys3)!= 0):
                keys3.pop(i)
            i -=1
        else:
            system.append(var)
        i+=1
        
    return keys, system , keys3

def edit_matrix(system,prime_numbers):
    l = len(system)
    matrix = np.array([np.zeros(len(prime_numbers))]*(l))
    for i in range(len(system)):
        raw = np.zeros(len(prime_numbers))
        for k in system[i]:
            raw[k]+=1
        matrix[i] = raw
    return matrix

def solve_system(n,keys,system,prime_numbers):
    system = edit_matrix(system, prime_numbers)
    keys = np.array(keys)
    l = len(system)
    #print(system, keys)
    good_vectors = []
    good_answers = []
    for i in range(len(keys)):
        index = 0
        len_vec = len(system[i])
        var = 0
        for j in range(len_vec):
            var = int(var + system[i][j])
            if(system[i][j] !=0):
                index+=1
                ind = j
        if (index == 1):
            if(math.gcd(var,(n-1)) != 1):
                continue
            else:
                keys[i] = (keys[i]*inverse(system[i][ind],(n-1)))%(n-1)
                system[i][ind] = 1
                good_vectors.append(list(system[i]))
                good_answers.append(keys[i])
    #after this we have array of ez numbers *x = num*
    
    return keys, system
     
def linear_equations(a,b,n,prime_numbers):
    c=int(n/2)
    keys3= []
    keys = []
    system = []
    k = random.sample(range(1, n + 1), len(prime_numbers)+c)
    for i in range(len(prime_numbers)+c):
        keys, keys3 = smoothness(a,1, n ,prime_numbers, k[i], keys, keys3)
    keys, system = system_of_linear_equations(a,b,1,n,prime_numbers,keys,keys3)[0],system_of_linear_equations(a,b,1,n,prime_numbers,keys,keys3)[1]
    return keys,system

def unsolved_answers(a,b,n,prime_numbers):
    keys2 = []
    keys3 = []
    system2 = []
    l = random.sample(range(1, n), int(n/2))
    for i in range(len(prime_numbers)):
        keys2,keys3 = smoothness(a,b, n ,prime_numbers, l[i], keys2, keys3)
    #print("keys2", keys2)
    keys2, system2 = system_of_linear_equations(a,1,b,n,prime_numbers,keys2,keys3)[2],system_of_linear_equations(a,b,b,n,prime_numbers,keys2,keys3)[1]
    
    return keys2,system2

def solve_index_calculus(keys,system,keys2,system2):
    x = 0
    for i in range(len(keys2)):
        idx = np.where((system == (system2[i])).all(axis=1))
        if(len(idx[0])>0):
            if(len(idx)>1):
                idx = int(idx[0])
                x = (keys[idx] - keys2[i][1])%(n-1)
                return x
            else:
                x = (keys[idx] - keys2[i][1])%(n-1)
                return x

def index_calculus(a,b,n):
    primes= get_primes(n)
    keys, system = linear_equations(a,b,n,primes)
    keys, system = solve_system(n,keys,system,primes)
    keys2, system2 = unsolved_answers(a,b,n,primes)
    system2 = edit_matrix(system2,primes)
    x = solve_index_calculus(keys,system,keys2,system2)
    return x


a = int(input("Введіть a: "))
b = int(input("Введіть b: "))
n = int(input("Введіть n: "))

# a = 691
# b = 4757
# n = 34583
#start_time = time.time()
print("Your answer is : ",index_calculus(a,b,n)[0])
# end_time = time.time()
# execution_time = end_time - start_time
# print("time:", execution_time, "s")




