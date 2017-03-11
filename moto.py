from bottle import (
    route, post,
    debug, run,
    request, response,
    redirect, template,
    install
)

from common import (
    Note,
    DateValueError,
    MongoPlugin
)


NOTES = MongoPlugin('moto', 'notes')
install(NOTES)

debug(True)


@route('/')
def glavnaya(mongo):
    list_of_notes = mongo.list()
    return template('templates/glavnaya', list_of_notes=list_of_notes, dateerror=None)


@post('/add_note')
def add_note(mongo):
    date = request.forms.get('date')
    odometr = request.forms.get('odometr')
    type_to_do = request.forms.get('type_to_do')
    info = request.forms.get('info')
    try:
        note = Note(date=date, odometr=odometr, type_to_do=type_to_do, info=info)
        mongo.save(note)
        redirect('/')
    except DateValueError:
        list_of_notes = mongo.list()
        return template('templates/glavnaya', list_of_notes=list_of_notes, dateerror=True)


@route('/edit_note')
def edit_note(mongo):
    _id = request.query._id
    note = mongo.find_one(Note(_id))
    return template('templates/edit_note', note=note, dateerror=None)


@post('/edit_note')
def edit_note(mongo):
    _id = request.query._id
    date = request.forms.get('date')
    odometr = request.forms.get('odometr')
    type_to_do = request.forms.get('type_to_do')
    info = request.forms.get('info')
    try:
        note = Note(_id=_id, date=date, odometr=odometr, type_to_do=type_to_do, info=info)
        mongo.save(note)
        redirect('/')
    except DateValueError:
        note = mongo.find_one(Note(_id))
        return template('templates/edit_note', note=note, dateerror=True)


@post('/delete_note')
def delete_note(mongo):
    _id = request.query._id
    mongo.remove(Note(_id))

    redirect('/')


run(host='localhost', port=8080, reloader=True)
