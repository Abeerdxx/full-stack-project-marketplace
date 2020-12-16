from flask import Flask, render_template,request

app = Flask(__name__, static_url_path='',static_folder='static',template_folder='templates')


@app.route('/')
def root():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route("/submit", methods = ['GET'])
def do_search():
    full_name = request.args.get('fullName')
    email = request.args.get('email')
    phone_number = request.args.get('mobileNo')
    description = request.args.get('comment')
  
   
    return "form_data: {0}, {1}, {2}, {3}".format(full_name, email, phone_number ,description)

if __name__ == '__main__':
    app.run(port=3000)