import sys
 
def participant_schedule(mydb):
    uid = sys.argv[2]
 
    mycursor = mydb.cursor()
 
    try:
        mycursor.execute(
            """
            SELECT e.eid, e.title, e.type, e.datetime, s.snum,
                   v.vid, v.street, v.city, v.state, v.zip
            FROM Slot s
            JOIN Event e ON s.eid = e.eid
            LEFT JOIN Hosting h ON e.eid = h.eid AND h.is_primary = TRUE
            LEFT JOIN Venue v ON h.vid = v.vid
            WHERE s.uid = %s
            ORDER BY e.datetime ASC
            """,
            (uid,)
        )
        rows = mycursor.fetchall()
        for row in rows:
            print(",".join("" if col is None else str(col) for col in row))
    except Exception as e:
        mydb.rollback()
        print("Fail")
    finally:
        mycursor.close()
 