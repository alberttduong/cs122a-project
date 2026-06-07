import sys
from datetime import datetime, date

def participant_schedule(mydb):
    uid = sys.argv[2]

    mycursor = mydb.cursor()

    try:
        mycursor.execute(
            """
            SELECT e.eid, e.title, e.type, e.datetime, s.snum,
                   h.vid, v.street, v.city, v.state, v.zip
            FROM Slot s
            JOIN Event e ON s.eid = e.eid
            LEFT JOIN (
                SELECT eid, vid FROM Hosting WHERE is_primary = TRUE
            ) h ON e.eid = h.eid
            LEFT JOIN Venue v ON h.vid = v.vid
            WHERE s.uid = %s AND s.is_reserved = TRUE
            ORDER BY e.datetime ASC
            """,
            (uid,)
        )
        rows = mycursor.fetchall()
        for row in rows:
            formatted = []
            for col in row:
                if col is None:
                    formatted.append("")
                elif isinstance(col, datetime):
                    formatted.append(col.strftime("%Y-%m-%d %H:%M:%S"))
                elif isinstance(col, date):
                    formatted.append(col.strftime("%Y-%m-%d"))
                else:
                    formatted.append(str(col))
            print(",".join(formatted))
    except Exception as e:
        mydb.rollback()
        print("Fail")
    finally:
        mycursor.close()