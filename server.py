from flask import Flask, render_template, request, url_for
from objects.owner import Owner
from objects.item import Item
from database.methods import insert, OwnerAlreadyExists
import os

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

items = []

@app.route('/')
def root():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route("/submit", methods=['GET'])
def do_search():
    global items
    full_name = request.args.get('fullName')
    email = request.args.get('email')
    phone_number = request.args.get('mobileNo')
    description = request.args.get('comment')
    owner = Owner(full_name, email, phone_number, description)
    try:
        insert(owner, items)
    except OwnerAlreadyExists as e:
        return "owner already exists"
    items = []
    return "form_data: {0}, {1}, {2}, {3}".format(full_name, email, phone_number, description)


@app.route("/add_item", methods=['GET'])
def add_item():
    global items
    item_name = request.args.get('itemName')
    price = request.args.get('Price')
    item_url = request.args.get('itemUrl')
    description = request.args.get('comment')
    item = Item(item_name, price, item_url, description)
    items.append(item)
    return "form_data: {0}, {1}, {2}, {3}".format(item_name, price, item_url, description)


@app.route('/register', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        url = os.path.join('Images/', uploaded_file.filename)
        a = uploaded_file.save(url)

    return ""


if __name__ == '__main__':
    app.run(port=3000)
