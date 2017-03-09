<!DOCTYPE html>
<html>

<head>
    <meta content="text/html; charset=utf-8">
    <title>MotoNote</title>
</head>
<body>
    % include('templates/header.tpl')
    % if dateerror:
        <br><strong>Не верный формат даты. Рекомендуевый формат </strong><i>ДД.ММ.ГГГГ</i><br>
    % end
<table border="3">
    <thead>
        <tr>
            <th>edit</th>
            <th>Date</th>
            <th>Odometr</th>
            <th>Type to do</th>
            <th>Info</th>
        </tr>
    </thead>
    <tbody>
        % for note in list_of_notes:
            <tr>
                <td><a href="/edit_note?_id={{note['_id']}}">e</a></td>
                <td>{{note['date'].day}}.{{note['date'].month}}.{{note['date'].year}}</td>
                <td>{{note['odometr']}}</td>
                <td>{{note['type_to_do']}}</td>
                <td>{{note['info']}}</td>
            </tr>
        % end
    </tbody>
</table>
    <form action='add_note' method="POST">
            <input type='datetime' name='date' placeholder="Date"><br>
            <input type='number' name='odometr' placeholder="Odometr"><br>
            <input type='radio' name='type_to_do' value="Zamena masla v dvigotele">Замена масла в двигателе<br>    
            <input type='radio' name='type_to_do' value="Zamena masla v reduktore">Замена масла в редукторе<br>
            <input type='radio' name='type_to_do' value="Zamena antifriza">Замена антифриза<br>
            <input type='radio' name='type_to_do' value="Zamena schin">Замена Шин<br>
            <textarea name="info" placeholder="Info"></textarea><br>
            <input type="submit" value="Add note" name="Создать запись"> 
        </form>
    </body>
</html>
