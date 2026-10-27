/*
8: find all bases b for which an odd composite number n is pseudoprime
Fermat’s little theorem: a fact about primes
If n is prime, then for every b with (b, n) = 1: b^(n−1) ≡ 1 (mod n).
The Fermat test: an algorithm that uses the theorem
Pick a random base b, compute r = b^(n−1) mod n. If r ≠ 1, output COMPOSITE. If it never fails after k tries, output PROBABLY PRIME.
Pseudoprime: a definition about composites
An odd composite n is a pseudoprime to base b if (b, n) = 1 and b^(n−1) ≡ 1 (mod n).
It names a composite number that fooled the test for one specific base. It’s the “failure case” of the test. It is always relative to a base b.
Carmichael numbers (like 561) are the exception: composites that pass for every base coprime to n, so the Fermat test can’t catch them.
*/
#include <stdio.h>
#include <stdlib.h>

typedef unsigned long long u64;

//Euclid gcd
u64 gcd(u64 a, u64 b){
    while (b!=0){
        u64 r = a%b;
        a=b;
        b=r;
    }
    return a;
}

u64 mod_pow(u64 b, u64 n) {
    /*
    naive: b^e takes e-1 multiplications
    here: log2(e) * 2 multiplications
    b^e has about e · log₂(b) bits
    */
    u64 e = n - 1; 
    u64 r = 1;    
    u64 p = b % n; //current power of b
    while (e > 0) {
        if (e & 1) {          
            //(b % n) · (b % n) % n = b² % n    
            r = (r * p) % n; //e's binary digits decides what values get collected
        }
        p = (p * p) % n;         
        e >>= 1;                
    }
    return r;    
}

int is_prime(u64 n) {
    if (n < 2) return 0;
    for (u64 d = 2; d * d <= n; d++) {
        if (n % d == 0) return 0;
    }
    return 1;
}

int main(int argc, char *argv[]) {
    u64 n;
    if (argc > 1) {
        n = strtoull(argv[1], NULL, 10);
    } else {
        printf("Enter an odd composite number n: ");
        if (scanf("%llu", &n) != 1) {
            printf("Invalid input.\n");
            exit(1);
        }
    }
    if (n >= (1ULL << 32)){
        printf("n must be at most 4294967295.\n");
        exit(1);
    }
    if (n < 9 || n % 2 == 0 || is_prime(n)) {
        printf("n must be an odd composite number (e.g. 9, 15, 91, 341, 561).\n");
        exit(1);
    }
    u64 count = 0;
    //a list of the bases that make a known composite number look prime
    printf("Bases b for which %llu is pseudoprime:\n", n);
    for (u64 b = 1; b < n; b++) {
        if (gcd(b, n) == 1 && mod_pow(b, n) == 1) {
            printf("%llu ", b);
            count++;
        }
    }
    printf("\nTotal: %llu bases\n", count);
    return 0;

}
