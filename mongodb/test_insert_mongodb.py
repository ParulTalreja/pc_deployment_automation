from pymongo import MongoClient

def insert_in_mongodb(checksum, static_resolution=None, jira=None):

  dict = \
  {
    "checksum" : checksum,
    "static_resolution" : static_resolution,
    "jira" : jira
  }
  client = MongoClient()
  db_triage = client.triage
  checksum = db_triage.checksum

  x = checksum.insert_one(dict)
  print("Document inserted with id: ", x.inserted_id)

def main():
  print("inside main: ")
  insert_in_mongodb("1539d9301a5c518935e00198b4a5d3bf", "test_from_python")

if __name__ == "__main__":
  main()