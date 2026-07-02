from math import ceil
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.modules.admin.api.schemas import AdminCustomerRequestsPageResponse
from src.modules.customer_requests.application.commands.change_customer_request_status import ChangeCustomerRequestStatusCommand
from src.modules.customer_requests.application.queries.get_customer_request_by_id import GetCustomerRequestByIdQuery
from src.modules.customer_requests.application.queries.list_customer_requests import ListCustomerRequestsQuery
from src.modules.customer_requests.domain.enums import CustomerRequestStatus, CustomerRequestType
from src.modules.customer_requests.domain.exceptions import CustomerRequestNotFound
from src.modules.auth.api.dependencies import CurrentUser, require_admin
from src.modules.customer_requests.api.dependencies import get_customer_requests_mediator
from src.modules.customer_requests.api.schemas import CustomerRequestResponse, RequestItemResponse
from src.shared.application.mediator import Mediator

router = APIRouter(
    prefix="/admin/customer-requests",
    tags=["Admin Customer Requests"],
)

@router.get(
    "",
    response_model=AdminCustomerRequestsPageResponse,
    status_code=status.HTTP_200_OK,
)
async def get_customer_requests(
    status_filter: CustomerRequestStatus | None = Query(default=None, alias="status"),
    request_type: CustomerRequestType | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=40, ge=1, le=100),
    mediator: Mediator = Depends(get_customer_requests_mediator),
    current_user: CurrentUser = Depends(require_admin)
) -> AdminCustomerRequestsPageResponse:
    result = await mediator.send(
        ListCustomerRequestsQuery(
            status=status_filter,
            request_type=request_type,
            page=page,
            page_size=page_size,
        )
    )
    total_pages = ceil(result.total / page_size) if result.total else 1
    
    return AdminCustomerRequestsPageResponse(
        items=result.items,
        total=result.total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )

@router.get(
    "/{request_id}",
    response_model=CustomerRequestResponse,
    status_code=status.HTTP_200_OK,
)
async def get_customer_request_by_id(
    request_id: UUID,
    mediator: Mediator = Depends(get_customer_requests_mediator),
    current_user: CurrentUser = Depends(require_admin)
) -> CustomerRequestResponse:
    query = GetCustomerRequestByIdQuery(request_id=request_id)
    try:
        result = await mediator.send(query)
        return CustomerRequestResponse(
            request_type=result.request_type,
            customer_name=result.customer_name,
            contact=result.contact,
            desired_datetime=result.desired_datetime,
            person_count=result.person_count,
            comment=result.comment,
            status=result.status,
            items=[
                RequestItemResponse(
                    menu_item_id=item.id,
                    title=item.title,
                    quantity=item.quantity,
                    price_amount=item.price_amount,
                    price_currency=item.price_currency,
                    comment=item.comment,
                )
                for item in result.items
            ],
            created_at=result.created_at,
            updated_at=result.updated_at,
        )
        
    except CustomerRequestNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

@router.patch(
    "/{request_id}/status",
    response_model=CustomerRequestResponse,
    status_code=status.HTTP_200_OK,
)
async def patch_customer_request_status(
    request_id: UUID,
    new_status: CustomerRequestStatus = Query(alias="status"),
    mediator: Mediator = Depends(get_customer_requests_mediator),
    current_user: CurrentUser = Depends(require_admin)
) -> CustomerRequestResponse:
    cmd = ChangeCustomerRequestStatusCommand(
        request_id=request_id,
        status=new_status,
    )
    try:
        resust = await mediator.send(cmd)
    except CustomerRequestNotFound as exc:
        raise HTTPException(
            status_code=new_status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )