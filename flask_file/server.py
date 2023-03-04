from flask import render_template,request,Blueprint,redirect,session
from db_control import show_db,insert_db,delete_db,update_db,now_time
import os

bp =Blueprint("server",__name__)

@bp.route("/",methods=["GET","POST"])
def index():
    #print(f"##heders##\n{request.headers}")
    print(f"##referrer##:\n{request.referrer}")
    #print(f"##access_root##:\n{request.access_route}")
    # print(os.system("dir"))

    if request.referrer == None:
        session["log_text"] = None
        session["log"] = None
    # request.referrerがNoneにならない場合、session["log"]が無いためにKeyErrorになる。
    if session["log"] == []:
        session["log"] = None

    if request.method == "GET":
        select = request.args.get("select")
        if select:
            session["log_text"] = None
            session["log"] = None
        return render_template("index.html",select=select,log_text=session["log_text"],now_time=now_time(),logs=session["log"],posts=show_db())

    if request.method == "POST": 
        sql_cmd = request.form.get("sql_cmd")

        if sql_cmd == "insert":
            insert_text = request.form.get("insert_text")
            insert_db(insert_text)
            session["log"] = [show_db()[-1]]
            
        elif sql_cmd == "delete":
            delete_id = request.form.getlist("delete_id")
            session["log"] = [i for i in show_db() if i["key"] in delete_id]
            [delete_db(i) for i in delete_id]

        elif sql_cmd == "update":
            update_texts = request.form.getlist("update_texts")
            update_id = request.form.getlist("update_id")

            db_items = show_db().copy()
            update_id_list =[]
            for i in range(len(update_texts)):
                if db_items[i]["key"] == update_id[i] and db_items[i]["text"] != update_texts[i]:
                    update_id_list.append(db_items[i]["key"])
                    update_db(update_id[i],update_texts[i]) 
            session["log"] = [i for i in show_db() if i["key"] in update_id_list]
        

        session["log_text"] = sql_cmd

        return redirect(location="/")

