#!/usr/bin/env python
# coding: utf-8

# In[72]:


# ceaser cipher
def encryption(plain_text):
    cipher_text = ""
    for ch in plain_text:
        if ch.isalpha():
            ch = chr(ord(ch) + 3)
            if ch.isalpha() != True:
                ch = chr(ord(ch)-26)
        cipher_text += ch
    return cipher_text

def decryption(cipher):
    plain_text = ""
    for ch in cipher:
        if ch.isalpha():
            ch = chr(ord(ch) - 3)
            if ch.isalpha() != True:
                ch = chr(ord(ch) + 26)
        
        plain_text += ch
    return plain_text

original_text = "Computer Science and Engineering , University of Rajshahi"
print("original_text : ", original_text)

encrypted_text = encryption(original_text)
print("Encrypted Text: ", encrypted_text)

decrypted_text = decryption(encrypted_text)
print("Plain text: ", decrypted_text)


# In[ ]:


# # 2. Polygram substitution cipher

import itertools

char_substitution = {
    'a': 'x', 'b': 'q', 'c': 'i', 'd': 'n', 'e': 'b',
    'f': 'c', 'g': 'r', 'h': 'w', 'i': 'o', 'j': 'z',
    'k': 'l', 'l': 'h', 'm': 'a', 'n': 'u', 'o': 'f',
    'p': 'm', 'q': 'g', 'r': 't', 's': 'e', 't': 'y',
    'u': 's', 'v': 'd', 'w': 'p', 'x': 'v', 'y': 'j',
    'z': 'k'
}

def substitute(text):
    return ''.join(char_substitution.get(c.lower(), c) for c in text)

def generate_polygram_file(filename="Polygram Blocks.txt", max_n=3):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    total = 0

    with open(filename, 'w') as f:
        for n in range(max_n, 0, -1):
            for combo in itertools.product(letters, repeat=n):
                original = ''.join(combo)
                f.write(f"{original} {substitute(original)}\n")
                total += 1

    print(f"File '{filename}' generated with {total} combinations.")

if __name__ == "__main__":
    generate_polygram_file()


encryption_rules, decryption_rules = {} , {}

with open("Polygram Blocks.txt","r") as f:
    content = f.read()
    words = content.split()
    # print(words)

for i in range(0,len(words),2):
    word_1, word_2 = words[i], words[i+1]
    encryption_rules[word_1] = word_2
    decryption_rules[word_2] = word_1


def encrypt(plain_text):
    cipher_text = ""
    block = ""

    for i in range(len(plain_text)):
        if i and i % 3 == 0:
            cipher_text += encryption_rules[block]
            block = ""
        block += plain_text[i]

    cipher_text += encryption_rules[block]
    return cipher_text





def decrypt(cipher_text):
    plain_text = ""
    block = ""

    for i in range(len(cipher_text)):
        if i and i % 3 == 0:
            plain_text += decryption_rules[block]
            block = ""
        block += cipher_text[i]

    plain_text += decryption_rules[block]
    return plain_text


plain_text = 'rucse'
cipher_text = encrypt(plain_text)
decrypted_text = decrypt(cipher_text)

print(f"Plain Text: {plain_text}")
print(f"Encrypted Text: {cipher_text}")
print(f"Decrypted Text: {decrypted_text}")


# In[74]:


# Transposition cipher
def encryption(plain_text,width):
    length = len(plain_text)
    cipher_text = ""
    for k in range(width):
        for i in range(k,length,width):
            cipher_text += plain_text[i]
    
    return cipher_text

def decryption(cipher,width):
    length = len(cipher)
    plain_text = ['']*length
    idx = 0
    for k in range(width):
        for i in range(k,length,width):
            plain_text[i] += cipher[idx]
            idx += 1
    return ''.join(plain_text)

plain_text = "rucse, bangladesh"
width = 3

enc = encryption(plain_text,4)
print(enc)

dec = decryption(enc,width=4)
print(dec)

# double transposition
# enc2 = encryption(enc)

enc2 = encryption(enc,width=3)
print("double transposition: ",enc2)

dec1 = decryption(enc2,width=3)
print("First decipher :" , dec1)

dec2 = decryption(dec1,width=4)
print("Original text : ", dec2)




# In[75]:


#OTP
key = ""
store_key = ""

with open("OTP","r") as f:
    key = f.read()
    print(key)
store_key = key

def encryption(plain_text):
    cipher = ""
    ukey = ""
    for i,ch in enumerate(plain_text):
        if ch == ch.upper():
            char = (ord(ch) - ord('A')+(ord(key[i]) - ord('A'))) % 26 
            cipher += chr(char + ord('A'))
        elif ch == ch.lower():   
            char = (ord(ch) - ord('a')+(ord(key[i]) - ord('a'))) % 26
            cipher += chr(char + ord('a'))
        print("enc:",char)
        ukey += key[i]
    return cipher,ukey

def decryption(cipher,key):
    plain_text = ""
    for i,ch in enumerate(cipher):
        if ch == ch.upper():
            char = (ord(ch) - ord('A')-(ord(key[i]) - ord('A'))) % 26
            plain_text += chr(char + ord('A')) 
        elif ch == ch.lower():   
            char = (ord(ch) - ord('a')-(ord(key[i]) - ord('a'))) % 26
            plain_text += chr(char + ord('a'))
        print("dec:",char)
        
    return plain_text

plain_text = "ruCseENGliSh"
enc,ukey = encryption(plain_text)
print(enc,"",ukey)

dec = decryption(enc,ukey)
print(dec)

remaining_key = key[len(plain_text):]

print(len(ukey), " ", len(plain_text))

with open("OTP","w") as f:
    f.write(remaining_key)

with open("OTP","r") as f:
    key = f.read()
    print(key)


# In[82]:


# Lehman primality test
import random

def lehman_primality_test(p,t):
    if p < 2:
        return False
    if p in [2,3]:
        return True
    if p%2==0:
        return False
    
    for _ in range(t):
        a = random.randint(2,p-2)
        x = pow(a,((p-1)//2),p)
        # x = (a ** int((p-1)/2))%p
        if x not in [1,p-1]:
            return False
    return True

p = 999983
res = lehman_primality_test(p,50)
if res == True:
    print("Probably prime")
else:
    print("Composit")


# In[84]:


# miller - rabin
def miller_rabin(n,k):
    if n < 2:
        return False
    if n in [2,3]:
        return True
    if n % 2 == 0:
        return False

    m = n-1
    b = 0

    while m % 2 == 0:
        m //= 2
        b+=1
    
    for _ in range(k):
        a = random.randint(2,n-1)

        z = pow(a,m)%n

        if z == 1 or z == n-1:
            continue
        for _ in range(b-1):
            z = pow(z,2)%n
            if z == n-1:
                break
            if z == 1:
                return False
        else:
            return False
    
    return True

test_numbers = [7,13,15,17,19,21,561]
for num in test_numbers:
    print(f"{num} is probably prime " if miller_rabin(num, k =5) else f"{num} is composite" )

# res = miller_rabin(p,10)
# if res == True:
#     print("Probably prime")
# else:
#     print("Composite")


# In[91]:


import hashlib

plain_text = "hello world"
cipher = hashlib.md5(plain_text.encode()).hexdigest()

sha = hashlib.sha1(plain_text.encode()).hexdigest()
print(cipher)
print(sha)


# In[103]:


# RSA
import random
from math import gcd,isqrt

def is_prin(n):
    if n < 2:
        return False
    for i in range(2,isqrt(n)+1):
        if n % i == 0:
            return False
    return True

def generate_key_pair():
    primes = [p for p in range(50,100) if is_prin(p)]
    p = random.choice(primes)
    q = random.choice(primes)
    while p == q:
        q = random.choice(primes)
    n = p * q
    phi = (p-1) * (q-1)
    e = 65537

    while gcd(e,phi) != 1:
        e = random.randint(3,phi-1)
    
    d = pow(e, -1, phi)
    return (e,n),(d,n),p,q

def rsa_encrypt(message,public_key):
    e,n = public_key
    return pow(message,e,n)

def rsa_decrypt(message,private_key):
    d,n = private_key
    return pow(message,d,n)
def string_to_ascii(text):
    return [ord(c) for c in text]
def ascii_to_string(ascii_list):
    return ''.join(chr(i) for i in ascii_list)

public_key,private_key,p,q = generate_key_pair()
e,n = public_key
d,_ = private_key

print("RSA key generation:")
print(f"p : {p}, q : {q}")
print(f"n : {n}")
print(f"e : {e}")
print(f"d : {d}")

integer_message = 42
enc_int = rsa_encrypt(integer_message,(e,n))
dec_int = rsa_decrypt(enc_int,(d,n))

print(f"original message : {integer_message}")
print(f"encryption : {enc_int}")
print(f"decryption : {dec_int} ")

string_msg = "rusho"
ascii = string_to_ascii(string_msg)
enc_str = []
enc_str = [rsa_encrypt(val,public_key) for val in ascii]
dec_str = [rsa_decrypt(val,private_key) for val in enc_str]
print(enc_str)
print(dec_str)
print(ascii)
print("original strring: ", ascii_to_string(dec_str))

long_msg = 6882326879666682
mst_str = str(long_msg)
block_size = len(str(n))-1

blocks = [int(mst_str[i:i+block_size]) for i in range(0,len(mst_str),block_size)]

enc_blocks = [rsa_encrypt(block,public_key) for block in blocks]
dec_blocks = [rsa_decrypt(block,private_key) for block in enc_blocks]

print(enc_blocks)
print(dec_blocks)
print(blocks)

decrypted_text = ''.join((str(b)) for b in dec_blocks)
print(decrypted_text)


# In[126]:


# diffie hellman
import random
import math

def find_primitive_roots(p):
    required_set = {num for num in range(1,p) if math.gcd(num,p) == 1}
    primitive_roots = []

    for g in range(2,p):
        actual_set = {pow(g,powers,p) for powers in range(1,p)}
        if required_set == actual_set:
            primitive_roots.append(g)
    
    return primitive_roots


def diffie_hellman(prime,primitive_root):
    xa = random.randint(1,prime-1)
    ya = pow(primitive_root,xa,prime)

    xb = random.randint(1,prime-1)
    while xa == xb:
        xb = random.randint(1,prime-1)
    
    yb = pow(primitive_root,xb,prime)

    k1 = pow(yb,xa,prime)
    k2 = pow(ya,xb,prime)

    print(f"A's private key : {xa}, public key = {ya}")
    print(f"B's primitive root = {xb}, public key = {yb}")
    print(f"Shared key at A's end = {k1}, at B's end = {k2}")

    if k1 == k2:
        print("Key exchange successfully")
    else :
        print("failed")

p = 13
primitive_root = find_primitive_roots(p)
if primitive_root:
    pr = random.choice(primitive_root)
    diffie_hellman(p,pr)
else:
    print("error")



# In[128]:


# pgp
import hashlib
import os
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA1
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

print("PGP Implementation - Using Built-in RSA and AES Functions")

class PGPSystem:
    def __init__(self):
        self.sender_key = RSA.generate(1024)
        self.receiver_key = RSA.generate(1024)
        print("PGP System Initialized")
    
    def authentication_service(self, message):
        # SHA-1 hash of message
        message_bytes = message.encode('utf-8')
        hash_code = SHA1.new(message_bytes)
        
        # Sign hash with sender's private key
        signature = pkcs1_15.new(self.sender_key).sign(hash_code)
        
        # Prepend signature to message
        signed_message = signature + message_bytes
        return signed_message, len(signature)
    
    def authentication_verify(self, signed_message, signature_length):
        # Extract signature and message
        signature = signed_message[:signature_length]
        message_bytes = signed_message[signature_length:]
        message = message_bytes.decode('utf-8')
        
        try:
            # Verify signature with sender's public key
            new_hash = SHA1.new(message_bytes)
            pkcs1_15.new(self.sender_key.publickey()).verify(new_hash, signature)
            return True, message
        except (ValueError, TypeError):
            return False, message
    
    def confidentiality_service(self, message):
        # Generate 128-bit session key
        session_key = get_random_bytes(16)
        
        # Encrypt message with AES
        cipher_aes = AES.new(session_key, AES.MODE_CBC)
        iv = cipher_aes.iv
        padded_message = pad(message.encode('utf-8'), AES.block_size)
        encrypted_message = cipher_aes.encrypt(padded_message)
        
        # Encrypt session key with RSA
        cipher_rsa = PKCS1_OAEP.new(self.receiver_key.publickey())
        encrypted_session_key = cipher_rsa.encrypt(session_key)
        
        # Combine: encrypted_session_key + iv + encrypted_message
        encrypted_package = encrypted_session_key + iv + encrypted_message
        return encrypted_package, len(encrypted_session_key)
    
    def confidentiality_decrypt(self, encrypted_package, key_length):
        # Extract components
        encrypted_session_key = encrypted_package[:key_length]
        iv = encrypted_package[key_length:key_length+16]
        encrypted_message = encrypted_package[key_length+16:]
        
        # Decrypt session key with RSA
        cipher_rsa = PKCS1_OAEP.new(self.receiver_key)
        session_key = cipher_rsa.decrypt(encrypted_session_key)
        
        # Decrypt message with session key
        cipher_aes = AES.new(session_key, AES.MODE_CBC, iv)
        decrypted_padded = cipher_aes.decrypt(encrypted_message)
        decrypted_message = unpad(decrypted_padded, AES.block_size).decode('utf-8')
        
        return decrypted_message

# Initialize PGP System
pgp = PGPSystem()

# Test PGP Services
message = "This is a confidential message for PGP testing"

# Test Authentication Service
signed_msg, sig_len = pgp.authentication_service(message)
is_authentic, recovered_msg = pgp.authentication_verify(signed_msg, sig_len)

# Test Confidentiality Service  
encrypted_pkg, key_len = pgp.confidentiality_service(message)
decrypted_msg = pgp.confidentiality_decrypt(encrypted_pkg, key_len)

# Results
print("PGP Test Results:")
print(f"Original: '{message}'")
print(f"Authentication: {'PASS' if is_authentic and recovered_msg == message else 'FAIL'}")
print(f"Confidentiality: {'PASS' if decrypted_msg == message else 'FAIL'}")

