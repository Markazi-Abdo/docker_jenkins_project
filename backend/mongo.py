from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask_cors import CORS

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://zh:test@mongodb:27017/mongotask?authSource=admin'
mongo = PyMongo(app)
CORS(app)


@app.route('/api/tasks', methods=['GET'])
def get_all_tasks():
    tasks = mongo.db.tasks
    result = [{'_id': str(t['_id']), 'title': t['title']} for t in tasks.find()]
    return jsonify(result)


@app.route('/api/task', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'title is required'}), 400

    task_id = mongo.db.tasks.insert_one({'title': data['title']}).inserted_id
    return jsonify({'_id': str(task_id), 'title': data['title']}), 201


@app.route('/api/task/<id>', methods=['PUT'])
def update_task(id):
    try:
        oid = ObjectId(id)
    except InvalidId:
        return jsonify({'error': 'Invalid ID'}), 400

    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'title is required'}), 400

    mongo.db.tasks.update_one({'_id': oid}, {'$set': {'title': data['title']}})
    return jsonify({'message': 'updated'})


@app.route('/api/task/<id>', methods=['DELETE'])
def delete_task(id):
    try:
        oid = ObjectId(id)
    except InvalidId:
        return jsonify({'error': 'Invalid ID'}), 400

    res = mongo.db.tasks.delete_one({'_id': oid})
    return jsonify({'deleted': res.deleted_count == 1})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
