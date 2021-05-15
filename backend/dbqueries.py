import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate(
    "./shrdlu-storage2-firebase-adminsdk-4zbgr-ae1cfe53f9.json"
)
firebase_admin.initialize_app(cred)

db = firestore.client()

"""
test function
"""


def test():
    data = {u"name": u"Los Angeles", u"state": u"CA", u"country": u"USA"}
    db.collection("schools").document("school1").set(data)


"""
given instance, field, and data function stores it as a string
"""


def storeField(instance, field, data):
    db.collection("instances").document(instance).update({field: data})


"""
given instance, field the function returns data as a string
turning back into real data type is done inside setter
"""


def retrieveField(instance, field):
    ref = db.collection("instances")
    docs = ref.stream()

    stringOfData = ""

    for doc in docs:
        if doc.id == instance:
            stringOfData = doc.to_dict()[field]
    return stringOfData


"""
Query for making an empty collection with the wanted fields initialized
"""


def createInstanceStorage(worldName, creator, size):
    new_ref = db.collection("instances").document()

    new_ref.set(
        {
            "worldName": worldName,
            "creator": creator,
            "size": size,
            "grid": str(
                [[("", "", 0) for i in range(int(size))]
                 for j in range(int(size))]
            ),
            "history": "[]",
            "messages": "[]",
        }
    )


"""
Query to get: worldName, creator, size from all documents
Return type List of List, inner list holds each field value as a string, outer holds each document fields
"""


def getAllStoredInstances(collectionName):
    docs = db.collection(collectionName).stream()

    instancesBio = []
    for doc in docs:
        ele = []
        temp = doc.to_dict()
        ele.append(str(doc.id))
        ele.append(temp["worldName"])
        ele.append(temp["creator"])
        ele.append(temp["size"])

        instancesBio.append(ele)
    return instancesBio
