"""
Keep all messages
"""

from yoyo import step

__depends__ = {'acars-server_20190809_01_WggOt-add-message-s-full-text'}

steps = [
    step("ALTER TABLE aircrafts ADD COLUMN first_seen datetime"),
    step("ALTER TABLE aircrafts ADD COLUMN last_seen datetime"),
    step("""
INSERT OR REPLACE INTO aircrafts
SELECT a.id, a.registration, a.image, MIN(m.first_seen) first_seen, MAX(m.last_seen) last_seen
FROM messages m
INNER JOIN aircrafts a ON m.aircraft_id = a.id
GROUP BY a.id
ORDER BY a.id
    """),
    step("""
DELETE FROM aircrafts WHERE id IN(
    SELECT a.id
    FROM aircrafts a
    LEFT JOIN messages m ON a.id = m.aircraft_id
    GROUP BY a.id
    HAVING COUNT(m.id) = 0
);
    """),
    step("""
CREATE TABLE messages_no_first_seen(
    id integer primary key autoincrement,
    aircraft_id varchar(10),
    flight varchar(10),
    created_at datetime,
    client_id integer,
    txt varchar(255)
)
    """),
    step("""
INSERT INTO messages_no_first_seen
SELECT id, aircraft_id, flight, last_seen AS created_at, client_id, txt
FROM messages
    """),
    step("DROP TABLE messages"),
    step("ALTER TABLE messages_no_first_seen RENAME TO messages"),
    step("DELETE FROM messages WHERE created_at = ''")
]
