import hashlib

def SHA256Hash(concatenation_list):
	
	hash_string = hashlib.sha256()

	for item in concatenation_list:
		hash_string.update(str(item))

	return hash_string.hexdigest()