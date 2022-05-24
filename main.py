from flask import Flask, flash, render_template, request, redirect, session, url_for
from scripts.variables import Vars
from scripts.controller import Controller
from scripts.db import Database
from colorama import Fore, Style
import os
from datetime import datetime
import json


app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")

@app.route("/")
def index():
    if "session_user" not in session or session['session_user'] == None:
        return redirect(url_for("login"))
    user_vip_time = datetime.utcfromtimestamp(int(Vars.db.get_user_vip_time(session['session_user']))).strftime('%d/%m/%Y - %H:%M:%S')
    return render_template("index.html", app_link=Vars.app_link, my_links=Vars.db.get_user_links(session['session_user']), vip_time=user_vip_time)

@app.route("/create-link")
def create_link():
    if "session_user" not in session or session['session_user'] == None:
        return redirect(url_for("login"))
    return render_template("create_link.html", initial_link_input_value=Vars.initial_link_input_value, app_link=Vars.app_link)

@app.route("/create-link/new", methods=['POST',])
def new_link():
    if "session_user" not in session or session['session_user'] == None:
        return redirect(url_for("login"))
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
            sql_injection = Controller.verify_response([new_link])
            if sql_injection == True:
                Controller.error("SQL_INJECTION_NEW_LINK")
                return render_template("action_result.html", result="SQL_INJECTION_NEW_LINK"), {"Refresh": "5; url=/"}
            elif len(new_link) > 150:
                Controller.error("LINK_TOO_BIG")
                return render_template("action_result.html", result="LINK_TOO_BIG"), {"Refresh": "5; url=/"}
            links = f"{links},{new_link}"
    return render_template("action_result.html", result=Vars.db.new_link(link_name, links, session['session_user'])), {"Refresh": "5; url=/"}

@app.route("/access/<username>/<link_name>")
def redirect_client(username = None, link_name = None):
    redirect_link = Vars.db.get_links(username, link_name)
    if redirect_link == "ERROR":
        return render_template("action_result.html", result=redirect_link), {"Refresh": f"5; url={request.path}"}
    else:
        return redirect(redirect_link)

@app.route("/delete/<username>/<link_name>")
def delete_link(username = None, link_name = None):
    if "session_user" not in session or session['session_user'] == None:
        return redirect(url_for("login"))
    if username != session['session_user']:
        return render_template("action_result.html", result="PERMISSION_DENIED"), {"Refresh": "5; url=/"}
    sql_injection = Controller.verify_response([link_name])
    if sql_injection == True:
        Controller.error("SQL_INJECTION_DELETE_LINK")
        return render_template("action_result.html", result="SQL_INJECTION_DELETE_LINK"), {"Refresh": "5; url=/"}
    return render_template("action_result.html", result=Vars.db.delete_link(link_name, session['session_user'])), {"Refresh": "5; url=/"}

@app.route("/info/<username>/<link_name>")
def info_link(username = None, link_name = None):
    if "session_user" not in session or session['session_user'] == None:
        return redirect(url_for("login"))
    if username != session['session_user']:
        return render_template("action_result.html", result="PERMISSION_DENIED"), {"Refresh": "5; url=/"}
    sql_injection = Controller.verify_response([link_name])
    if sql_injection == True:
        Controller.error("SQL_INJECTION_INFO_LINK")
        return render_template("action_result.html", result="SQL_INJECTION_INFO_LINK"), {"Refresh": "5; url=/"}
    return render_template("redirections-info.html")

@app.route("/update/<username>/<link_name>")
def update_link(username = None, link_name = None):
    if "session_user" not in session or session['session_user'] == None:
        return redirect(url_for("login"))
    if username != session['session_user']:
        return render_template("action_result.html", result="PERMISSION_DENIED"), {"Refresh": "5; url=/"}
    return

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        try:
            sql_injection = Controller.verify_response([username, password])
            if sql_injection == True:
                Controller.error(f"{sql_injection}")
                flash(f"{sql_injection}", "ERROR")
                return redirect(url_for("login"))
            if Vars.db.get_user(username) == False:
                flash(f"Wrong username.", "ERROR")
                return redirect(url_for("login"))
            if Controller.verify_hash(password, Vars.db.get_user_password(username)) == False:
                flash(f"Wrong password.", "ERROR")
                return redirect(url_for("login"))
            session['session_user'] = username
            flash(f"Logged in successfully.")
            return render_template("login.html"), {"Refresh": "5; url=/"}
        except Exception as e:
            Controller.error(str(e), f"username: '{request.form['username']}'\nip: '{request.remote_addr}'")
            return render_template("action_result.html", result="WRONG_USERNAME_OR_PASSWORD"), {"Refresh": f"5; url={url_for('login')}"}

@app.route("/logout", methods=['GET'])
def logout():
    session['session_user'] = None
    return redirect(url_for("login"))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        cellphone = request.form['cellphone'].upper().strip("-()ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        password = request.form['password']
        sql_injection = Controller.verify_response([name, username, email, cellphone, password])
        if sql_injection == True:
            Controller.error(f"{sql_injection}")
            flash(f"{sql_injection}", "ERROR")
            return redirect(url_for("register"))
        if len(cellphone) < 8:
            flash("Incorrect cellphone.", "ERROR")
            return redirect(url_for("register"))
        if "@" not in email:
            flash("Incorrect email.", "ERROR")
            return redirect(url_for("register"))
        if len(password) < 6:
            flash("Password needs at least 6 characters.", "ERROR")
            return redirect(url_for("register"))
        if Vars.db.get_user(username) == True:
            flash("Username already exists.", "ERROR")
            return redirect(url_for("register"))
        if len(name) > 50:
            flash("Name too big.", "ERROR")
            return redirect(url_for("register"))
        if len(username) > 30:
            flash("Username too big.", "ERROR")
            return redirect(url_for("register"))
        if len(email) > 40:
            flash("Email too big.", "ERROR")
            return redirect(url_for("register"))
        if len(cellphone) > 20:
            flash("Cellphone too big.", "ERROR")
            return redirect(url_for("register"))
        if len(password) > 50:
            flash("Password too big.", "ERROR")
            return redirect(url_for("register"))
        Vars.db.new_account(name, username, email, cellphone, Controller.generate_hash(password))
        flash("Account created successfully.")
        return redirect(url_for("register"))

@app.errorhandler(404)
def handle_404(error):
    return "Page Not Found"

if __name__ == "__main__":
    os.system("cls")
    Vars.db = Database(host = os.environ['link_switch_db_host'], database = os.environ['link_switch_db_name'], user = os.environ['link_switch_db_user'], password = os.environ['link_switch_db_password'])
    print(f"WEBSERVER VERSION IS {Vars.version}")
    app.secret_key = os.environ['link_switch_secret_key']
    app.run(host="0.0.0.0", port=Vars.server_port, debug=True) # ssl_context="adhoc"
