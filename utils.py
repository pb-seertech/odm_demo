import hashlib
from bson import json_util


def get_hash(data):
    m = hashlib.md5()
    m.update(str(data).encode('utf-8'))
    return m.hexdigest()


def fmt_resp(data):

    def do_fmt(data):
        attrs = data['attributes']
        for key in attrs:
            if isinstance(attrs[key], list):
                for index in range(len(attrs[key])):
                    del attrs[key][index]['_cls']
                    attrs[key][index] = {
                        'attributes': attrs[key][index]
                    }

            if key.endswith('_dt'):
                attrs[key] = attrs[key].time

        return data

    if isinstance(data, list):
        temp = []
        for datum in data:
            temp.append(do_fmt(datum))
        data = temp
    else:
        data = do_fmt(data)

    return json_util.dumps({
        'data': data
    })
