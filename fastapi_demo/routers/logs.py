from bson import ObjectId
from fastapi import APIRouter

from fastapi_demo.mongodb import api_call_log

router = APIRouter(prefix="/logs", tags=["Logs"])

# Range-Based Pagination Api Call Log
@router.get("/logs")
async def get_logs(limit: int = 10, last_id: str = None):
    query = {}
    if last_id:
        query["_id"] = {"$lt": ObjectId(last_id)}
    cursor = (
        api_call_log.find(query)
        .sort("_id", -1)
        .limit(limit)
    )
    logs = []
    async for doc in cursor:
        logs.append(doc)
    for log in logs:
        log["_id"] = str(log["_id"])
    return {
        "logs": logs,
        "next_cursor": logs[-1]["_id"] if logs else None
    }