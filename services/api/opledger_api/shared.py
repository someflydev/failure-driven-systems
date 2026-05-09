from typing import Annotated

from fastapi import Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session

from opledger_api.config import Settings, get_settings
from opledger_api.db import get_db_session

SessionDependency = Annotated[Session, Depends(get_db_session)]
SettingsDependency = Annotated[Settings, Depends(get_settings)]
LimitQuery = Annotated[int, Query(ge=1, le=100)]
OffsetQuery = Annotated[int, Query(ge=0)]
IdempotencyKeyHeader = Annotated[
    str | None,
    Header(alias="Idempotency-Key", min_length=1, max_length=191),
]


def error_response(
    status_code: int,
    code: str,
    message: str,
    details: object | None = None,
) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail={"error": {"code": code, "message": message, "details": details}},
    )
