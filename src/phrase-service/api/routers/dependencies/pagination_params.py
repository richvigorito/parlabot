from pydantic import BaseModel
from typing import Optional
from fastapi import Query

class PaginationParams(BaseModel):
    limit: Optional[int] = 1000
    offset: Optional[int] = 0

def get_pagination_params(
    limit: int = Query(1000, ge=1, le=1000),
    offset: int = Query(0, ge=0)
) -> PaginationParams:
    return PaginationParams(limit=limit, offset=offset)

