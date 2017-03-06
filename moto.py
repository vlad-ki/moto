from bottle import (
    route, post,
    debug, run,
    request, response,
    redirect, template
)

from common import Note, Mongo


NOTES = Mongo('moto', 'notes')

debug(True)


@route('/')
def glavnaya():
    # list_of_notes = Note().list()
    list_of_notes = NOTES.list()
    return template('templates/glavnaya', list_of_notes=list_of_notes)


@post('/add_note')
def add_note():
    date = request.forms.get('date')
    odometr = request.forms.get('odometr')
    type_to_do = request.forms.get('type_to_do')
    info = request.forms.get('info')
    note = Note(date=date, odometr=odometr, type_to_do=type_to_do, info=info)
    # note.save()
    NOTES.save(vars(note))

    redirect('/')


@route('/edit_note')
def edit_note():
    _id = request.query._id
    # note = Note(_id).find()
    note = NOTES.find_one(Note(_id)._id)
    return template('templates/edit_note', note=note)


@post('/edit_note')
def edit_note():
    _id = request.query._id
    date = request.forms.get('date')
    odometr = request.forms.get('odometr')
    type_to_do = request.forms.get('type_to_do')
    info = request.forms.get('info')
    # Note(_id=_id, date=date, odometr=odometr, type_to_do=type_to_do, info=info).save()
    note = Note(_id=_id, date=date, odometr=odometr, type_to_do=type_to_do, info=info)
    NOTES.save(vars(note))

    redirect('/')


@post('/delete_note')
def delete_note():
    _id = request.query._id
    # Note(_id).remove()
    NOTES.remove({'_id': Note(_id)._id})

    redirect('/')


run(host='localhost', port=8080, reloader=True)
