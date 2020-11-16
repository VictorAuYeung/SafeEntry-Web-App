import sqlite3
import names


db = sqlite3.connect("database.db")

query = """
INSERT INTO Student(MatricNo, Name, Class, Gender)
VALUES(? , ?, ?, ?)
"""

classes = ["20J01", "20J02", "20J03", "20J04", "20J05", "20J06", "20J07", "20J08", "20J09", "20J10", "20J11", "20J12", "20J13", "20J14", "20J15", "20J16", "20J17", "20J18"]
matriclst = []
namelst = []
genderlst = []

i = 0
while i < len(classes):
    j = 1
    while j <= 30:
        if j < 15:
            namelst.append(names.get_full_name(gender="female"))
            genderlst.append("F")
        elif j >= 15:
            namelst.append(names.get_full_name(gender="male"))
            genderlst.append("M")


        if j < 10:
            matricno = classes[i] + '0' + str(j)
        else:
            matricno = classes[i] + str(j)

        j += 1
        matriclst.append(matricno)
    i += 1


for i in range(len(matriclst)):
    matricno = matriclst[i]
    name = namelst[i]
    class_ = matricno[0:5]
    gender = genderlst[i]
    db.execute(query, (matricno, name, class_, gender))
    db.commit()

db.close()