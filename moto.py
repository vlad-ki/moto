from bottle import (
    route, post,
    debug, run,
    request, response,
    redirect, template
)

from common import Note, Mongo, DateValueError


NOTES = Mongo('moto', 'notes')

debug(True)


@route('/')
def glavnaya():
    list_of_notes = NOTES.list()
    return template('templates/glavnaya', list_of_notes=list_of_notes, dateerror=None)


@post('/add_note')
def add_note():
    date = request.forms.get('date')
    odometr = request.forms.get('odometr')
    type_to_do = request.forms.get('type_to_do')
    info = request.forms.get('info')
    try:
        note = Note(date=date, odometr=odometr, type_to_do=type_to_do, info=info)
        NOTES.save(note)
        redirect('/')
    except DateValueError:
        list_of_notes = NOTES.list()
        return template('templates/glavnaya', list_of_notes=list_of_notes, dateerror=True)


@route('/edit_note')
def edit_note():
    _id = request.query._id
    note = NOTES.find_one(Note(_id))
    return template('templates/edit_note', note=note, dateerror=None)


@post('/edit_note')
def edit_note():
    _id = request.query._id
    date = request.forms.get('date')
    odometr = request.forms.get('odometr')
    type_to_do = request.forms.get('type_to_do')
    info = request.forms.get('info')
    try:
        note = Note(_id=_id, date=date, odometr=odometr, type_to_do=type_to_do, info=info)
        NOTES.save(note)
        redirect('/')
    except DateValueError:
        note = NOTES.find_one(Note(_id))
        return template('templates/edit_note', note=note, dateerror=True)


@post('/delete_note')
def delete_note():
    _id = request.query._id
    NOTES.remove(Note(_id))

    redirect('/')


run(host='localhost', port=8080, reloader=True)
