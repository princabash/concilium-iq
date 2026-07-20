"""
Concilium IQ™ — Neo4j Seed Data
"""

import asyncio
from app.graph.neo4j_client import Neo4jClient


async def seed_neo4j():
    """Seed Neo4j with initial clinical knowledge"""
    client = Neo4jClient()
    try:
        await client.seed_knowledge_graph()
        print("✅ Neo4j Knowledge Graph seeded successfully")
    except Exception as e:
        print(f"⚠️ Neo4j seeding error: {e}")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(seed_neo4j())
