from dotenv import load_dotenv
from google import genai

genai_client = genai.Client()


def replace_mongo_id(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc
