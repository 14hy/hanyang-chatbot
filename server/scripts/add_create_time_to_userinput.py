from google.cloud.firestore_v1 import DocumentSnapshot, CollectionReference

from db.connect import client

collection: CollectionReference = client.collection("user_input")
for each in collection.stream():
    each: DocumentSnapshot
    create_time = each.create_time

    doc_id = each.id
    ret = collection.document(doc_id).update({"create_time": create_time.seconds})
    print(each._data.get("text"))
    print(ret)
