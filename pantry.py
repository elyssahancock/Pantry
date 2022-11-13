
# Assignment requirements.
"""Your software must demonstrate 
the ability to insert, modify, delete,
 and retrieve (or query) data."""

# Basic Imports.
from select import select
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
#from datetime import datetime

from pyparsing import col

def main():

    # Set up.
    db_json_file =  "food-inventory-6cbfd-firebase-adminsdk-zjecw-9714286f35.json"
    cred = credentials.Certificate(db_json_file)
    firebase_admin.initialize_app(cred)

    db = firestore.client()


    
    collection_name = "Pantry" 
    
    # Timestamps:
    """
    Stored as: 
    DatetimeWithNanoseconds(2022, 9, 29, 22, 36, 6, 661000, tzinfo=datetime.timezone.utc)
    DatetimeWithNanoseconds(year, month, day, militaryHour + 6, minutes, seconds, nanoseconds )
    """
    # Trial of Expiration date
    # db.collection(collection_name).add({"expiration": datetime.datetime(2022, 10, 7)})

    """# Get all documents in a collection
    docs = db.collection(collection_name).get()
    for doc in docs:
        print(doc.to_dict()) """

    selection = getInput()
    while selection != 0:    
        print(selection)
        if_expired(collection_name, db)

        if selection == 1:
            addItem(collection_name, db)
        if selection == 2:
            deleteItem(collection_name, db)
        if selection == 4:
            displayItems(collection_name, db)
        
        selection = getInput()
        

# ✅
def getInput():
    # Menu.
    
    print("Menu:")
    print("(0) Quit")
    print("(1) Add Item")
    print("(2) Delete Item")
    print("(3) Edit Item")
    print("(4) Display all items")
    selection = int(input("-- "))
    return selection

# ✅
def addItem(collection_name, db):

    # Get item.
    item_name = input("Item: ")
    
    # Get expiration.
    print("Expiration date")
    date = input("Date: MM/DD/YYYY  ")
    date_items = date.split("/")
    month = int(date_items[0])
    day = int(date_items[1])
    year = int(date_items[2])

    expiration = datetime.datetime(year, month, day)
    db.collection(collection_name).document(item_name).set({"item": item_name, "expirationDate": expiration})

# ✅ 
def displayItems(collection_name, db):
    expired_docs = db.collection("Near Expiration").get()
    sorted_expired_docs = orderByDateTime("Near Expiration", db)
    print("\n\nITEMS TO EXPIRE SOON! ")
    for doc in sorted_expired_docs:
        dictionary = doc.to_dict()
        print(f"  * {dictionary['item']}")
        expiration_date = dictionary["expirationDate"]
        print(f"  - - {expiration_date}")
    print(" - - - - - - - - - - - - - -")
    
    docs = db.collection(collection_name).get()
    results = orderByDateTime(collection_name, db)
    print("\nAll items:")
    for doc in results:
        dictionary = doc.to_dict()
        print(f"  * {dictionary['item']}")
        expiration_date = dictionary["expirationDate"]
        print(f"  - - {expiration_date}")

    


       




def if_expired(collection_name, db):

    docs = db.collection(collection_name).get()
    for doc in docs:
        dictionary = doc.to_dict()
        food_date = str(dictionary["expirationDate"])
        calendar_date = str(datetime.datetime.now() + datetime.timedelta(days = 4))

        if food_date < calendar_date:
            db.collection("Near Expiration").document(dictionary["item"]).set(dictionary)
    

# ✅ 
def deleteItem(collection_name, db):
    item_name = input("Item to be deleted: ")
    db.collection(collection_name).document(item_name).delete()
### Cloud Messaging -> notifacations to operating system 

# ✅ 
def orderByDateTime(collection_name, db):
    cities_ref = db.collection(collection_name)
    query = cities_ref.order_by("expirationDate")
    results = query.stream()
    
    #for doc in results:
    #    print(f'{doc.id} => {doc.to_dict()}')
    return results
main()