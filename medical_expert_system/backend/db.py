"""MongoDB integration for MedPredict"""
import os
from datetime import datetime, timedelta

MONGO_AVAILABLE = False
_db = None

# Hardcoded URI — no .env dependency
MONGO_URI = "mongodb+srv://meduser:medpass123@cluster0.41heu6j.mongodb.net/?appName=Cluster0"
MONGO_DB  = "medpredict"

try:
    from pymongo import MongoClient
    _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=8000)
    _client.server_info()  # force connection check
    _db = _client[MONGO_DB]
    MONGO_AVAILABLE = True
    print("[MongoDB] Connected successfully")
except Exception as _e:
    print(f"[MongoDB] Connection failed: {_e}")


def save_record(record: dict) -> str:
    if not MONGO_AVAILABLE or _db is None:
        return ""
    try:
        record["timestamp"] = datetime.utcnow()
        result = _db.diagnoses.insert_one(record)
        return str(result.inserted_id)
    except Exception as e:
        print(f"[MongoDB] Save failed: {e}")
        return ""


def get_records(search: str = "", limit: int = 100) -> list:
    if not MONGO_AVAILABLE or _db is None:
        return []
    try:
        query = {}
        if search:
            query = {"$or": [
                {"name": {"$regex": search, "$options": "i"}},
                {"primary_diagnosis": {"$regex": search, "$options": "i"}},
                {"risk_level": {"$regex": search, "$options": "i"}},
            ]}
        cursor = _db.diagnoses.find(query, {"_id": 0}).sort("timestamp", -1).limit(limit)
        return list(cursor)
    except Exception as e:
        print(f"[MongoDB] Get records failed: {e}")
        return []


def get_analytics() -> dict:
    if not MONGO_AVAILABLE or _db is None:
        return {}
    try:
        total = _db.diagnoses.count_documents({})
        disease_pipeline = [
            {"$group": {"_id": "$primary_diagnosis", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}, {"$limit": 10}
        ]
        diseases = {d["_id"]: d["count"] for d in _db.diagnoses.aggregate(disease_pipeline)}
        risk_pipeline = [{"$group": {"_id": "$risk_level", "count": {"$sum": 1}}}]
        risks = {r["_id"]: r["count"] for r in _db.diagnoses.aggregate(risk_pipeline)}
        daily_pipeline = [
            {"$match": {"timestamp": {"$gte": datetime.utcnow() - timedelta(days=7)}}},
            {"$group": {"_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}}, "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ]
        daily = {d["_id"]: d["count"] for d in _db.diagnoses.aggregate(daily_pipeline)}
        sym_pipeline = [
            {"$unwind": "$symptoms"},
            {"$group": {"_id": "$symptoms", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}, {"$limit": 10}
        ]
        symptoms = {s["_id"]: s["count"] for s in _db.diagnoses.aggregate(sym_pipeline)}
        high_risk = _db.diagnoses.count_documents({"risk_level": {"$in": ["High", "Critical"]}})
        return {
            "total": total, "diseases": diseases, "risks": risks,
            "daily": daily, "symptoms": symptoms,
            "high_risk_pct": round(high_risk / total * 100, 1) if total else 0,
        }
    except Exception as e:
        print(f"[MongoDB] Analytics failed: {e}")
        return {}
