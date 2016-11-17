import datetime
import os
import json
import bottle


bottle.debug(True)
FILE = '/home/vk/doc/Python3/moto/moto.json'


class Note():
    def __init__(self, date, odometr, type_to_do, dop_info, db=True):

        '''
        if db:
            year = int(date[0:4])
            month = int(date[5:7])
            day = int(date[8:])
        else:
            day = int(date[0:2])
            month = int(date[3:5])
            year = int(date[6:])
        '''
        self.date = date  #  datetime.date(year, month, day)
        self.odometr = odometr
        self.type_to_do = type_to_do
        self.dop_info = dop_info

    def save(self):
        with open(FILE) as fh:
            if len(fh.read()) > 0:
                load_data = json.load(fh)
            else:
                load_data = []
            load_data.append(
                {
                    'date': self.date,
                    'odometr': self.odometr,
                    'type_to_do': self.type_to_do,
                    'dop_info': self.dop_info
                }
            )
        with open(FILE, 'w') as fh:
            json.dump(load_data, fh, indent=4, ensure_ascii=True)


@bottle.route('/')
def glavnaya():
    return bottle.template('glavnaya', level='')


@bottle.post('/work/<level>')
def parse(level):
    bottle.response.content_type = 'text/html; charset=utf8'
    date = bottle.request.forms.get('date')
    odometr = bottle.request.forms.get('odometr')
    type_to_do = bottle.request.forms.get('type_to_do')
    dop_info = bottle.request.forms.get('dop_info')
    note = Note(date=date, odometr=odometr, type_to_do=type_to_do, dop_info=dop_info, db=False)
    note.save()

    bottle.redirect('/')


@bottle.route('/moto.json')
def data_response():
    with open(FILE) as fh:
        if len(fh.read()) > 0:
            json_data = json.load(fh)
        else:
            json_data = ""
    return str(json_data)
bottle.run(host='localhost', port=8080, reloader=True)
