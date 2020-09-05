from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta

@app.route('/food', methods=['GET'])
def read_reviews():
    title_receive = request.args.get('title_give')
    reviews = list(db.foods.find({'title':title_receive}, {'_id': 0}))

    return jsonify({'result': 'success', 'reviews': reviews})



@app.route('/')
def home():
    return render_template('project-1.html')

@app.route('/search')
def search():
    q_receive = request.args.get('q_give')
    return render_template('ice.html', q=q_receive)





if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

