import sys

def insert_admin(mydb):
    uid      = sys.argv[2]
    email    = sys.argv[3]
    username = sys.argv[4]
    joined   = sys.argv[5]
    firstname = sys.argv[6]
    lastname  = sys.argv[7]

    mycursor = mydb.cursor()

    try:
        mycursor.execute(
            "INSERT INTO User (uid, email, username, joined) VALUES (%s, %s, %s, %s)",
            (uid, email, username, joined)
        )
        mycursor.execute(
            "INSERT INTO Administrator (uid, firstname, lastname) VALUES (%s, %s, %s)",
            (uid, firstname, lastname)
        )
        mydb.commit()
        print("Success")
    except Exception as e:
        mydb.rollback()
        print("Fail")
    finally:
        mycursor.close()    