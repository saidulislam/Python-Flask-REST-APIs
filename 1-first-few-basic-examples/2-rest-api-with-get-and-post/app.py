from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [{
    'name': 'My Store',
    'items': [{'name':'my item', 'price': 15.99 }]
}]


# index/home page
@app.route('/')
def home():
    return render_template('index.html')


# CREATE
# POST /store data: {name:}
@app.route('/store' , methods=['POST'])
def create_store():
    request_data = request.get_json()
    print("\n*************** request ****************\n")
    print(request_data)
    print("\n\n")
    
    new_store = {
        'name': request_data['name'],
        'item': []
    }

    stores.append(new_store)
    return jsonify(new_store)


# RETRIEVE
# GET /store/<name> data: {name :}
@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'store not found'})


#GET /store
@app.route('/store')
def get_stores():
    print("\n*************** data ****************\n")
    print(stores)
    print("\n\n")
    return jsonify({'stores': stores})


#POST /store/<name> data: {name :}
@app.route('/store/<string:name>/item' , methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    print("\n*************** request ****************\n")
    print(request_data)
    print("\n\n")

    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message' : 'store not found'})


#GET /store/<name>/item data: {name :}
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items' : store['items']})
    return jsonify({'message': 'store not found'})


if __name__ == '__main__':
    app.run(debug=True)