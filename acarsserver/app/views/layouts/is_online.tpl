% color = 'red'
% caption = 'The client is offline. You see historical data.'

% for msg in messages:
    % if msg.client.is_online == True:
        % color = 'green'
        % caption = 'The client is online! You see realtime data!'
        % break
    % end
% end

<div id="is-online" style="background-color: {{ color }};">{{ caption }}</div>
