import requests
import hashlib
import base58
import codecs
import ecdsa
private_key = "18e14a7b6aaaaaaaaaa4f8114701e7c8e774e7f9a47e2c2035db29a206321725"
print(private_key)

#randomizing the startpoint at every program launch, so you dont scroll the same wallets again and again
a =int(input("Enter a big random number(1-9999999999999999999999): "))
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
	

def gen_public_key(private_key):

	private_key_bytes = codecs.decode(private_key, 'hex')
	public_key_raw = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
	public_key_bytes = public_key_raw.to_string()
	public_key_hex = codecs.encode(public_key_bytes, 'hex')
	public_key = (b'04' + public_key_hex).decode("utf-8")



	if (ord(bytearray.fromhex(public_key[-2:])) % 2 == 0):
	    public_key_compressed = '02'
	else:
	    public_key_compressed = '03'
    
	public_key_compressed += public_key[2:66]


	hex_str = bytearray.fromhex(public_key_compressed)
	sha = hashlib.sha256()
	sha.update(hex_str)


	rip = hashlib.new('ripemd160')
	rip.update(sha.digest())
	key_hash = rip.hexdigest()


	modified_key_hash = "00" + key_hash

	sha = hashlib.sha256()
	hex_str = bytearray.fromhex(modified_key_hash)
	sha.update(hex_str)


	sha_2 = hashlib.sha256()
	sha_2.update(sha.digest())

	checksum = sha_2.hexdigest()[:8]
	
	byte_25_address = modified_key_hash + checksum
	


	address = base58.b58encode(bytes(bytearray.fromhex(byte_25_address))).decode('utf-8')
	print(f"Privatekey: {private_key}")
	print(f"Publickey: {address}")
	print("-----------------------------------------------------------------------------------------------")
	return address

while True:
	private_key_decimal = int(private_key, base=16)
	private_key_decimal += 1
	private_key=str(hex(private_key_decimal))
	private_key = private_key[2:]
	pub_key = gen_public_key(private_key)
	data = requests.get(f"https://blockstream.info/api/address/{pub_key}").json()
	eingehend = data["chain_stats"]["funded_txo_count"]
	print(f'Balance: {data["chain_stats"]["funded_txo_sum"]-data["chain_stats"]["spent_txo_sum"]}')
	if eingehend >= 1:
		with open("yay.txt","a") as f:
			f.write(f"{private_key}\n")
	

