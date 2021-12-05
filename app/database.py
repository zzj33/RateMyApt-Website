import sqlalchemy
from app import db
from sqlalchemy.exc import OperationalError

def fetch_LivePlace():
    conn = db.connect()
    query_results = conn.execute("Select * from LivePlace;").fetchall()
    conn.close()
    LP_list = []
    for result in query_results:
        item = {
            "LPId": result[0],
            "LPName": result[1],
            "address": result[2],
            "price": result[3],
            "rating": result[4],
            "leaseOption": result[5],
            "distance": result[6],
            "website": result[7][:100]+"......" if len(result[7])>100 else result[7]
        }
        LP_list.append(item)
    return LP_list

def search_LivePlace(keyword:str):
    conn = db.connect()
    search_query="Select * from LivePlace Where LPName Like %s;"
    args=['%'+keyword+'%']
    query_results = conn.execute(search_query,args).fetchall()
    conn.close()
    search_list=[]
    for result in query_results:
        item = {
            "LPId": result[0],
            "LPName": result[1],
            "address": result[2],
            "price": result[3],
            "rating": result[4],
            "leaseOption": result[5],
            "distance": result[6],
            "website": result[7][:100]+"......" if len(result[7])>100 else result[7]
        }
        search_list.append(item)
    return search_list

def fetch_q1():
    conn = db.connect()
    query_results = conn.execute('SELECT LPId, LPName FROM LivePlace natural join CommunityAmenity natural join Model WHERE rating > 4.0 AND distance < 2 Group by ModelId Order by LPName limit 15;').fetchall()
    conn.close()
    q1_list = []
    for result in query_results:
        item = {
            "LPId": result[0],
            "LPName": result[1],
        }
        q1_list.append(item)
    return q1_list


def fetch_q2():
    conn = db.connect()
    query_results = conn.execute('SELECT LPId, LPName FROM comments NATURAL JOIN LivePlace WHERE LPName in (SELECT LPName FROM LivePlace WHERE rating > 3.5) AND price < 900 GROUP BY LPId HAVING COUNT(commentsId) > 2 ORDER BY LPId LIMIT 15;').fetchall()
    conn.close()
    q2_list = []
    for result in query_results:
        item = {
            "LPId": result[0],
            "LPName": result[1],
        }
        q2_list.append(item)
    return q2_list
    
def update_LPName_entry(LPId:int, LPName:str):
    conn = db.connect()
    query = 'Update LivePlace set LPName = "{}" where LPId = {};'.format(LPName,LPId)
    try:
        conn.execute(query)
        print("Success to update name")
    except Exception as e:
        print(e)
    conn.close()


def update_address_entry(LPId:int, address:str):
    conn = db.connect()
    query = 'Update LivePlace set address = "{}" where LPId = {};'.format(address,LPId)
    conn.execute(query)
    conn.close()

def update_price_entry(LPId:int, price:int):
    conn = db.connect()
    query = 'Update LivePlace set price = "{}" where LPId = {};'.format(price,LPId)
    conn.execute(query)
    conn.close()

def update_rating_entry(LPId:int, rating:int):
    conn = db.connect()
    query = 'Update LivePlace set rating = "{}" where LPId = {};'.format(rating,LPId)
    conn.execute(query)
    conn.close()

def update_leaseOption_entry(LPId:int, leaseOption:str):
    conn = db.connect()
    query = 'Update LivePlace set leaseOption = "{}" where LPId = {};'.format(leaseOption,LPId)
    conn.execute(query)
    conn.close()

def update_website_entry(LPId:int, website:str):
    conn = db.connect()
    query = 'Update LivePlace set website = "{}" where LPId = {};'.format(website,LPId)
    conn.execute(query)
    conn.close()

def insert_new_LivePlace(LPName, address, price, rating, leaseOption, website):
    conn = db.connect()
    rst=conn.execute("Select distinct Max(LPId) from LivePlace;")
    rst = [x for x in rst]
    LPId= rst[0][0]+1
    query = 'Insert Into LivePlace (LPId, LPName, address, price, rating, leaseOption, distance, website) VALUES ("{}","{}","{}","{}","{}","{}","{}","{}");'.format(str(LPId), LPName,address,price,rating,leaseOption,"0",website)
    try:
        conn.execute(query)
        query_results = conn.execute("Select LAST_INSERT_ID();")
        query_results = [x for x in query_results]
        LP_id = query_results[0][0]
        conn.close()
        return LP_id
    except:
        conn.close()
        print(-1)
        return -1




def remove_LivePlace_by_id(LPId):
    conn = db.connect()
    query = 'Delete From LivePlace where LPId={};'.format(LPId)
    conn.execute(query)
    conn.close()

def run_procedure(leaseOption):
    conn=db.connect()
    command="call Result('{}');".format(leaseOption)
    sp_results=conn.execute(command).fetchall()
    conn.close()
    sp_rst_list=[]
    for result in sp_results:
        item = {
            "LPId": result[0],
            "LPName": result[1],
            "address": result[2],
            "price": result[3],
            "rating": result[4],
            "leaseOption": result[5],
            "distance": result[6],
            "website": result[7][:100]+"......" if len(result[7])>100 else result[7]
        }
        sp_rst_list.append(item)
    print(len(sp_rst_list))
    return sp_rst_list






