import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


class DBService:
    # Local MongoDB connection using your URI
    client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    db = client.get_database(os.getenv("DB_NAME"))
    collection = db.get_collection("leads")

    @classmethod
    async def upsert_lead(cls, lead_data, email):
        # Email as a unique identifier for CRM
        lead_data["email"] = email
        lead_data["last_contacted"] = datetime.utcnow()

        # MongoDB Upsert Logic: Agar email pehle se hai to update, warna insert
        result = await cls.collection.update_one(
            {"email": email}, {"$set": lead_data}, upsert=True
        )

        if result.matched_count > 0:
            return "Lead Updated Successfully"
        else:
            return "New Lead Created in CRM"

    @classmethod
    async def get_history(cls):
        # Latest 5 leads for the UI history tab
        cursor = cls.collection.find().sort("last_contacted", -1).limit(5)
        leads = []
        async for doc in cursor:
            # ObjectId fix for JSON serialization
            doc["_id"] = str(doc["_id"])
            leads.append(doc)
        return leads
