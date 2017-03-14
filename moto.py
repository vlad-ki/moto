from bottle import (
    route, post,
    debug, run,
    request, response,
    redirect, template,
    install,
    static_file
)

from common import (
    Note,
    DateValueError,
    MongoPlugin,
    date_parse,
    note_object_to_dict
)


debug(True)


@route('/templates/<filename:path>')
def static(filename):
    return static_file(filename, root='/home/vk/doc/projects/moto/app/templates/')


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
        date = date_parse(date)
    except DateValueError:
        list_of_notes = mongo.list()
        return template('templates/glavnaya', list_of_notes=list_of_notes, dateerror=True)

    note = Note(date=date, odometr=odometr, type_to_do=type_to_do, info=info)
    mongo.save(note_object_to_dict(note))
    redirect('/')


@route('/edit_note')
def edit_note(mongo):
    _id = request.query._id
    note = mongo.find_one(note_object_to_dict(Note(_id)))
    return template('templates/edit_note', note=note, dateerror=None)


@post('/edit_note')
def edit_note(mongo):
    _id = request.query._id
    date = request.forms.get('date')
    odometr = request.forms.get('odometr')
    type_to_do = request.forms.get('type_to_do')
    info = request.forms.get('info')

    try:
        date = date_parse(date)
    except DateValueError:
        note = mongo.find_one(note_object_to_dict(Note(_id)))
        return template('templates/edit_note', note=note, dateerror=True)

    note = Note(_id=_id, date=date, odometr=odometr, type_to_do=type_to_do, info=info)
    mongo.save(note_object_to_dict(note))
    redirect('/')


@post('/delete_note')
def delete_note(mongo):
    _id = request.query._id
    mongo.remove(Note(_id))

    redirect('/')


if __name__ == '__main__':
    NOTES = MongoPlugin('moto', 'notes')
    install(NOTES)

run(host='localhost', port=8080, reloader=True)
