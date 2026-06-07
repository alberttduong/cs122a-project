import sys

def delete_organizer(mydb):
    uid = sys.argv[2]

    mycursor = mydb.cursor()

    try:
        mycursor.execute(
            "SELECT uid FROM Organizer WHERE uid = %s",
            (uid,)
        )
        row = mycursor.fetchone()
        if row is None:
            print("Fail")
            return
        mycursor.execute(
            "DELETE FROM User WHERE uid = %s",
            (uid,)
        )
        mydb.commit()
        print("Success")
    except Exception as e:
        mydb.rollback()
        print("Fail")
    finally:
        mycursor.close()