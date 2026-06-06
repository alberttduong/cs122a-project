import sys

def cancel_reservation(mydb):
    eid  = sys.argv[2]
    snum = sys.argv[3]
    uid  = sys.argv[4]

    mycursor = mydb.cursor()

    try:
        # Check the slot exists and is reserved by the given participant
        mycursor.execute(
            "SELECT is_reserved, uid FROM Slot WHERE eid = %s AND snum = %s",
            (eid, snum)
        )
        row = mycursor.fetchone()

        if row is None or row[0] != 1 or row[1] != int(uid):
            print("Fail")
            return

        # Cancel the reservation and remove the participant
        mycursor.execute(
            "UPDATE Slot SET is_reserved = FALSE, uid = NULL WHERE eid = %s AND snum = %s",
            (eid, snum)
        )
        mydb.commit()
        print("Success")
    except Exception as e:
        mydb.rollback()
        print("Fail")
    finally:
        mycursor.close()
