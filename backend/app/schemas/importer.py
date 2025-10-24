from typing import Dict, List, Optional
from pydantic import BaseModel


class ImportPreviewRequest(BaseModel):
    account_id: Optional[str]
    delimiter: Optional[str] = None
    decimal_separator: Optional[str] = None
    date_format: Optional[str] = None
    skip_rows: int = 0


class ImportPreviewResponse(BaseModel):
    headers: List[str]
    rows: List[Dict[str, str]]
    suggested_mapping: Dict[str, str]
    duplicates: int = 0


class ImportCommitRequest(BaseModel):
    account_id: str
    mapping: Dict[str, str]
    rules_enabled: bool = True
    template_name: Optional[str]


class ImportCommitResponse(BaseModel):
    processed: int
    duplicates: int
    skipped: int
