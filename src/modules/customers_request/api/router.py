from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.modules.auth.api.dependencies import CurrentUser, get_current_user
from src.modules.customers_request.api.dependencies import get_order_mediator
from src.modules.customers_request.api.schemas import RequestCreateOrder, ResponseOrder, ResponseOrderItem
from src.modules.customers_request.application.commands.create_order import CreateOrderCommand, CreateOrderItem
from src.modules.customers_request.application.queries.get_by_id import GetOrderByIdQuery
from src.modules.customers_request.domain.exceptions import DifferentCurrencyInOrderError, EmptyOrderError, OrderAccessDeniedError, OrderNotFoundError, ProductForOrderNotFoundError
from src.shared.application.mediator import Mediator

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)

@router.post(
    "",
    response_model=ResponseOrder,
    status_code=status.HTTP_201_CREATED,
    )
async def create_order(
    request: RequestCreateOrder,
    current_user: CurrentUser = Depends(get_current_user),
    mediator: Mediator = Depends(get_order_mediator),
) -> ResponseOrder:
    cmd = CreateOrderCommand(
        buyer_id=current_user.id,
        items=list(
            CreateOrderItem(
                menu_item_id=item.menu_item_id,
                quantity=item.quantity,
            )
            for item in request.items
        )
    )
    
    try:
        order = await mediator.send(cmd)
    except EmptyOrderError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except DifferentCurrencyInOrderError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except ProductForOrderNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    
    return ResponseOrder(
        id=order.id,
        buyer_id=order.buyer_id,
        total_price_amount=order.total_price.amount,
        total_price_currency=order.total_price.currency,
        status=order.status.value,
        items=list(
            ResponseOrderItem(
                menu_item_id=item.menu_item_id,
                title=item.menu_item_title_snapshot,
                price_amount=item.price_snapshot.amount,
                price_currency=item.price_snapshot.currency,
                quantity=item.quantity,
            )
            for item in order._items
        ),
        created_at=order.created_at,
    )

@router.get(
    "/{order_id}",
    response_model=ResponseOrder,
    status_code=status.HTTP_200_OK,
)
async def get_order_by_id(
    order_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    mediator: Mediator = Depends(get_order_mediator),
) -> ResponseOrder:
    query = GetOrderByIdQuery(
        order_id=order_id,
        buyer_id=current_user.id,
    )

    try:
        order = await mediator.send(query)
    except OrderNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except OrderAccessDeniedError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc

    return ResponseOrder(
        id=order.id,
        buyer_id=order.buyer_id,
        total_price_amount=order.total_price_amount,
        total_price_currency=order.total_price_currency,
        status=order.status,
        items=[
            ResponseOrderItem(
                menu_item_id=item.menu_item_id,
                title=item.menu_item_title_snapshot,
                price_amount=item.price_amount_snapshot,
                price_currency=item.price_currency_snapshot,
                quantity=item.quantity,
            )
            for item in order.items
        ],
        created_at=order.created_at,
    )