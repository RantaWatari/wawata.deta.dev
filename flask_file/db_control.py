import datetime
from deta import Deta

def get_db():
    db = Deta(project_key="c0h15t2h_LsJsyUoSd4n3heSzCaC2S82twuCv1wrV")
    db = db.Base(name="flask_file")
    return db

def show_db():
    db = get_db()
    fetch_data = db.fetch()
    
    #(3)
    try:  
        ## Usefull only deploy enviroment
        for i in fetch_data:
            datas = i
        posts = []
        for j in datas:
            posts.append(j)

    except TypeError:
        ## Usefull Only local enviroment
        posts = fetch_data.items

    posts = posts.copy()

    posts = sort(posts)
    # データ確認用
    #[print(i) for i in posts]

    return posts

def sort(posts_unsorted): 
    # データ確認用
    #[print(i) for i in posts]
    posts_copy = posts_unsorted.copy()
    #[[print(pp[i]["time"][j],end=" ") for j in range(len(pp[i]["time"]))] for i in range(len(pp))]
    #print(type(posts[0]["time"][0]),type(posts[0]["time"][6]))
    sort_p = {}
    for i in range(len(posts_unsorted)):
        bind_time = ""
        for j in posts_unsorted[i]["time"]:
            bind_time = bind_time + str(j)
        sort_p[int(bind_time)] = posts_unsorted[i]["key"]
    
    #print(sort_p)
    sort_in = sorted(sort_p)
    #print(sort_in)
    sorted_index = [sort_p[i] for i in sort_in]

    posts_sorted = []
    for i in sorted_index:
        for j in posts_copy:
            if j["key"] == i: posts_sorted.append(j)

    return posts_sorted

def now_time():
    now_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))) 
    now_time_tuple = now_time.timetuple()
    now = []
    
    for i in range(len(now_time_tuple[:6])):
        time = str(now_time_tuple[i])
        if i == 0 :
            time = time.zfill(4)
        else:
            time = time.zfill(2)
        now.append(time)
    # year~microsecond 
    time = (str(now_time.microsecond))
    now.append(time.zfill(6))
    return now



def insert_db(insert_text):
    post = show_db()
    p = [int(post[i]["key"]) for i in range(len(post))]
    post_max = max(p)
    key = str(post_max+1)

    time = now_time()

    # (1),(2)
    get_db().put({ 
       "key": key,
       "time": time,
       "text": insert_text,
    })
    
def delete_db(delete_key):
    get_db().delete(delete_key)
    
def update_db(update_key,update_text):

    time = now_time()
    get_db().update({
        "time": time,
        "text": update_text
    },update_key)
