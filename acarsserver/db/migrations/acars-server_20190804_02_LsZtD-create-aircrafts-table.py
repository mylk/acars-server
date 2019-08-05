"""
Create aircrafts table
"""

from yoyo import step

__depends__ = {'acars-server_20190804_01_xPcZQ-create-messages-and-clients-tables'}

steps = [
    step("""
CREATE TABLE aircrafts(
    id integer primary key autoincrement,
    registration varchar(10),
    image varchar(120)
)
    """),
    step("""
CREATE UNIQUE INDEX idx_aircrafts_registration_unique ON aircrafts(registration)
    """),
    step("""
INSERT INTO aircrafts (registration, image)
SELECT aircraft, LOWER(aircraft) || '.jpg'
FROM messages
GROUP BY aircraft
    """),
    step("""
CREATE TABLE messages_aircrafts_migration(
    id integer primary key autoincrement,
    aircraft_id integer,
    flight varchar(10),
    first_seen datetime,
    last_seen datetime,
    client_id integer
)
    """),
    step("""
INSERT INTO messages_aircrafts_migration
SELECT m.id, a.id, m.flight, m.first_seen, m.last_seen, m.client_id
FROM messages AS m
INNER JOIN aircrafts AS a ON m.aircraft = a.registration
    """),
    step("""
DROP TABLE messages
    """),
    step("""
ALTER TABLE messages_aircrafts_migration RENAME TO messages
    """)
]
