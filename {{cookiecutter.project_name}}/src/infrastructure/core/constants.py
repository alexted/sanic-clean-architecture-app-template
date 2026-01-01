from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error: str
    message: str
    request_id: str
    timestamp: str


responses = {
    403: {"model": ErrorResponse, "description": "Not enough privileges"},
    422: {"model": ErrorResponse, "description": "Validation error"},
    500: {"model": ErrorResponse, "description": "Internal error"},
}
