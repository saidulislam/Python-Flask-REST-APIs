from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'asewergadfgaergtergsdfgsdfg'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )


    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {f'message': "An item with name {name} already exists"}, 400

        data = Item.parser.parse_args()
        
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201 # error code 201 is for Created
    
    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] == name, items))
        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        # Once again, print something not in the args to verify everything works
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/item/chair
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(debug=True)