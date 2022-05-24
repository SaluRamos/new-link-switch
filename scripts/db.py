import traceback
from colorama import Fore, Style
from scripts.controller import Controller
from scripts.variables import Vars
from scripts.models import Link
import psycopg2
import os
import time

class Database:

    def __init__(self, host, database, user, password):
        try:
            self.conn = psycopg2.connect(os.environ["DATABASE_URL"], sslmode = "require")
        except:
            self.conn = psycopg2.connect(host = host, database = database, user = user, password = password)
        self.cur = self.conn.cursor()

    def new_link(self, link_name, links, owner):
        try:
            self.cur.execute(f"SELECT link_name FROM links WHERE link_name = '{link_name}' and owner = '{owner}';")
            selected = self.cur.fetchall()
            if len(selected) == 0:
                self.cur.execute(f"INSERT INTO links (link_name, links, last_index, owner) VALUES ('{link_name}', '{links}', '0', '{owner}');")
                self.conn.commit()
                return f"INSERTED IN DATABASE"
            else:
                self.cur.execute(f"UPDATE links SET links = '{links}', last_index = '0' WHERE link_name = '{link_name}';")
                self.conn.commit()
                return f"UPDATED IN DATABASE"
        except:
            Controller.error(str(traceback.format_exc()))
            return "ERROR"

    def delete_link(self, link_name, owner):
        try:
            self.cur.execute(f"DELETE FROM links WHERE link_name = '{link_name}' AND owner = '{owner}';")
            self.conn.commit()
            return "SUCCESFUL DELETE"
        except:
            Controller.error(str(traceback.format_exc()))
            return "ERROR"

    def get_redirections_info(self, username, link_name):
        self.cur.execute(f"SELECT UNIQUE_CLIENTS_EVER, UNIQUE_CLIENTS_24HRS, UNIQUE_REDIRECTIONS_EVER, UNIQUE_REDIRECTIONS_24HRS, CLIENTS_EVER, CLIENTS_24HRS FROM links WHERE owner = '{username}' and link_name = '{link_name}';")
        info = self.cur.fetchall()
        info = f"UNIQUE_CLIENTS_REQUESTS:{len(Vars.clients)}<br>UNIQUE_REDIRECTIONS:{Vars.total_redirections}<br><br>"
        for i in Vars.redirections.keys():
            info = info + f"'{i}':{Vars.redirections[i]}<br>"
        return info

    def get_links(self, username, link_name):
        try:
            self.cur.execute(f"SELECT links, last_index FROM links WHERE owner = '{username}' AND link_name = '{link_name}';")
            links = self.cur.fetchall()
            links_len = len(links[0][0].split(","))
            last_index = links[0][1]
            if last_index >= (links_len - 1):
                last_index = 0
            else:
                last_index += 1
            self.cur.execute(f"UPDATE links SET last_index = '{last_index}' WHERE owner = '{username}' AND link_name = '{link_name}';")
            self.conn.commit()
            the_link = links[0][0].split(",")[links[0][1]]
            return f"{the_link}"
        except:
            Controller.error(str(traceback.format_exc()))
            return "ERROR"

    def get_user_links(self, username):
        try:
            self.cur.execute(f"SELECT links, link_name FROM links WHERE owner = '{username}';")
            links = self.cur.fetchall()
            links_objects = []
            for i in links:
                links_objects.append(Link(i[1], i[0].split(",")))
            return links_objects
        except:
            Controller.error(str(traceback.format_exc()))
            return "ERROR"

    def get_user(self, username):
        try:
            self.cur.execute(f"SELECT username FROM users WHERE username = '{username}';")
            user = self.cur.fetchall()[0][0]
            return True
        except:
            return False

    def get_user_password(self, username):
        try:
            self.cur.execute(f"SELECT password_ FROM users WHERE username = '{username}';")
            user_password = self.cur.fetchall()[0][0]
            return user_password
        except:
            Controller.error(str(traceback.format_exc()))
            return "ERROR"

    def get_user_verified(self, username):
        try:
            self.cur.execute(f"SELECT verified FROM users WHERE username = '{username}';")
            user_verified = self.cur.fetchall()[0][0]
            return True
        except:
            return False

    def new_account(self, name, username, email, cellphone, password):
        try:
            self.cur.execute(f"INSERT INTO users (name, username, email, cellphone, password_, vip_time) VALUES ('{name}', '{username}', '{email}', '{cellphone}', '{password}', '{int(time.time()) + 604800}');")
            self.conn.commit()
            return True
        except:
            Controller.error(str(traceback.format_exc()))
            return "ERROR"

    def delete_account(self, username):
        try:
            self.cur.execute(f"DELETE FROM users WHERE username = '{username}';")
            self.conn.commit()
            return True
        except:
            Controller.error(str(traceback.format_exc()))
            return "ERROR"

    def get_user_vip_time(self, username):
        try:
            self.cur.execute(f"SELECT vip_time FROM users WHERE username = '{username}';")
            user_vip_time = self.cur.fetchall()[0][0]
            return user_vip_time
        except:
            Controller.error(str(traceback.format_exc()))
            return "ERROR"

    def set_user_vip_time(self, username, vip_time):
        return