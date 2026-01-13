from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional, Any
import httpx
import asyncio

from gateway.app.services.policy import apply_policy
from gateway.app.services.rate_limit import check_rate_limit

router = APIRouter(prefix="/v1")


class RelayRequest(BaseModel):
    method: str
    url: str
    headers: Dict[str, str] = {}
    body: Optional[Any] = None
    policy: Optional[str] = "standard"


@router.post("/relay")
async def relay(req: RelayRequest):

    await check_rate_limit(
        key="global",
        limit=5,              # allow 5 requests per window
        window_seconds=60     # 60-second window
    )

    shaped = apply_policy(req.policy or "standard", req.headers)

    if shaped["jitter_ms"] > 0:
        await asyncio.sleep(shaped["jitter_ms"] / 1000)

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.request(
                method=req.method.upper(),
                url=req.url,
                headers=shaped["headers"],
                json=req.body,
            )
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return {
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "body": response.text[:10_000],
        "policy": req.policy,
        "jitter_applied_ms": shaped["jitter_ms"],
    }
