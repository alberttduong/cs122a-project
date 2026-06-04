import sys
import csv

tables = {
    "Administrator": {
        "num_cols": 3,
        "rules": '''
            uid INT,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            PRIMARY KEY (uid),
            FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE
        ''',
    },
    "Approval": {
        "num_cols": 4,
        "rules": '''
            uid INT NOT NULL,
            vid INT NOT NULL,
            valid_from DATE NOT NULL,
            valid_until DATE NOT NULL,
            PRIMARY KEY (uid, vid),
            FOREIGN KEY (uid) REFERENCES Administrator(uid) ON DELETE CASCADE,
            FOREIGN KEY (vid) REFERENCES OffCampus(vid) ON DELETE CASCADE
        ''',
    },
    "Event": {
        "num_cols": 5,
        "rules": '''
            eid INT,
            creator_uid INT NOT NULL,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            datetime DATETIME NOT NULL,
            PRIMARY KEY (eid),
            FOREIGN KEY (creator_uid) REFERENCES Organizer(uid) ON DELETE CASCADE
        ''',
    },
    "Hosting": {
        "num_cols": 3,
        "rules": '''
            eid INT NOT NULL,
            vid INT NOT NULL,
            is_primary BOOLEAN NOT NULL,
            PRIMARY KEY (eid, vid),
            FOREIGN KEY (eid) REFERENCES Event(eid) ON DELETE CASCADE,
            FOREIGN KEY (vid) REFERENCES Venue(vid) ON DELETE CASCADE
        ''',
    },
    "OffCampus": {
        "num_cols": 2,
        "rules": '''
            vid INT,
            distance INT NOT NULL,
            PRIMARY KEY (vid),
            FOREIGN KEY (vid) REFERENCES Venue(vid) ON DELETE CASCADE
        ''',
    },
    "OnCampus": {
        "num_cols": 2,
        "rules": '''
            vid INT,
            code TEXT NOT NULL,
            PRIMARY KEY (vid),
            FOREIGN KEY (vid) REFERENCES Venue(vid) ON DELETE CASCADE
        ''',
    },
    "Organizer": {
        "num_cols": 3,
        "rules": '''
            uid INT,
            department TEXT NOT NULL,
            experience INT NOT NULL,
            PRIMARY KEY (uid),
            FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE
        ''',
    },
    "Participant": {
        "num_cols": 2,
        "rules": '''
            uid INT,
            type TEXT,
            PRIMARY KEY (uid),
            FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE
        ''',
    },
    "Slot": {
        "num_cols": 4,
        "rules": '''
            eid INT,
            snum INT NOT NULL,
            is_reserved BOOLEAN NOT NULL,
            uid INT,
            PRIMARY KEY (eid, snum),
            FOREIGN KEY (eid) REFERENCES Event(eid) ON DELETE CASCADE,
            FOREIGN KEY (uid) REFERENCES Participant(uid) ON DELETE CASCADE
        ''',
    },
    "User": {
        "num_cols": 4,
        "rules": '''
            uid INT,
            email TEXT NOT NULL,
            username TEXT NOT NULL,
            joined DATE NOT NULL,
            PRIMARY KEY (uid)
        ''',
    },
    "Venue": {
        "num_cols": 5,
        "rules": '''
            vid INT,
            street TEXT NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            zip TEXT NOT NULL,
            PRIMARY KEY (vid)
        ''',
    },
}

tables_in_order = [
    "User",
    "Organizer",
    "Participant",
    "Administrator",
    "Event",
    "Venue",
    "OffCampus",
    "OnCampus",
    "Slot",
    "Hosting",
    "Approval",
]

def value_str(n):
    s = "%s, " * n
    s = s.removesuffix(", ")
    return f"({s})"

def convert_null_to_none(row):
    return [None if c == 'NULL' else c for c in row]

def import_data(mydb):
    folder = sys.argv[2]
    mycursor = mydb.cursor()

    try:
        mycursor.execute("SET foreign_key_checks = 0")
        for t in reversed(tables_in_order):
            mycursor.execute(f"DROP TABLE IF EXISTS {t}")
        mycursor.execute("SET foreign_key_checks = 1")

        for t in tables_in_order:
            mycursor.execute(f"CREATE TABLE {t} ({tables[t]['rules']})")

        for t in tables_in_order:
            with open(f"{folder}/{t}.csv", mode="r") as file:
                csv_reader = csv.reader(file)
                data = [convert_null_to_none(row) for row in csv_reader]
                if data:
                    mycursor.executemany(
                        f"INSERT INTO {t} VALUES {value_str(tables[t]['num_cols'])}",
                        data
                    )

        mydb.commit()
        print("Success")
    except Exception as e:
        mydb.rollback()
        print("Fail")
    finally:
        mycursor.close()