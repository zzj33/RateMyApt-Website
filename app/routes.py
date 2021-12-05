from flask import render_template, request, jsonify
from flask_paginate import Pagination
from app import app
from app import database as db_helper

@app.route("/delete/<int:LPId>", methods=['POST'])
def delete(LPId):
    try:
        db_helper.remove_LivePlace_by_id(LPId)
        result = {'success': True, 'response': 'Removed LivePlace'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/edit/<int:LPId>", methods=['POST'])
def update(LPId):
    print(f"Successfully get EDIT request, LPId={LPId}")
    data = request.get_json()
    print(data)
    try:
        if data:
            if "LPName" in data:
                db_helper.update_LPName_entry(LPId, data["LPName"])
                result = {'success': True, 'response': 'LPName Updated'}
            if "address" in data:
                db_helper.update_address_entry(LPId, data["address"])
                result = {'success': True, 'response': 'address Updated'}
            if "price" in data:
                db_helper.update_price_entry(LPId, data["price"])
                result = {'success': True, 'response': 'price Updated'}
            if "rating" in data:
                db_helper.update_rating_entry(LPId, data["rating"])
                result = {'success': True, 'response': 'rating Updated'}
            if "leaseOption" in data:
                db_helper.update_leaseOption_entry(LPId, data["leaseOption"])
                result = {'success': True, 'response': 'leaseOption Updated'}
            if "website" in data:
                db_helper.update_website_entry(LPId, data["website"])
                result = {'success': True, 'response': 'website Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/create", methods=['POST'])
def create():
    data = request.get_json()
    flag=db_helper.insert_new_LivePlace(data['LPName'], data['address'], data['price'], data['rating'], data['leaseOption'], data['website'])
    if flag>0:
        result = {'success': True, 'response': 'Done'}
    else:
        result = {'success': False, 'response': 'Something went wrong'}
    return jsonify(result)


@app.route('/search/', methods=['GET'])
def search(limit=10):
    keyword=request.args.get("query",type=str,default=None)
    if keyword is None:
        homepage()
        return
    items=db_helper.search_LivePlace(keyword)
    page = int(request.args.get("page", 1))
    start = (page - 1) * limit
    end = page * limit if len(items) > page * limit else len(items)
    paginate = Pagination(page=page, total=len(items))
    items = items[start:end]
    return render_template("index.html", items=items,paginate=paginate)

@app.route("/")
def homepage(limit=10):
    items = db_helper.fetch_LivePlace()
    page = int(request.args.get("page", 1))
    start = (page - 1) * limit
    end = page * limit if len(items) > page * limit else len(items)
    paginate = Pagination(page=page, total=len(items))
    items = items[start:end]
    return render_template("index.html", items=items,paginate=paginate)

@app.route("/q1/")
def q1page():
    """ returns rendered homepage """
    items = db_helper.fetch_q1()
    return render_template("index.html", items=items)

@app.route("/q2/")
def q2page():
    """ returns rendered homepage """
    items = db_helper.fetch_q2()
    return render_template("index.html", items=items)

@app.route("/procedure/", methods=['GET'])
def sp_call(limit=10):
    data=request.args.get("leaseOption")
    print(data)
    items = db_helper.run_procedure(data)
    print(len(items))
    page = int(request.args.get("page", 1))
    start = (page - 1) * limit
    end = page * limit if len(items) > page * limit else len(items)
    paginate = Pagination(page=page, total=len(items))
    items = items[start:end]
    return render_template("index.html", items=items,paginate=paginate)