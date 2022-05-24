import traceback
from colorama import Fore, Style
from scripts.general import General
from scripts.variables import Vars
from scripts.models import Link
import psycopg2
import os

class Database:

    def __init__(self, host, database, user, password):
        try:
            self.conn = psycopg2.connect(os.environ["DATABASE_URL"], sslmode = "require")
        except:
            self.conn = psycopg2.connect(host = host, database = database, user = user, password = password)
        self.cur = self.conn.cursor()

    def new_link(self, link_name, links, owner):
        try:
            self.cur.execute(f"SELECT LINK_NAME FROM LINKS WHERE LINK_NAME = '{link_name}' and OWNER = '{owner}';")
            selected = self.cur.fetchall()
            if len(selected) == 0:
                self.cur.execute(f"INSERT INTO LINKS (LINK_NAME, LINKS, LAST_INDEX, OWNER) VALUES ('{link_name}', '{links}', '0', '{owner}');")
                self.conn.commit()
                return f"ACTION = 'INSERTED IN DATABASE'<br>LINK IS: '{Vars.app_link}/redirect?id={link_name}'"
            else:
                self.cur.execute(f"UPDATE LINKS SET LINKS = '{links}', LAST_INDEX = '0' WHERE LINK_NAME = '{link_name}';")
                self.conn.commit()
                return f"ACTION = 'UPDATED IN DATABASE'<br>LINK IS: '{Vars.app_link}/redirect?id={link_name}'"
        except:
            General.error(str(traceback.format_exc()))
            return "ERROR"

    def delete_link(self, link_name, owner):
        try:
            self.cur.execute(f"DELETE FROM LINKS WHERE LINK_NAME = '{link_name}' and OWNER = '{owner}';")
            self.conn.commit()
            return "SUCCESFUL DELETE!"
        except:
            General.error(str(traceback.format_exc()))
            return "ERROR"

    def get_links(self, username, link_name):
        try:
            self.cur.execute(f"SELECT LINKS, LAST_INDEX FROM LINKS WHERE OWNER = '{username}' and LINK_NAME = '{link_name}';")
            links = self.cur.fetchall()
            links_len = len(links[0][0].split(","))
            last_index = links[0][1]
            if last_index >= (links_len - 1):
                last_index = 0
            else:
                last_index += 1
            self.cur.execute(f"UPDATE LINKS SET LAST_INDEX = '{last_index}' WHERE OWNER = '{username}' and link_name = '{link_name}';")
            self.conn.commit()
            the_link = links[0][0].split(",")[links[0][1]]
            return f"{the_link}"
        except:
            General.error(str(traceback.format_exc()))
            return "ERROR"

    def get_user_links(self, username):
        try:
            self.cur.execute(f"SELECT LINKS, LINK_NAME FROM links WHERE OWNER = '{username}';")
            links = self.cur.fetchall()
            links_objects = []
            for i in links:
                links_objects.append(Link(i[1], i[0].split(",")))
            return links_objects
        except:
            General.error(str(traceback.format_exc()))
            return "ERROR"

    def get_redirections_info(self, username, link_name):
        self.cur.execute(f"SELECT UNIQUE_CLIENTS_EVER, UNIQUE_CLIENTS_24HRS, UNIQUE_REDIRECTIONS_EVER, UNIQUE_REDIRECTIONS_24HRS, CLIENTS_EVER, CLIENTS_24HRS FROM links WHERE OWNER = '{username}' and LINK_NAME = '{link_name}';")
        info = self.cur.fetchall()
        info = f"UNIQUE_CLIENTS_REQUESTS:{len(Vars.clients)}<br>UNIQUE_REDIRECTIONS:{Vars.total_redirections}<br><br>"
        for i in Vars.redirections.keys():
            info = info + f"'{i}':{Vars.redirections[i]}<br>"
        return info