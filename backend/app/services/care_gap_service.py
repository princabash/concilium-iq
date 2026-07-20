"""Care Gap Service stub"""
class CareGapService:
    def __init__(self, db):
        self.db = db
    async def get_for_patient(self, patient_id):
        return []
