#Base64
import base64
import binascii

def decrypt(ciphertext, b=None):
	try:
		plaintext = str(base64.b64decode(ciphertext))
		if plaintext.startswith("b'") and plaintext.endswith("'"):
			plaintext = plaintext[2:-1] #fixes formatting
		return [plaintext]
	except binascii.Error:
		return []