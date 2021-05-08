import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate(
    "./shrdlu-storage-firebase-adminsdk-690pn-c4f962b560.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

'''
test function
'''
def test():
    data = {
        u'name': u'Los Angeles',
        u'state': u'CA',
        u'country': u'USA'
    }
    # Add a new doc in collection 'cities' with ID 'LA'
    db.collection('schools').document('school1').set(data)


'''
given instance, field, and data function stores it as a string
'''
def storeField(instance, field, data):
    db.collection('shrdlu').document(instance).update({field: data})


'''
given instance, field the function returns data as a string
turning back into real data type is done inside setter
'''
def retrieveField(instance, field):
    ref = db.collection('shrdlu')
    docs = ref.stream()

    stringOfData = ""

    for doc in docs:
        if(doc.id == instance):
            stringOfData = doc.to_dict()[field]
    return stringOfData


'''
query for making an empty collection with the wanted fields initialized
'''
def createInstanceStorage(worldName, creator, size):
    new_ref = db.collection('instances').document()

    new_ref.set({
        'worldName': worldName,
        'creator': creator,
        'size': size,
        'grid': "",
        'history': "",
        'messages': "",
    })


'''
query to return all stored instances ids
GH TASK: get all instances returns stuff on instance page
'''
def getAllStoredInstances(collectionName):
    docs = db.collection(collectionName).stream()

#in each doc get worldName, creator, size

    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')

'''
query to return all stored instances ids
'''





