
import os
from flask import Flask, redirect, url_for, request, Response, jsonify, render_template
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
import urllib3
import json


app = Flask(__name__)

client = MongoClient()
db = client.myretail


@app.route("/products/<int:product_id>", methods=['GET', 'PUT'])
def get_product(product_id):
    """
    Function for Products
    """

    try:

        if request.method == "GET":
            products_obj = db.product.find({"product_id": product_id})
            if products_obj.count() == 0:
                return jsonify(error=404, text="Not Found"), 404  # Product_id not found in MongoDB

            status, name = get_name_from_redsky(product_id=product_id)
            if status != 200:
                return jsonify(error=status, text=name), status   # for given Product ID, name not found in redsky

            product_doc = {                                   # Creating Json dynamically / aggregating it for response
                'product_id': product_id,
                'name': name,
                'current_price': {
                    'currency_code': products_obj[0]['current_price']['currency_code'],
                    'value': products_obj[0]['current_price']['value']
                }
            }

            return jsonify(product_doc)

        if request.method == "PUT":
            status, product_doc = update_price(request)
            if status != 200:
                return jsonify(error=status, text=product_doc), status   # for given Product ID, name not found in redsky

            return Response(dumps(product_doc), mimetype='application/json')


    except Exception as error:
        return jsonify(error=502, text="Unknown Error {0}".format(error)), 502


def get_name_from_redsky(product_id):

    try:

        url = "https://redsky.target.com/v2/pdp/tcin/{0}?excludes=taxonomy,price,promotion,bulk_ship,rating_and_review_reviews,rating_and_review_statistics,question_answer_statistics".format(product_id)
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        if 200 == response.status:                     # checks Get successness with redskys
            json_obj = json.loads(response.data.decode('utf8'))
            for i in json_obj:
                name = json_obj[i]['item']['product_description']['title']
            return 200, name
        else:
            return response.status, response.reason   # if redsky didn't provide no response then print status & reason

    except Exception as ex:                        # handle unknow expections from redsky
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return 500, "Internal Server Error"


def update_price(request):

    try:

        req_data = request.get_json()
        if req_data is None:
            return 500, "Request was invalid"

        products_obj = db.product.update(
            {
              'product_id': req_data['product_id']
            },
            {
                "$set":
                {
                    'current_price': {
                        'currency_code': req_data['current_price']['currency_code'],
                        'value': req_data['current_price']['value']
                    }
                }
            })
        if  products_obj["nModified"] == 0:
            return 404, "Not Found"

        product_doc = db.product.find({"product_id": req_data['product_id']}, {"_id": 0, "product_id": 0, "name": 0})
        if product_doc.count() == 0:
            return 404, "Not Found"

        return 200, product_doc

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return 500, "Internal Server Error"


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
