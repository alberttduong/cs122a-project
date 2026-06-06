import sys

def add_venue(mydb):
    eid        = sys.argv[2]
    vid        = sys.argv[3]
    is_primary = sys.argv[4].lower() == 'true'

    mycursor = mydb.cursor()

    try:
        # If is_primary is true, check that no other primary venue exists for this event
        if is_primary:
            mycursor.execute(
                "SELECT COUNT(*) FROM Hosting WHERE eid = %s AND is_primary = TRUE",
                (eid,)
            )
            count = mycursor.fetchone()[0]
            if count > 0:
                print("Fail")
                return

        mycursor.execute(
            "INSERT INTO Hosting (eid, vid, is_primary) VALUES (%s, %s, %s)",
            (eid, vid, is_primary)
        )
        mydb.commit()
        print("Success")
    except Exception as e:
        mydb.rollback()
        print("Fail")
    finally:
        mycursor.close()