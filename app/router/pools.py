from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Table
from sqlalchemy.engine import Result
from ..database import get_db, engine, pool_table, transactions_table, holders_table
import time

router = APIRouter(prefix="/api/v1", tags=["oroswappools"])

@router.get("/pools", status_code=200)
async def get_pools(limit: int = 10 , offset: int = 0):
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
        print("Error fetching pools:", str(e))
        return {"error": HTTPException(status_code=500, detail="Internal Server Error")}
    
@router.get("/pool/{address}", status_code=200)
async def get_pool_by_address(address: str):
    start_time = time.time()
    execution_time = 0.0

    if pool_table is None:
        return {"error": "Table not found"}

    try:
        with engine.connect() as conn:
            result: Result = conn.execute(pool_table.select().where(pool_table.c.pair_contract == address))
            pool = [dict(row._mapping) for row in result]
            execution_time = time.time() - start_time
            count = len(pool)
            print(f"Fetched pool {address} in {execution_time:.4f} seconds")

        if count == 0:
            return {"message": "Pool not found"}

        return {"pool": pool[0], "execution_time": f"{execution_time:.4f}s"}

    except Exception as e:
        print("Error fetching pool:", str(e))
        return {"error": HTTPException(status_code=500, detail="Internal Server Error")}
    
@router.get("/pool/transactions/{address}", status_code=200)
def get_pool_transactions(address: str, limit: int = 10 , offset: int = 0):
    start_time = time.time()
    execution_time = 0.0

    if transactions_table is None:
        return {"error": "Table not found"}

    try:
        with engine.connect() as conn:
            result: Result = conn.execute(transactions_table.select().where(transactions_table.c.pair_contract == address).limit(limit).offset(offset))
            transactions = [dict(row._mapping) for row in result]
            execution_time = time.time() - start_time
            count = len(transactions)
            print(f"Fetched {len(transactions)} transactions for pool {address} in {execution_time:.4f} seconds")

        return {"transactions": transactions, "count": count, "execution_time": f"{execution_time:.4f}s"}

    except Exception as e:
        print("Error fetching transactions:", str(e))
        return {"error": HTTPException(status_code=500, detail="Internal Server Error")}

@router.get("/denom/holders/{denomaddress}", status_code=200)
def get_denom_holders(denomaddress: str, limit: int = 10 , offset: int = 0):
    start_time = time.time()
    execution_time = 0.0

    if holders_table is None:
        return {"error": "Table not found"}

    try:
        with engine.connect() as conn:
            result: Result = conn.execute(holders_table.select().where(holders_table.c.denom == denomaddress).limit(limit).offset(offset))
            holders = [dict(row._mapping) for row in result]
            execution_time = time.time() - start_time
            count = len(holders)
            print(f"Fetched {len(holders)} holders for denom {denomaddress} in {execution_time:.4f} seconds")

        return {"holders": holders, "count": count, "execution_time": f"{execution_time:.4f}s"}

    except Exception as e:
        print("Error fetching holders:", str(e))
        return {"error": HTTPException(status_code=500, detail="Internal Server Error")}
