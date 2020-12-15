from flask import Flask, render_template

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
if __name__ == '__main__':
    app.run(port=3000)