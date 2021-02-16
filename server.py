from flask import Flask, render_template, request, session, Response, redirect, url_for
from objects.owner import Owner
from objects.user import User
from objects.item import Item
from database.methods import *
import os

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
app.secret_key = "BL0ckN0nAdmIN"
items = []
template = "masterpage.html"

@app.route('/')
def root():
    owners = get_owners()
    categories = [x['categories'] for x in get_categories()]
    categories.append("All")
    return render_template('index.html', owners=owners, categories=list(set(categories)), var=template)


@app.route('/register')
def register():
    return render_template('main_register.html')


@app.route('/logout')
def logout():
    global template
    session.pop('user_email', None)
    template = "masterpage.html"
    return redirect(url_for('root'))


@app.route('/about')
def about():
    email = request.args.get('em')
    owner_items = None
    try:
        owner_items = get_items(email)
    except:
        pass
    owner = get_owner(email)
    return render_template('about_owner.html', owner_items=owner_items, owner=owner)


@app.route('/category')
def sort_category():
    cat = request.args.get('cat')
    if cat == 'All':
        owners = get_owners()
    else:
        owners = get_owners(cat)
    categories = [x['categories'] for x in get_categories()]
    categories.append("All")
    return render_template('index.html', owners=owners, categories=list(set(categories)), var=template)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login/user')
def login_user():
    global template
    email = request.args.get('email')
    password = request.args.get('password')
    try:
        res = is_owner(email, password)
        if res:
            session['user_email'] = email
            template = "masterpage_loggedin.html"
    except OwnerDoesntExist:
        return root()
    return root()


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
    password = request.args.get('password')
    owner = Owner(full_name, email, city, zip_code, phone_number, busninessType, description, img_url, password)
    try:
        insert(owner, 0, items)
    except UserAlreadyExists as e:
        return "User already exists"
    items = []
    return root()


@app.route("/user_submit")
def register_user():
    full_name = request.args.get('fullName')
    email = request.args.get('email')
    city = request.args.get('city')
    zip_code = request.args.get('userzip_code')
    phone_number = request.args.get('usermobileNo')
    img_url = request.args.get('itemUrl')
    password = request.args.get('password')
    user = User(full_name, email, city, zip_code, phone_number, img_url, password)
    try:
        insert(user, 1)
    except UserAlreadyExists as e:
        return "User already exists"
    return root()


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
