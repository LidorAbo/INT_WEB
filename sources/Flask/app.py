from pymongo import MongoClient
from flask import render_template, request
from flask import Flask

app = Flask(__name__)
file = open(".env")
port = file.readline().split("=")[1]
ip = file.readline().split("=")[1]
@app.route('/')
def student():
    return render_template('student.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form["userId"]
        client = MongoClient(ip.rstrip(), int(port))
        print((ip.rstrip(), int(port), "inside get"))
        db = client.app
        collection = db.messages
        users = collection.find({"userId": str(result)})
        res = {}
        for user1 in users:
            res[user1['msg']] = user1['userId']
        print(res)
        if res is not None:
            return render_template("result.html", result=res)


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
