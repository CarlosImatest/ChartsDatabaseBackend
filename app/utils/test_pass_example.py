from pwdlib import PasswordHash, exceptions
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher

password_hash = PasswordHash((
    Argon2Hasher(),
    BcryptHasher(),
))

hash = password_hash.hash("herminetincture")
print(f"this is the hassedh password: \n{hash}")

#verifies the password matches the hash
valid = password_hash.verify("herminetincture", hash)
print(valid)

#the verify_and_update() method verifies the password but also update the hash if NECESSARY
#by necessary it means that the current hash was made by an older/different hasher like bcrypt
'''
for example

old_hash = BcryptHasher().hash("herminetincture")
print(f"old bcrypt hash:\n{old_hash}\n")

valid, updated_hash = password_hash.verify_and_update("herminetincture", old_hash)
print(f"valid: {valid}")
print(f"updated_hash: {updated_hash}")  # this will now be a real Argon2 hash string

old bcrypt hash:
$2b$12$U48HdVY1d2sJro2tKszxluNgQId7wZRsMQfGb3lAe2S1YPjQYoIJi

updated_hash: $argon2id$v=19$m=65536,t=3,p=4$gyhkQOaEUKYgZqcLa1kKIw$5Be03yIjnO3Xe2VpmTdxQH/AeDrJJJaJlqcLtI2gHVA'''
valid, updated_hash = password_hash.verify_and_update("herminetincture", hash)

print(f"new hashed password: \n{updated_hash}")
print(valid)