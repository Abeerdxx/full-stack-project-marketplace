from flask import Flask, render_template, request, url_for, Response
from objects.owner import Owner
from objects.item import Item
from database.methods import insert, OwnerAlreadyExists, get_owners, get_items, get_categories
import os

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

items = []


@app.route('/')
def root():
    owners = get_owners()
    categories = [x['categories'] for x in get_categories()]
    categories.append("All")
    return render_template('index.html', owners=owners, categories=categories)


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/about')
def about():
    id = request.args.get('id')
    owner_items = get_items(id)

    print(owner_items)
    return render_template('about.html', owner_items=owner_items)


@app.route('/category')
def sort_category():
    cat = request.args.get('cat')
    if cat == 'All':
        owners = get_owners()
    else:
        owners = get_owners(cat)
    categories = [x['categories'] for x in get_categories()]
    categories.append("All")
    return render_template('index.html', owners=owners, categories=categories)


@app.route("/submit", methods=['GET'])
def do_search():
    global items
    full_name = request.args.get('fullName')
    email = request.args.get('email')
    city = request.args.get('city')
    zip_code = request.args.get('zip_code')
    phone_number = request.args.get('mobileNo')
    busninessType = request.args.get('busninessType')
    description = request.args.get('comment')
    img_url = request.args.get('itemUrl')
    owner = Owner(full_name, email, city, zip_code, phone_number, busninessType, description, img_url)
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
        img_url = os.path.join('Images/', uploaded_file.filename)
        a = uploaded_file.save(img_url)

    return ""


if __name__ == '__main__':
    app.run(port=3000)
