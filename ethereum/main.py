api_key ="YOUR_API_KEY_HERE"

import codecs
import requests
import time
import ecdsa
from Crypto.Hash import keccak #pip install cryptodome

def checksum_address(address):
    checksum = '0x'
    # Remove '0x' from the address
    address = address[2:]
    address_byte_array = address.encode('utf-8')
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(address_byte_array)
    keccak_digest = keccak_hash.hexdigest()
    for i in range(len(address)):
        address_char = address[i]
        keccak_char = keccak_digest[i]
        if int(keccak_char, 16) >= 8:
            checksum += address_char.upper()
        else:
            checksum += str(address_char)
    return checksum

def gen_public(private_key):
    private_key_bytes = codecs.decode(private_key, 'hex')
    # Get ECDSA public key
    key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
    key_bytes = key.to_string()
    public_key = codecs.encode(key_bytes, 'hex')
    return public_key

def gen_address(public_key):
    public_key_bytes = codecs.decode(public_key, 'hex')
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(public_key_bytes)
    keccak_digest = keccak_hash.hexdigest()
    # Take last 20 bytes
    wallet_len = 40
    wallet = '0x' + keccak_digest[-wallet_len:]
    return wallet


private_key = '28441ca5276a9d010cab075584ef3b67cd9a9c84afe7bd502eb89af3171e4980'
a =int(input("random number between 1 and 100000000000000000000"))
if a % 2 == 0:
        private_key_decimal = int(private_key, base=16)
        private_key_decimal += a
        private_key=str(hex(private_key_decimal))
        #print(private_key,"\n",type(private_key))
        private_key = private_key[2:]
else:
        private_key_decimal = int(private_key, base=16)
        private_key_decimal -= a
        private_key=str(hex(private_key_decimal))
        #print(private_key,"\n",type(private_key))
        private_key = private_key[2:]
while True:
#       time.sleep(0.25)
        private_key_decimal = int(private_key, base=16)
        private_key_decimal += 1
        private_key=str(hex(private_key_decimal))
        private_key = private_key[2:]

        tmp = gen_public(private_key)
        address = gen_address(tmp)
        x = requests.get(f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={api_key}").json()
        balance = int(x["result"])
        print(f"address: {address}\nbalance: {balance}\n---------------------------------------------------------------------------")
        if balance >= 1:
                with open("yay.txt","a") as f:
                        f.write(f"{private_key}\n")



