import sys

def venue_events(mydb):
    vid = sys.argv[2]

    mycursor = mydb.cursor()

    try:
        mycursor.execute(
            """
            SELECT e.eid, e.title, e.type, e.datetime, h.is_primary
            FROM Event e
            JOIN Hosting h ON e.eid = h.eid
            WHERE h.vid = %s
            ORDER BY e.datetime ASC, e.eid ASC
            """,
            (vid,)
        )
        rows = mycursor.fetchall()
        for row in rows:
            print(",".join(str(col) for col in row))
    except Exception as e:
        print("Fail")
    finally:
        mycursor.close()