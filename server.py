from flask import Flask, render_template, request, url_for, Response
from objects.owner import Owner
from objects.item import Item
from database.methods import insert, OwnerAlreadyExists, get_owners
import os

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

items = []


@app.route('/')
def root():
    owners = get_owners()
    categories = ["Fitness", "Beauty"]
    return render_template('index.html', owners=owners,categories=categories)


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/category')
def sort_category():
    cat = request.args.get('cat')
    owners = get_owners(cat)
    return render_template('index.html', owners=owners)


@app.route("/submit", methods=['GET'])
def do_search():
    global items
    full_name = request.args.get('fullName')
    email = request.args.get('email')
    phone_number = request.args.get('mobileNo')
    description = request.args.get('comment')
    busninessType = request.args.get('busninessType')
    img_url = request.args.get('itemUrl')
    owner = Owner(full_name, email, phone_number, description, busninessType, img_url)
    try:
        insert(owner, items)
    except OwnerAlreadyExists as e:
        return "owner already exists"
    items = []
    owners = get_owners()
    return render_template('index.html', owners=owners)


@app.route("/add_item", methods=['GET'])
def add_item():
    global items
    item_name = request.args.get('itemName')
    price = request.args.get('Price')
    item_url = request.args.get('itemUrl')
    description = request.args.get('comment')
    item = Item(item_name, price, item_url, description)
    items.append(item)
    return Response("", 204)


@app.route('/register', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        url = os.path.join('Images/', uploaded_file.filename)
        a = uploaded_file.save(url)

    return ""


if __name__ == '__main__':
    app.run(port=3000)
