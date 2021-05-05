import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("./shrdlu-storage-firebase-adminsdk-690pn-c4f962b560.json")
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

def setMessages(instance, data):
	db.collection('shrdlu').document(instance).update({'messy': data})

def getMess(instance):
	ref = db.collection('shrdlu')
	docs = ref.stream()

	strry = ""

	for doc in docs:
		if(doc.id == instance):
			test = doc.to_dict()
			strry = test['messy']
			
	return strry
			
 		#print(f'{doc.id} => {doc.to_dict()}')