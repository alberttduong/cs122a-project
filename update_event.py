import sys

def update_event(mydb):
    eid      = sys.argv[2]
    title    = sys.argv[3]
    datetime = sys.argv[4]

    mycursor = mydb.cursor()

    try:
        # Check the event exists
        mycursor.execute(
            "SELECT eid FROM Event WHERE eid = %s",
            (eid,)
        )
        row = mycursor.fetchone()

        if row is None:
            print("Fail")
            return

        # Update the event title and datetime
        mycursor.execute(
            "UPDATE Event SET title = %s, datetime = %s WHERE eid = %s",
            (title, datetime, eid)
        )
        mydb.commit()
        print("Success")
    except Exception as e:
        mydb.rollback()
        print("Fail")
    finally:
        mycursor.close()
