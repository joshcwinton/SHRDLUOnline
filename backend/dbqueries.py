import pyrebase

config = {
    "apiKey": "AIzaSyB7EsIaeyJ3MnYF_1fjyzNcYFRLNRtx3x0",
    "authDomain": "shrdlu-tdb.firebaseapp.com",
    "databaseURL": "https://shrdlu-tdb-default-rtdb.firebaseio.com",
    "projectId": "shrdlu-tdb",
    "storageBucket": "shrdlu-tdb.appspot.com",
    "messagingSenderId": "420253619610",
    "appId": "1:420253619610:web:c359b6239511f757a6d623",
    "measurementId": "G-YX5PBR5SBQ"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

# stores users message


def archiveSelfMessage(toBeStored):
    db.child("users").child("user1").push({"Me": toBeStored})

# stores bot message


def archiveBotMessage(toBeStored):
    db.child("users").child("user1").push({"SHRDLU": toBeStored})

# retrieves all messages


def retrieveAllMessages():
    print (db.child("users").child("user1").get().val())

# TODO
# store environment
# retireve environment
# store messages more efficiently


# CRUD with firebase
# put data to db
#db.child("names").push({"name": "raunak"})

# update needs to be fitted with json
# db.child("names").child("MYjrJEpvUvoNBufufHw").update({"name":"updoot"})

# get data
#users = db.child("names").child("MYjrJEpvUvoNBufufHw").get()
# print(users.key())

# remove data
# db.child("names").child("MYjrJEpvUvoNBufufHw").remove()
