import os
from scripts.controller import Controller

class Vars:

    version = "2.0"
    try:
        server_port = int(os.environ["PORT"])
    except:
        server_port = 8080
    db = None
    start_time = Controller.system_time_log()
    initial_link_input_value = "paste here one of your links!"
    app_link = "https://link-switch.herokuapp.com"
