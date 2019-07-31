<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="10">
    <title>ACARS server</title>
    <link href="/css/application.css" rel="stylesheet" type="text/css">
</head>

<body>
    <div id="wrap">
    
    % include('layouts/header.tpl')

    <p>These aircrafts just passed above my head (Palaio Faliro, Athens, Greece):</p>

    % include('layouts/is_online.tpl', messages=messages)

    <table>
        <tr>
            <th>Aircraft Reg.</th>
            <th>Flight No.</th>
            <th>First Seen</th>
            <th>Last Seen</th>
            <th>Aircraft Image</th>
        </tr>
    % for msg in messages:
        <tr>
            <td>{{ msg.aircraft }}</td>
            <td>{{ msg.flight }}</td>
            <td>{{ msg.first_seen }}</td>
            <td>{{ msg.last_seen }}</td>
            <td>
                <a href="/img/aircrafts/{{ msg.aircraft.lower() }}.jpg" target="_blank">
                    <img src="/img/aircrafts/{{ msg.aircraft.lower() }}.jpg" height="120" /></li>
                </a>
            </td>
        </tr>
    % end
    </table>

    % include('layouts/footer.tpl')

    </div>
</body>
</html>
