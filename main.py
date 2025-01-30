from functions import *
from RSA import *

P, S = generate_key_pair(1024)
print(P)
print(S)

m = 0xFFFFF

print(m)
c = RSA_encrypt(m, P)
print(c)
print(RSA_decrypt(c, S))