import time
from colorama import Fore, Style
from argon2 import PasswordHasher

#funções que não utilizam variaveis globais (funções gerais)
class Controller:

    def system_time_log():
        return str(time.strftime("%d/%b at %H:%M:%S"))

    #Controller.Error(str(traceback.format_exc()), str(e))
    def error(error, aditional_info = ""):
        print(f"{Fore.RED}{Style.BRIGHT}XXXXX{Fore.WHITE}{Style.NORMAL}")
        print(f"{Fore.RED}{Style.BRIGHT}ERROR: '{error}'{Fore.WHITE}{Style.NORMAL}")
        if aditional_info != "":
            print(f"{Fore.RED}{Style.BRIGHT}ADITIONAL INFO:\n{aditional_info}{Fore.WHITE}{Style.NORMAL}")
        print(f"{Fore.RED}{Style.BRIGHT}XXXXX{Fore.WHITE}{Style.NORMAL}")

    #procura em uma lista de strings por padrões de sql injection, retorna False se encontrar algo de errado
    def verify_response(responses):
        for i in responses:
            response = i.upper()
            filter_chars = ["'", "|", "<", ">", "!", "*", '"', "(", ")", "[", "]", "{", "}"]
            filter_words = ["SELECT", "ALTER", "TABLE", "CREATE", "DATABASE", "ADD", "DROP", "COLUMN", "SET", "DEFAULT ", "NULL", "CONSTRAINT", "FOREIGN", "REFERENCES", "BACKUP", "CHECK", "INDEX", "WHERE", "UPDATE"]
            for j in filter_chars:
                if j in response:
                    return f"char '{j}' (ascii = {ord(j)}) not allowed.\nPlease, try again."
            for j in filter_words:
                if j in response:
                    return f"word '{j}' not allowed.\nPlease, try again."
            if i == "":
                return "'blank' response not allowed.\nPlease, fill all the fields."
        return False

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