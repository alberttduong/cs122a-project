import sys

def reserve_slot(mydb):
    eid  = sys.argv[2]
    snum = sys.argv[3]
    uid  = sys.argv[4]

    mycursor = mydb.cursor()

    try:
        # Check the slot exists and is currently unreserved
        mycursor.execute(
            "SELECT is_reserved FROM Slot WHERE eid = %s AND snum = %s",
            (eid, snum)
        )
        row = mycursor.fetchone()

        if row is None or row[0] == 1:
            print("Fail")
            return

        # Reserve the slot and assign the participant
        mycursor.execute(
            "UPDATE Slot SET is_reserved = TRUE, uid = %s WHERE eid = %s AND snum = %s",
            (uid, eid, snum)
        )
        mydb.commit()
        print("Success")
    except Exception as e:
        mydb.rollback()
        print("Fail")
    finally:
        mycursor.close()