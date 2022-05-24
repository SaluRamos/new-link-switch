import time
from colorama import Fore, Style

class General:

    def system_time_log():
        return str(time.strftime("%d/%b at %H:%M:%S"))

    #General.Error(str(traceback.format_exc()), str(e))
    def error(error, aditional_info = ""):
        print(f"{Fore.RED}{Style.BRIGHT}XXXXX{Fore.WHITE}{Style.NORMAL}")
        print(f"{Fore.RED}{Style.BRIGHT}ERROR: '{error}'{Fore.WHITE}{Style.NORMAL}")
        if aditional_info != "":
            print(f"{Fore.RED}{Style.BRIGHT}ADITIONAL INFO:\n{aditional_info}{Fore.WHITE}{Style.NORMAL}")
        print(f"{Fore.RED}{Style.BRIGHT}XXXXX{Fore.WHITE}{Style.NORMAL}")