import sys
 
def popular_event_types(mydb):
    n = sys.argv[2]
 
    mycursor = mydb.cursor()
 
    try:
        mycursor.execute(
            """
            SELECT e.type, COUNT(s.snum) AS reservedCount
            FROM Event e
            JOIN Slot s ON e.eid = s.eid
            WHERE s.is_reserved = TRUE
            GROUP BY e.type
            HAVING reservedCount >= %s
            ORDER BY reservedCount DESC, e.type ASC
            """,
            (n,)
        )
        rows = mycursor.fetchall()
        for row in rows:
            print(",".join(str(col) for col in row))
    except Exception as e:
        mydb.rollback()
        print("Fail")
    finally:
        mycursor.close()
 