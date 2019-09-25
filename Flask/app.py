from pymongo import MongoClient
from flask import render_template, request
from flask import Flask
app = Flask(__name__)
@app.route('/')
def student():
    return render_template('student.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form["userId"]
        users = collection.find({"userId": str(result)})
        res = {}
        for user1 in users:
            res[user1['msg']] = user1['userId']
        print(res)
        if user is not None:
            return render_template("result.html", result=res)


client = MongoClient()
db = client.test_database
collection = db.Users
Users = [{"msg": "dev", "userId": "Yuval"}, {"msg": "devops", "userId": "Lidor"}, {"msg": "dev", "userId": "Tamir"},
         {"msg": "deviiiiiii", "userId": "Tamir"}]

x = collection.insert_many(Users)
collist = db.list_collection_names()

user = (collection.find({"userId": "Tamir"}))
print(user, 55555555555)
if __name__ == '__main__':
    app.debug = True
    app.run()
