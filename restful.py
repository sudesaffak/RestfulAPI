 
from flask import Flask, jsonify, request


app = Flask(__name__)

users = [
    {"id": 1, "name": "aaa", "email": "aaak@example.com"},
    {"id": 2, "name": "bbb", "email": "bbbk@example.com"},
   
]

@app.route('/')
def home():
    return "HELLO"

## tüm kullanıcıları listeler
@app.route('/users', methods=['GET'])  
def get_users():
    return jsonify(users)


## id ye göre kullanıcıyı seçer, getirir 
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users if user["id"] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"message": "User not found"}), 404 ## kullanıcı bulunamıyorsa 404 hatası verir


## yeni kullanıcı eklenir
@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.json
    new_user['id'] = len(users) + 1
    users.append(new_user)
    return jsonify(new_user), 201


## kullanıcıyı günceller
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((user for user in users if user["id"] == user_id), None)
    if user:
        data = request.json
        user.update(data)
        return jsonify(user)
    return jsonify({"message": "User not found"}), 404


## kullanıcıyı siler 
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [user for user in users if user["id"] != user_id]
    return jsonify({"message": "User deleted"}), 200




if __name__ == '__main__':
    app.run(debug=True)
