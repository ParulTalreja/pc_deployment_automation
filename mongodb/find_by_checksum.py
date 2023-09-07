from pymongo import MongoClient

def find_in_mongodb(checksum):
  client = MongoClient()
  db_triage = client.triage
  collection_checksum = db_triage.checksum
  document = collection_checksum.find_one({"checksum": checksum})
  if not document:
    print("checksum not present")
  else:
    return document

# def main():
#   checksum = "1539d9301a5c518935e00198b4a5d3bf"
#   document = find_in_mongodb(checksum)
#   print(document)

# if __name__ == "__main__":
#   main()