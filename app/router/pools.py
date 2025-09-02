from fastapi import APIRouter, Depends
from sqlalchemy import Table
from sqlalchemy.engine import Result
from ..database import get_db, engine, pool_table
import time

router = APIRouter(prefix="/api/v1", tags=["oroswappools"])

@router.get("/pools", status_code=200)
async def get_pools(db=Depends(get_db), limit: int = 10 , offset: int = 0):
    start_time = time.time()
    execution_time = 0.0

    if pool_table is None:
        return {"error": "Table not found"}

    try:
        with engine.connect() as conn:
            result: Result = conn.execute(pool_table.select().limit(limit).offset(offset))
            pools = [dict(row._mapping) for row in result]
            execution_time = time.time() - start_time
            count = len(pools)
            print(f"Fetched {len(pools)} pools in {execution_time:.4f} seconds")

        return {"pools": pools, "count": count, "execution_time": f"{execution_time:.4f}s"}

    except Exception as e:
        return {"error": str(e)}