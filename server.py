from flask import Flask, render_template, request, session, Response, redirect, url_for
from objects.owner import Owner
from objects.user import User
from objects.item import Item
from database.methods import *
from loginrsa import *
import os

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
app.secret_key = "BL0ckN0nAdmIN"
app.config['SECRET_KEY'] = app.secret_key
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


@app.route('/edit/<name>', methods=['GET'])
def edit(name):
    item = get_items(session["user_email"], name)[0]
    return render_template('edit_item.html', item=item)


@app.route('/edit/<name>', methods=['POST'])
def edit_item(name):
    data = request.form
    # if data["img_url"]:
    #     update_img(data["img_url"])
    update_item(data, session["user_email"], name)
    return redirect(url_for('about', em=session["user_email"]))


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
    return render_template('about_owner.html', owner_items=owner_items, owner=owner, var=template)

@app.route('/compare')
def compare():
    left = request.args.get('left')
    right = request.args.get('right')
    left_items = None
    right_items = None
    try:
        left_items = get_items(left)
        right_items = get_items(right)
    except:
        pass
    left_owner = get_owner(left)
    right_owner = get_owner(right)
    return render_template('comparison.html', var=template, left_items=left_items, right_items=right_items, left_owner=left_owner, right_owner=right_owner)

@app.route('/messages')
def messages():
    email = request.args.get('em')
    messages = None
    # try:
    # owner_items = get_items(email)
    # except:
    # pass
    return render_template('messages.html', var=template)


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


@app.route('/login', methods=['POST'])
def login_user():
    global template
    data = request.form
    email = data["email"]
    password = data["password"]
    try:
        res = is_owner(email, password)
        if res:
            session['user_email'] = email
            template = "masterpage_loggedin.html"
    except OwnerDoesntExist:
        return root()
    return root()


@app.route("/register/owner", methods=['GET'])
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
    return redirect(url_for('root'))


@app.route("/register/user")
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
        return Response("User already exists")
    return redirect(url_for('root'))


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
