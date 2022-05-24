from argon2 import PasswordHasher

class Hash:

    #retorna o hash de uma string
    def generate_hash(the_string, h = 64, s = 32, m = 16384, t = 4):
        password_hasher = PasswordHasher(hash_len = h, salt_len = s, memory_cost = m, time_cost = t)
        return password_hasher.hash(the_string)

    #verifica se o hash e a string batem
    def verify_hash(the_string, the_hash):
        password_hasher = PasswordHasher()
        try:
            return password_hasher.verify(the_hash, the_string)
        except:
            return False