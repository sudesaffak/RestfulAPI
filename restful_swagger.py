from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields


app = Flask(__name__)
api = Api(app, version='1.0', title='USERS API', doc='/docs')


ns = api.namespace('users')


user_model = api.model('User', {
    'id': fields.Integer(readOnly=True, description='The user id'),
    'name': fields.String(required=True, description='The user name'),
    'email': fields.String(required=True, description='The user email')
})


users = [
    {"id": 1, "name": "aaa", "email": "aaak@example.com"},
    {"id": 2, "name": "bbb", "email": "bbbk@example.com"},
    
]



@ns.route('/')
class UserList(Resource):
    @ns.marshal_list_with(user_model)
    def get(self):
        '''LIST ALL USERS'''
        return users

    @ns.expect(user_model)
    @ns.marshal_with(user_model, code=201)
    def post(self):
        '''CREATE A NEW USER'''
        new_user = api.payload
        new_user['id'] = len(users) + 1
        users.append(new_user)
        return new_user, 201







@ns.route('/<int:user_id>')
@ns.response(404, 'User not found')
@ns.param('user_id', 'The user ID')
class User(Resource):
    @ns.marshal_with(user_model)
    def get(self, user_id):
        '''GET USER WITH ID'''
        user = next((user for user in users if user["id"] == user_id), None)
        if user:
            return user
        api.abort(404, "User not found")

    @ns.expect(user_model)
    @ns.marshal_with(user_model)
    def put(self, user_id):
        '''UPDATE USER WITH ID'''
        user = next((user for user in users if user["id"] == user_id), None)
        if user:
            data = request.json
            user.update(data)
            return user
        api.abort(404, "User not found")

    @ns.response(204, 'User deleted')
    def delete(self, user_id):
        '''DELETE USER WITH ID'''
        global users
        users = [user for user in users if user["id"] != user_id]
        return '', 204


if __name__ == '__main__':
    app.run(debug=True)


