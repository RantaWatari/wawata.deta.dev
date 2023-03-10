from flask import render_template,request,Blueprint
from db_control import show_db,insert_db,delete_db,update_db

bp =Blueprint("server",__name__)

@bp.route("/",methods=["GET","POST"])
def index():
    if request.method == "GET":
        select = request.args.get("select")
        return render_template("index.html",select=select,posts=show_db())

    if request.method == "POST":
        sql_cmd = request.form.get("sql_cmd")

        if sql_cmd == "insert":
            insert_text = request.form.get("insert_text")
            insert_db(insert_text)
            
        elif sql_cmd == "delete":
            delete_id = request.form.getlist("delete_id")
            [delete_db(i) for i in delete_id]

        elif sql_cmd == "update":
            update_texts = request.form.getlist("update_texts")
            update_id = request.form.getlist("update_id")

            db_items = show_db().copy()
            for i in range(len(update_texts)):
                if db_items[i]["key"] == update_id[i] and db_items[i]["text"] != update_texts[i]:
                    update_db(update_id[i],update_texts[i])
                    #確認用
                    #print(f"update i={i},id={update_id[i]},text={update_texts[i]}")

        else:
            pass

        return render_template("index.html",posts=show_db())