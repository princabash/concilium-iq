"""
Concilium IQ™ — Neo4j Graph Client
"""

from neo4j import AsyncGraphDatabase
from typing import List, Dict, Any, Optional

from app.config import settings


class Neo4jClient:
    """Async Neo4j client for Clinical Knowledge Graph"""

    def __init__(self):
        self.driver = AsyncGraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )

    async def close(self):
        await self.driver.close()

    async def seed_knowledge_graph(self):
        """Seed initial clinical knowledge graph data"""
        async with self.driver.session() as session:
            # Create guideline nodes
            await session.run("""
                CREATE (g:Guideline {name: 'ESC/EAS 2019', type: 'dyslipidemia'})
                CREATE (g2:Guideline {name: 'ACC/AHA 2018', type: 'cholesterol'})
                CREATE (g3:Guideline {name: 'ADA 2024', type: 'diabetes'})
            """)

            # Create risk category nodes
            await session.run("""
                CREATE (r:RiskCategory {name: 'Very High', ldl_target: 55})
                CREATE (r2:RiskCategory {name: 'High', ldl_target: 70})
                CREATE (r3:RiskCategory {name: 'Moderate', ldl_target: 100})
                CREATE (r4:RiskCategory {name: 'Low', ldl_target: 116})
            """)

            # Create relationships
            await session.run("""
                MATCH (g:Guideline {name: 'ESC/EAS 2019'})
                MATCH (r:RiskCategory)
                CREATE (g)-[:RECOMMENDS]->(r)
            """)

    async def get_patient_graph(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """Get patient-related subgraph"""
        async with self.driver.session() as session:
            result = await session.run("""
                MATCH (p:Patient {patient_id: $patient_id})
                OPTIONAL MATCH (p)-[:HAS_LAB]->(l:LabResult)
                OPTIONAL MATCH (p)-[:HAS_RISK]->(r:RiskAssessment)
                RETURN p, collect(l) as labs, collect(r) as risks
            """, patient_id=patient_id)
            record = await result.single()
            if record:
                return {
                    "patient": dict(record["p"]),
                    "labs": [dict(l) for l in record["labs"]],
                    "risks": [dict(r) for r in record["risks"]],
                }
            return None
