from flask import Flask, render_template, request, redirect, session, url_for
from scripts.variables import Vars
from scripts.general import General
from scripts.no_sql_injection import NoSqlInjection
from scripts.hash import Hash
from scripts.db import Database
from colorama import Fore, Style
import os
import json


app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")

@app.route("/")
def index():
    if "session_user" not in session or session['session_user'] == None:
        return redirect(url_for("login", next_page=url_for("index")))
    return render_template("index.html", app_link=Vars.app_link, my_links=Vars.db.get_user_links(session['session_user']))

@app.route("/create-link")
def create_link():
    if "session_user" not in session or session['session_user'] == None:
        return redirect(url_for("login", next_page=url_for("create_link")))
    return render_template("create_link.html", initial_link_input_value=Vars.initial_link_input_value, app_link=Vars.app_link)

@app.route("/access/<username>/<link_name>")
def redirect_client(username = None, link_name = None):
    redirect_link = Vars.db.get_links(username, link_name)
    print(redirect_link)
    if redirect_link == "ERROR":
        return render_template("action_result.html", result=redirect_link), {"Refresh": f"5; url={request.path}"}
    else:
        return redirect(redirect_link)

@app.route("/new-link", methods=['POST',])
def new_link():
    if "session_user" not in session or session['session_user'] == None:
        return redirect(url_for("login", next_page=url_for("index")))
    link_name = request.form['link_name']
    links = ""
    form_len = len(request.form)
    for index, i in enumerate(request.form):
        if i == "link_name":
            continue
        elif index == (form_len - 1):
            continue
        else:
            new_link = str(request.form[i].replace(" ", "%20"))
            if NoSqlInjection.verify_message([new_link]) == False:
                General.error("SQL_INJECTION_NEW_LINK") 21
                return render_template("action_result.html", result="SQL_INJECTION_NEW_LINK"), {"Refresh": "5; url=/"}
            links = f"{links},{new_link}"
    return render_template("action_result.html", result=Vars.db.new_link(link_name, links, session['session_user'])), {"Refresh": "5; url=/"}

@app.route("/delete/<username>/<link_name>")
def delete_link(username = None, link_name = None):
    if "session_user" not in session or session['session_user'] == None:
        return redirect(url_for("login", next_page=url_for("index")))
    if username != session['session_user']:
        return render_template("action_result.html", result="PERMISSION_DENIED"), {"Refresh": "5; url=/"}
    if NoSqlInjection.verify_message([link_name]) == False:
        General.error("SQL_INJECTION_DELETE_LINK")
        return render_template("action_result.html", result="SQL_INJECTION_DELETE_LINK"), {"Refresh": "5; url=/"}
    return render_template("action_result.html", result=Vars.db.delete_link(link_name, session['session_user'])), {"Refresh": "5; url=/"}

@app.route("/info/<username>/<link_name>")
def info_link(username = None, link_name = None):
    if "session_user" not in session or session['session_user'] == None:
        return redirect(url_for("login", next_page=url_for("redirections_info")))
    if username != session['session_user']:
        return render_template("action_result.html", result="PERMISSION_DENIED"), {"Refresh": "5; url=/"}
    if NoSqlInjection.verify_message([link_name]) == False:
        General.error("SQL_INJECTION_INFO_LINK")
        return render_template("action_result.html", result="SQL_INJECTION_INFO_LINK"), {"Refresh": "5; url=/"}
    return render_template("redirections-info.html")

@app.route("/login")
def login():
    next_page = request.args.get("next_page")
    return render_template("login.html", next_page=next_page)

@app.route("/authenticate", methods=['POST',])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    next_page = request.form['next_page']
    try:
        if NoSqlInjection.verify_message([username, password, next_page]) == False:
            General.error("SQL_INJETION_LOGIN")
            return render_template("action_result.html", result="SQL_INJECTION_LOGIN"), {"Refresh": "5; url=/"}
        Vars.postgre_connection_cursor.execute(f"SELECT username, password_ FROM users WHERE username = '{username}';")
        user_info = Vars.postgre_connection_cursor.fetchall()
        try:
            Hash.verify_hash(password, user_info[0][1])
        except:
            raise Exception("WRONG_USERNAME_OR_PASSWORD")
        session['session_user'] = username
        if next_page == "None":
            return redirect(url_for("index"))
        else:
            return redirect(next_page)
    except Exception as e:
        General.error(str(e), f"username: '{request.form['username']}'\nip: '{request.remote_addr}'")
        return render_template("action_result.html", result="WRONG_USERNAME_OR_PASSWORD"), {"Refresh": f"5; url={url_for('login', next_page=next_page)}"}

@app.route("/logout")
def logout():
    session['session_user'] = None
    return redirect(url_for("login"))

@app.route("/register")
def register():
    if "session_user" not in session or session['session_user'] == None:
        return
    else:
        return redirect(url_for("login", next_page=url_for("index")))

@app.route("/create-account", methods=['POST',])
def create_account():
    return

@app.errorhandler(404)
def handle_404(error):
    return "Page Not Found"

if __name__ == "__main__":
    os.system("cls")
    Vars.db = Database(host = os.environ['link_switch_db_host'], database = os.environ['link_switch_db_name'], user = os.environ['link_switch_db_user'], password = os.environ['link_switch_db_password'])
    print(f"WEBSERVER VERSION IS {Vars.version}")
    # app.run(host="0.0.0.0", port=Vars.server_port, debug=True, ssl_context="adhoc")
    app.secret_key = os.environ['link_switch_secret_key']
    app.run(host="0.0.0.0", port=Vars.server_port, debug=True)
