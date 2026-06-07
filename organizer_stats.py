import sys
 
def organizer_stats(mydb):
    n = sys.argv[2]
 
    mycursor = mydb.cursor()
 
    try:
        mycursor.execute(
            """
            SELECT o.uid, u.username, o.department, COUNT(e.eid) AS eventCount
            FROM Organizer o
            JOIN User u ON o.uid = u.uid
            JOIN Event e ON e.creator_uid = o.uid
            GROUP BY o.uid, u.username, o.department
            HAVING eventCount >= %s
            ORDER BY eventCount DESC, o.uid ASC
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
 