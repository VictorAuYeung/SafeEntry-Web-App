import sqlite3
import hashlib


def encrypt_string(hash_string):
            sha_signature = \
            hashlib.sha256(hash_string.encode()).hexdigest()
            return sha_signature


db = sqlite3.connect("database.db")
query = """
INSERT INTO Seat (LocationID, SeatNo, Hash)
VALUES (?, ?, ?)
"""

for i in range(0, 100):
    db.execute(query, ("LIB", i + 1, encrypt_string("LIB" + str(i + 1))))

for i in range(0, 40):
    db.execute(query, ("ICO", i + 1, encrypt_string("ICO" + str(i + 1))))

for i in range(0, 20):
    db.execute(query, ("SHL", i + 1, encrypt_string("SHL" + str(i + 1))))

for i in range(0, 20):
    db.execute(query, ("JHL", i + 1, encrypt_string("JHL" + str(i + 1))))


db.commit()
db.close()




