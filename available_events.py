import sys

def available_events(mydb):
    date = sys.argv[2]

    mycursor = mydb.cursor()

    try:
        mycursor.execute(
            """
            SELECT e.eid, e.title, e.type, e.datetime, COUNT(s.snum) AS availableSlots
            FROM Event e
            JOIN Slot s ON e.eid = s.eid
            WHERE s.is_reserved = FALSE
            AND e.datetime > %s
            GROUP BY e.eid, e.title, e.type, e.datetime
            ORDER BY e.datetime ASC, e.eid ASC
            """,
            (date,)
        )
        rows = mycursor.fetchall()
        for row in rows:
            print(",".join(str(col) for col in row))
    except Exception as e:
        print("Fail")
    finally:
        mycursor.close()