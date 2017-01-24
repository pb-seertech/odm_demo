from pymodm import connect, MongoModel, EmbeddedMongoModel, fields
from pymongo.write_concern import WriteConcern
from pymodm.queryset import QuerySet
from pymodm.manager import Manager
from bson import json_util
from bson.codec_options import CodecOptions
from bson.objectid import ObjectId
from datetime import datetime
from time import time
from utils import get_hash


class Serializer():

    def get_data(self):
        return {
            'attributes': self.__dict__['_data']
        }


class CommonQuerySet(QuerySet):

    def get_queryset(self, **kwargs):
        return self.raw({'flags': 0})

    def find_by_id(self, id):
        return self.raw({
            '_id': ObjectId(str(id)),
            'flags': 0
        }).first()

    def all(self, **kwargs):
        return self.raw({'flags': 0}).all()


class User(MongoModel, Serializer):
    id = fields.ObjectIdField(primary_key=True)
    username = fields.CharField(min_length=8, max_length=32)
    email = fields.EmailField()
    created_dt = fields.TimestampField(default=datetime.now())
    etag = fields.CharField(min_length=32, max_length=32)
    contacts = fields.EmbeddedDocumentListField('Contact')
    flags = fields.IntegerField(default=0)

    objects = Manager.from_queryset(CommonQuerySet)()

    class Meta:
        connection_alias = 'app'
        collection_name = 'users'
        codec_options = CodecOptions(tz_aware=True)
        write_concern = WriteConcern(j=True)

    def __str__(self):
        return str(self.__dict__)

    def save(self, **kwargs):
        self.etag = get_hash(str(self))
        super(User, self).save(**kwargs)

    def delete(self, **kwargs):
        self.flags = 1
        self.etag = get_hash(str(self))
        super(User, self).save(**kwargs)


class Contact(EmbeddedMongoModel, Serializer):
    number = fields.IntegerField()

    def __str__(self):
        return self.__dict__
