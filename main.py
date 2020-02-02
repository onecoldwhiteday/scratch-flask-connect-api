from flask import Flask
from flask_restful import reqparse, abort, Api, Resource, fields
import vk_api
import credentials

app = Flask(__name__)
api = Api(app)


def get_auth():
    def two_factor():
        code = input('Code: ')
        return code, True

    vk = vk_api.VkApi(credentials.LOGIN, credentials.PASSWORD, auth_handler=two_factor)

    try:
        vk.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)

    return vk


def get_friends():
    vk = get_auth()
    return vk.method('friends.get', values={"count": 5, "fields": 'photo_50'})


friends = get_friends()


class Friends(Resource):
    def get(self):
        output_friends = []
        for f in friends['items']:
            output_friends.append({
                "id": f['id'],
                "full_name": '{} {}'.format(f['first_name'], f['last_name']),
                "photo_50": f["photo_50"]
            })
        return output_friends


api.add_resource(Friends, '/friends')

if __name__ == '__main__':
    app.run(debug=True)
