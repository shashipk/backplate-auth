
from flask_restful import Resource

class Items(Resource):
    # /v1/items
    def get(self):
        return [{'id': idx} for idx in range(0, 20)]

class Item(Resource):
    # /v1/items/:id
    def get(self, id):
        return {'id': id}
