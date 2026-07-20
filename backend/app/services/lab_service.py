"""Lab Service stub"""
class LabService:
    def __init__(self, db):
        self.db = db
    async def create(self, patient_id, labs):
        pass
    async def get_history(self, patient_id):
        return []
