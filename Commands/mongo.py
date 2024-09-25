from pymongo import MongoClient
import certifi

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://Cluster60849:S2NxfHFnXmhP@cluster60849.p6ste.mongodb.net/"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING,tlsCAFile=certifi.where())
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['users_to_do_lists']


   
# This is added so that many files can reuse the function get_database()
#if __name__ == "__main__":   
#  
#   # Get the database
#   dbname = get_database()