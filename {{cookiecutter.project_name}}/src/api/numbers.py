from sanic import Blueprint, Request, response
from sanic_ext import validate
from src.domain.use_cases.numbers import (
    DivideRequest, DivideResponse, DivideUseCase,
    MultiplyRequest, MultiplyResponse, MultiplyUseCase,
    SubtractRequest, SubtractResponse, SubtractUseCase,
    SummariseRequest, SummariseResponse, SummariseUseCase
)

bp = Blueprint("numbers", url_prefix="/numbers")

@bp.post("/summarise")
@validate(json=SummariseRequest)
async def summarise_numbers(request: Request, body: SummariseRequest, use_case: SummariseUseCase):
    result = await use_case.execute(body)
    return response.json(result.model_dump())

@bp.get("/subtract")
async def subtract_numbers(request: Request, use_case: SubtractUseCase):
    # В Sanic параметры Query берутся из request.args
    args = request.args
    request_object = SubtractRequest(
        left_number=int(args.get("minuend")),
        right_number=int(args.get("subtrahend"))
    )
    result = await use_case.execute(request_object)
    return response.json(result.model_dump())

@bp.put("/multiply")
@validate(json=MultiplyRequest)
async def multiply_numbers(request: Request, body: MultiplyRequest, use_case: MultiplyUseCase):
    result = await use_case.execute(body)
    return response.json(result.model_dump())

@bp.delete("/divide")
async def divide_numbers(request: Request, use_case: DivideUseCase):
    args = request.args
    request_object = DivideRequest(
        dividend=int(args.get("dividend")),
        divisor=int(args.get("divisor"))
    )
    result = await use_case.execute(request_object)
    return response.json(result.model_dump())