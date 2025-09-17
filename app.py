# PS C:\Users\ayush\Desktop\Flask> virtualenv env
# PS C:\Users\ayush\Desktop\Flask> .\env\Scripts\activate.ps1
# (env) PS C:\Users\ayush\Desktop\Flask> pip install flask
# Make sure u run python file inside virtual env only, otherwise error as modules installed will be present inside virtual env only
# We can also read the static files by http://127.0.0.1:5000/static/ayush.txt

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    # return "Hello World!"
    return render_template("index.html")

@app.route("/products")
def products():
    return "This is products page"

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=True, port=8000)    # if want to change the port