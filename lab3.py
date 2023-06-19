from lab2 import full_gcd, inverse, canonical_factorization
#from lab1 import solovei_shtrassen
from itertools import *
import random
import math
from sys import exit
from numpy import zeros, array, where
rand = random.SystemRandom()
import time

def sieve_of_eratosthenes(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    p = 2
    while p * p <= n:
        if is_prime[p]:
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
        p += 1
    prime_numbers = [i for i, prime in enumerate(is_prime) if prime]
    return prime_numbers

def find_prime_numbers(n):
    c = 3.38
    B = int(c * math.exp(1/2 * (math.log2(n) * math.log2(math.log2(n))) ** (1/2)))
    prime_numbers = sieve_of_eratosthenes(B)
    return prime_numbers

def decompose(n, prime_numbers):
    factor_counts = canonical_factorization(n)
    decomposition = []
    for factor, count in factor_counts.items():
        if factor in prime_numbers:
            decomposition += [prime_numbers.index(factor)] * count
        else:
            return []
    return decomposition

def smoothness(a, b, n, prime_numbers, k, keys, keys_thrd):
    if(len(decompose(b*pow(a, k, n)% n, prime_numbers))>0):
        keys.append(k)
        keys_thrd.append([b,k])
        return keys,keys_thrd
    else:
        return keys, keys_thrd
          

def sole(a, b, b1, n, prime_numbers, keys, keys_thrd):
    system = []
    lenght = len(keys)
    i = 0
 
    while i < len(keys):
        if(b1 == 1 ):
            power =pow(a,keys[i],n)
            if (power == b):
                exit(print(f"Відповідь: {keys[i]}"))
        else:
            power = b1*pow(a,keys[i],n)%n
        if (power == b):
           exit(print(f"Відповідь: {keys[i]}"))
        var = decompose(power,prime_numbers)
        if(len(var)==0):
            keys.pop(i)
            if(len(keys_thrd)!= 0):
                keys_thrd.pop(i)
            i -=1
        else:
            system.append(var)
        i+=1
        
    return keys, system, keys_thrd    

def edit_matrix(system, prime_numbers):
    matrix = zeros((len(system), max(prime_numbers) + 1), dtype=int)
    for i in range(len(system)):
        for k in system[i]:
            matrix[i, k] += 1
    return matrix

def solver(n,keys,system,prime_numbers):
    system = edit_matrix(system, prime_numbers)
    keys = array(keys)
    vectors = []
    answers = []
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
            if(full_gcd(var,(n-1))[0] != 1):
                continue
            else:
                keys[i] = keys[i]*inverse(system[i][ind],(n-1))%(n-1)
                system[i][ind] = 1
                vectors.append(list(system[i]))
                answers.append(keys[i])
    
    return keys, system
           
def linear_equations(a,b,n,prime_numbers):
    y=int(n*0.5)
    keys_thrd= []
    keys = []
    system = []
    k = random.sample(range(1, n + 1), len(prime_numbers) + y)
    for i in range(len(prime_numbers) + y):
        keys, keys_thrd = smoothness(a,1, n ,prime_numbers, k[i], keys, keys_thrd)
    keys, system = sole(a,b,1,n,prime_numbers,keys,keys_thrd)[0],sole(a, b, 1, n, prime_numbers, keys, keys_thrd)[1]
    return keys,system

def cant_find(a, b, n, prime_numbers):
    second_keys = []
    keys_thrd = []
    second_system = []
    l = random.sample(range(1, n), int(n/2))
    for i in range(len(prime_numbers)):
        second_keys,keys_thrd = smoothness(a,b, n ,prime_numbers, l[i], second_keys, keys_thrd)
    second_keys, second_system = sole(a, 1, b, n, prime_numbers, second_keys, keys_thrd)[2],sole(a, b, b, n, prime_numbers, second_keys, keys_thrd)[1]
    return second_keys,second_system

def solvelus(keys, system, second_keys, second_system):
    x = 0
    for i in range(len(second_keys)):
        idx = where((system == (second_system[i])).all(axis=1))
        if(len(idx[0])>0):
            if(len(idx)>1):
                idx = int(idx[0])
                x = keys[idx] - second_keys[i][1]%( n-1)
                return x
            else:
                x = keys[idx] - second_keys[i][1]%(n-1)
                return x
    
def logarifming(a,b,n):
    primes = find_prime_numbers(n)
    keys, system = linear_equations(a, b, n, primes)
    keys, system = solver(n, keys, system, primes)
    second_keys, second_system = cant_find(a, b, n, primes)
    second_system = edit_matrix(second_system, primes)
    x = solvelus(keys, system, second_keys, second_system)
    return x
        
a = int(input("Введіть a: "))
b = int(input("Введіть b: "))
n = int(input("Введіть n: "))
begin = time.time()
print(f"Відповідь: {logarifming(a,b,n)[0]}")
after = time.time()
print(f"Обчислено за : {after - begin}")
