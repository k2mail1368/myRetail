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
            url = "https://redsky.target.com/v2/pdp/tcin/{0}?excludes=taxonomy,price,promotion,bulk_ship,rating_and_review_reviews,rating_and_review_statistics,question_answer_statistics".format(product_id)
            http = urllib3.PoolManager()
            response = http.request('GET', url)
            json_obj = json.loads(response.data.decode('utf8'))
            for i in json_obj:
                name = json_obj[i]['item']['product_description']['title']
                product_doc = db.product.find({"product_id":product_id})
                db.product.update(
                    {
                        '_id': ObjectId(product_doc[0]['_id'])
                    },
                    {
                        "$set":
                            {
                                'name': name,
                                'current_price': {
                                    'currency_code': product_doc[0]['current_price']['currency_code'],
                                    'value': product_doc[0]['current_price']['value']
                                }
                            }
                    })

                product_doc = db.product.find({"product_id": product_id}, {"_id": 0})

            return Response(dumps(product_doc), mimetype='application/json')

        if request.method == "PUT":
            req_data = request.get_json()

            db.product.update(
                {
                  'product_id': req_data['product_id']
                },
                {
                    "$set":
                    {
                        'product_id': req_data['product_id'],
                        'name': req_data['name'],
                        'current_price': {
                            'currency_code': req_data['current_price']['currency_code'],
                            'value': req_data['current_price']['value'],
                        }
                    }
                })

            product_doc = db.product.find({"product_id": req_data['product_id']}, {"_id": 0})

            return Response(dumps(product_doc), mimetype='application/json')

        return jsonify(error=500, text="Invalid HTTP Verb"), 500

    except TypeError as error:
        return jsonify(error=501, text="I/O error: {0}".format(error)), 501

    except Exception as error:
        return jsonify(error=502, text="I/O error: {0}".format(error)), 502


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
