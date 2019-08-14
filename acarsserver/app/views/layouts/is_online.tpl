% color = 'red'
% caption = 'The client is offline. You see historical data.'

% if messages[0].client.is_online == True:
    % color = 'green'
    % caption = 'The client is online! You see realtime data!'
% end

<div id="is-online" style="background-color: {{ color }};">{{ caption }}</div>
