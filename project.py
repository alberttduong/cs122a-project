import mysql.connector
import sys

from import_data import import_data
from insert_admin import insert_admin
from add_venue import add_venue
from available_events import available_events
from cancel_reservation import cancel_reservation
from delete_organizer import delete_organizer
from organizer_stats import organizer_stats
from participant_schedule import participant_schedule
from popular_event_types import popular_event_types
from reserve_slot import reserve_slot
from update_event import update_event
from venue_events import venue_events

db_user = "test"
db_password = "password"

try:
    # if u have a diff user and password set up,
    # u can make a creds.py file with user=".." and password=".."
    # creds.py will be ignored by git
    import creds
    db_user = creds.user
    db_password = creds.password
except:
    pass

mydb = mysql.connector.connect(
    user=db_user,
    password=db_password,
    database="cs122a"
)

if __name__ == "__main__":
    match sys.argv[1]:
        case "import":
            import_data(mydb)
        case "insertAdmin":
            insert_admin(mydb)
        case "addVenue":
            add_venue(mydb)
        case "reserveSlot":
            reserve_slot(mydb)
        case "cancelReservation":
            cancel_reservation(mydb)
        case "updateEvent":
            update_event(mydb)
        case "deleteOrganizer":
            delete_organizer(mydb)
        case "availableEvents":
            available_events(mydb)
        case "popularEventTypes":
            popular_event_types(mydb)
        case "participantSchedule":
            participant_schedule(mydb)
        case "organizerStats":
            organizer_stats(mydb)
        case "venueEvents":
            venue_events(mydb)
        case _:
            print("function not found:", sys.argv[1])

    mydb.close()
