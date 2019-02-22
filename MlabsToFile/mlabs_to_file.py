import re
import pymongo
client = pymongo.MongoClient('mongodb://user:password123@ds123963.mlab.com:23963/project', connectTimeoutMS=300000)
db = client.get_default_database()
flipkart_data = db.flipkart_data

f = open("op.txt", "w")




for document in flipkart_data.find():
    print(document) # iterate the cursor
    for key in document:
        if(key == "model name"):
            f.write(str(document[key]) + "\t" + "model\n");
        else:
            f.write(key + "\t" + "attribute\n")
            f.write(str(document[key]) + "\t" + "data\n")

k = 0;