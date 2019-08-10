"""
Add message's full text
"""

from yoyo import step

__depends__ = {'acars-server_20190804_02_LsZtD-create-aircrafts-table'}

steps = [
    step('ALTER TABLE messages ADD COLUMN txt varchar(255)')
]
