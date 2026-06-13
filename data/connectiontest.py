from pymongo import MongoClient
import certifi
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGO_URI")

print(uri[:60])

client = MongoClient(
    uri,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=5000
)

print("Testing...")

print(client.admin.command("ping"))