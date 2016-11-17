<!DOCTYPE html>
<html>
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="content-type">
    </head>
    <body>
        <script>
            var xhr = new XMLHttpRequest();
            xhr.open('GET', 'moto.json', false);
            xhr.send();
            if (xhr.status != 200) {
                // обработать ошибку
                    alert('Ошибка ' + xhr.status + ': ' + xhr.statusText);
            } 
            else {
                // вывести результат
                document.write(xhr.responseText);
                }
        </script>

        <form action='work/1' method="POST">
        Date
            <input type = 'datetime' name = 'date'>
        <br>
        Одометр
            <input type = 'number' name = 'odometr'>
        <br>
        Тип действия
        <br>
            <input type = 'radio' name = 'type_to_do' value="Замена масла в двигателе">
            Замена масла в двигателе
        <br>    
            <input type = 'radio' name = 'type_to_do' value="Замена масла в редукторе">
            Замена масла в редукторе
        <br>
            <input type = 'radio' name = 'type_to_do' value="Замена антифриза">
            Замена антифриза
        <br>
            <input type = 'radio' name = 'type_to_do' value="Замена шин">
            Замена Шин
        <br>
        Дополнительная информация
            <input type = 'text' name = 'dop_info'>
        <br>
            <button type="submit">Создать запись</button>

        </form>
    </body>
</html>