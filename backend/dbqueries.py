import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate(
    "./shrdlu-storage-firebase-adminsdk-690pn-c4f962b560.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def test():
    data = {
        u'name': u'Los Angeles',
        u'state': u'CA',
        u'country': u'USA'
    }
    # Add a new doc in collection 'cities' with ID 'LA'
    db.collection('schools').document('school1').set(data)


def storeField(instance, field, data):
    db.collection('shrdlu').document(instance).update({field: data})


def retrieveField(instance, field):
    ref = db.collection('shrdlu')
    docs = ref.stream()

    stringOfData = ""

    for doc in docs:
        if(doc.id == instance):
            stringOfData = doc.to_dict()[field]
    return stringOfData
