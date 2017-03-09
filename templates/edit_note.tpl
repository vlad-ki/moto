<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>MotoNote | Edit Note</title>
</head>
<body>
	% include('templates/header.tpl')
	% if dateerror:
    <br><strong>Не верный формат даты. Рекомендуевый формат </strong><i>ДД.ММ.ГГГГ</i>
	% end
	<form action="/edit_note?_id={{note['_id']}}" method="POST">
		<!-- <input type="text" name="_id" value="{{note['_id']}}" readonly hidden><br> -->
		<input type="text" name="date" placeholder="Date" value="{{note['date'].day}}.{{note['date'].month}}.{{note['date'].year}}"><br>
		<input type="text" name="odometr" placeholder="odometr" value="{{note['odometr']}}"><br>
		<input type='radio' name='type_to_do' value="Zamena masla v dvigotele">Замена масла в двигателе<br> 
        <input type='radio' name='type_to_do' value="Zamena masla v reduktore">Замена масла в редукторе<br>
        <input type='radio' name='type_to_do' value="Zamena antifriza">Замена антифриза<br>
        <input type='radio' name='type_to_do' value="Zamena schin">Замена Шин<br>
        <textarea name="info" value="{{note['info']}}" placeholder="Info"></textarea><br>
        <input type="submit" value="Edit note" name="Создать запись">
		<button formaction="/delete_note?_id={{note['_id']}}">Remove</button>
	</form>
</body>
</html>