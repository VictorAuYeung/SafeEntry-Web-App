from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import hashlib

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("homepage.html")
        
@app.route("/checkin/<location>/<seatno>", methods = ["GET", "POST"])
def seat(location, seatno):
    #db = sqlite3.connect("database.db")
    #db.close()
    #return "database unlocked"
    check = False
    if location == "LIB" and int(seatno) <= 100 and int(seatno) > 0:
        check = True

    elif location == "ICO" and int(seatno) <= 40 and int(seatno) > 0:
        check = True

    elif location == "SHL" and int(seatno) <= 20 and int(seatno) > 0:
        check = True

    elif location == "JHL" and int(seatno) <= 20 and int(seatno) > 0:
        check = True


    # checks whether url is correct
    if check:
        

        # check whether already booked
        taken_query = """
        SELECT Taken from Seat
        WHERE LocationID = ?
        AND SeatNo = ?
        """

        db = sqlite3.connect("database.db")
        cursor = db.execute(taken_query,(location, seatno))
        data = cursor.fetchall()
        cursor.close()
        db.close()
        if str(data[0][0]) == "True":
            return "Seat Taken!"



        if request.method == "GET":
            db = sqlite3.connect("database.db")
            cursor = db.execute("SELECT LocationName from Location WHERE LocationID = ?", (location,))
            locationname = cursor.fetchall()
            locationname = locationname[0][0]

            return render_template("index.html", locationname = locationname, seatno = seatno)
        else:
            matricno = request.form["matricno"]

            matric_query = """
            SELECT Name from Student
            WHERE MatricNo = ?
            """

            db = sqlite3.connect("database.db")
            cursor = db.execute(matric_query,(matricno,))
            temp = cursor.fetchall()
            cursor.close()
            db.close()

            if len(temp) == 0:
                return "Invalid Matric Number!"

            else:

            
                now = datetime.now()
                startdatetime = now.strftime("%Y-%m-%d %H:%M:%S")
                db = sqlite3.connect("database.db")

                insert_entry = """
                INSERT INTO Entry (MatricNo, LocationID, SeatNo, StartDateTime, EndDateTime)
                VALUES (?, ?, ?, ?, ?)
                """

                db.execute(insert_entry, (matricno, location, seatno, startdatetime, 0))
                db.commit()
                db.close()

                insert_seat = """
                UPDATE Seat
                SET Taken = "True"
                WHERE LocationID = ?
                AND SeatNo = ?
                """

                db = sqlite3.connect("database.db")

                db.execute(insert_seat, (location, seatno))
                db.commit()
                db.close()

            def encrypt_string(hash_string):
                sha_signature = \
                hashlib.sha256(hash_string.encode()).hexdigest()
                return sha_signature

            sha = encrypt_string(location + str(seatno))

            return redirect(url_for("check_out", sha = sha))
    
    
    else:
        return "Invalid URL"



@app.route("/checkout/<sha>", methods = ["GET", "POST"])
def check_out(sha):
    if request.method == "GET":
        return render_template("checkout.html")

    else:
        seat_query = """
        SELECT LocationID, SeatNo, Taken 
        FROM Seat
        WHERE Hash = ?
        """

        db = sqlite3.connect("database.db")
        cursor = db.execute(seat_query, (sha,))
        data = cursor.fetchall()
        cursor.close()
        db.close()

        if data[0][2] == "False":
            return "Unable to check out. Seat is not taken."

        else:
            db = sqlite3.connect("database.db")
            seat_update = """
            UPDATE Seat
            SET Taken = "False"
            WHERE Hash = ?
            """
            
            db.execute(seat_update, (sha,))
            db.commit()
            db.close()

            db = sqlite3.connect("database.db")

            now = datetime.now()
            enddatetime = now.strftime("%Y-%m-%d %H:%M:%S")

            update_entry = """
            UPDATE Entry
            SET EndDateTime = ?
            WHERE LocationID = ?
            AND SeatNo = ?
            AND EndDateTime = ?
            """

            db.execute(update_entry, (enddatetime, data[0][0], data[0][1], 0))
            db.commit()
            db.close()

            return "Checked Out!"
            

        #return str(data)


@app.route("/admin/entries", methods = ["GET", "POST"])
def admin_entry():

    if request.method == "GET":

        db = sqlite3.connect("database.db")

        query = """
        SELECT Entry.MatricNo, Student.Name, Student.Class, Student.Gender, Location.LocationName, Entry.SeatNo, Entry.StartDateTime, Entry.EndDateTime
        FROM Entry, Student, Location
        WHERE Entry.MatricNo = Student.MatricNo
        AND Entry.LocationID = Location.LocationID
        ORDER BY StartDateTime DESC
        """

        cursor = db.execute(query)
        data = cursor.fetchall()
        cursor.close()
        db.close()

        return render_template("admin_entry.html", data = data)
       

    else:

        query = """
        SELECT Entry.MatricNo, Student.Name, Student.Class, Student.Gender, Location.LocationName, Entry.SeatNo, Entry.StartDateTime, Entry.EndDateTime
        FROM Entry, Student, Location
        WHERE Entry.MatricNo = Student.MatricNo
        AND Entry.LocationID = Location.LocationID
        """
        lst = []

        if request.form["matricno"] != '':
            matricno = request.form["matricno"]
            lst.append(matricno)
            query = query + "\nAND Entry.MatricNo = ?"

    
        if request.form["name"] != '':
            name = request.form["name"]
            lst.append(name)
            query = query + "\nAND Student.Name = ?"           

        
        if request.form["class"] != '':
            class_ = request.form["class"]
            lst.append(class_)
            query = query + "\nAND Student.Class = ?"     

        
        if request.form["gender"] != '':
            gender = request.form["gender"]
            lst.append(gender)
            query = query + "\nAND Student.Gender = ?"     

        if request.form["seatno"] != '':
            seatno = request.form["seatno"]
            lst.append(seatno)
            query = query + "\nAND Entry.SeatNo = ?"    


        if request.form["location"] != '':
            location = request.form["location"]
            lst.append(location)
            query = query + "\nAND Location.LocationName = ?"   

        query = query + "\nORDER BY StartDateTime DESC"
        #return query

        tup = tuple(lst)

        db = sqlite3.connect("database.db")
        cursor = db.execute(query, tup)
        data = cursor.fetchall()
        cursor.close()
        db.close()

        return render_template("admin_entry.html", data = data)









if __name__ == "__main__":
    app.run(debug = True, port = 5000)