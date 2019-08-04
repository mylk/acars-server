"""
Create messages and clients tables
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
CREATE TABLE messages(
    id integer primary key autoincrement,
    aircraft varchar(10),
    flight varchar(10),
    first_seen datetime,
    last_seen datetime,
    client_id integer
)
    """),
    step("""
CREATE TABLE clients(
    id integer primary key autoincrement,
    ip varchar(15),
    last_seen datetime
)
    """)
]
