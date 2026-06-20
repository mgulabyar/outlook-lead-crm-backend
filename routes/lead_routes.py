from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.lead_service import LeadService
from services.db_service import DBService

router = APIRouter(prefix="/api/leads", tags=["Outlook CRM"])


class EmailInput(BaseModel):
    sender: str
    body: str

# asdfasdfasdf
@router.post("/extract-and-sync")
async def extract_and_sync(req: EmailInput):
    try:
        
        if not req.sender or not req.body:
            raise HTTPException(status_code=400, detail="Sender or Body missing")

        lead_info = await LeadService.process_email_to_lead(req.body, req.sender)

        
        status = await DBService.upsert_lead(lead_info, req.sender)

        return {"status": "success", "message": status, "data": lead_info}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
