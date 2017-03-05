from bottle import (
    route, post,
    debug, run,
    request, response,
    redirect, template
)

from Note import Note


debug(True)


@route('/')
def glavnaya():
    list_of_notes = Note().list()
    return template('templates/glavnaya', list_of_notes=list_of_notes)


@post('/add_note')
def add_note():
    date = request.forms.get('date')
    odometr = request.forms.get('odometr')
    type_to_do = request.forms.get('type_to_do')
    info = request.forms.get('info')
    note = Note(date=date, odometr=odometr, type_to_do=type_to_do, info=info)
    note.save()
    redirect('/')


@route('/edit_note')
def edit_note():
    _id = request.query._id
    note = Note(_id).find()
    return template('templates/edit_note', note=note)


@post('/edit_note')
def edit_note():
    _id = request.query._id
    date = request.forms.get('date')
    odometr = request.forms.get('odometr')
    type_to_do = request.forms.get('type_to_do')
    info = request.forms.get('info')
    Note(_id=_id, date=date, odometr=odometr, type_to_do=type_to_do, info=info).save()

    redirect('/')


@post('/delete_note')
def delete_note():
    _id = request.query._id
    Note(_id).remove()

    redirect('/')


run(host='localhost', port=8080, reloader=True)
