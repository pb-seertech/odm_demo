from flask import Flask, request, g, url_for, abort, Response
from models import User, Contact
from pymodm import connect
from utils import fmt_resp
from bson import json_util

app = Flask(__name__)


@app.before_request
def open_connection():
    connect('mongodb://localhost:27017/user', alias='app')


@app.route('/user', methods=['GET', 'POST'], defaults={'id': None})
@app.route('/user/<id>', methods=['GET', 'PATCH', 'DELETE'])
def user_crud(id):
    result = None
    if request.method == 'GET':
        if id is None:
            result = User.objects.all()
            return Response(
                fmt_resp([row.get_data() for row in result]),
                status=200, mimetype='application/json')
        else:
            result = User.objects.find_by_id(id)
            return Response(
                fmt_resp(result.get_data()),
                status=200, mimetype='application/json')

    elif request.method == 'POST':
        payl = request.get_json()
        User(**payl).save()
        return '', 201

    elif request.method == 'PATCH':
        payl = request.get_json()
        user = User.objects.find_by_id(id)
        for key in payl:
            setattr(user, key, payl[key])
        user.save()
        return '', 201

    elif request.method == 'DELETE':
        result = User.objects.find_by_id(id)
        result.delete()
        return '', 204

if __name__ == '__main__':
    app.run(debug=True)
