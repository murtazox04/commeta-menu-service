from typing import List
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider
from app.infrastructure.database.dao import HolderDao

router = APIRouter(prefix="/discounts", tags=["discounts"])

@router.get("/", response_model=List[dto.Discount])
async def get_discounts(
        dao: HolderDao = Depends(dao_provider)
) -> List[dto.Discount]:
    try:
        discounts = await dao.discount.get_discounts()
        if not discounts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discounts not found")
        return discounts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", response_model=dto.Discount)
async def create_discount(
        discount: schems.DiscountCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Discount:
    try:
        created_discount = await dao.discount.add_discount(discount)
        return created_discount
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{discount_id}", response_model=dto.Discount)
async def get_discount(
        discount_id: int,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Discount:
    try:
        discount = await dao.discount.get_discount(discount_id)
        if not discount:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discount not found")
        return discount
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{discount_id}", response_model=dto.Discount)
async def update_discount(
        discount_id: int,
        discount_update: schems.DiscountCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Discount:
    try:
        updated_discount = await dao.discount.update_discount(discount_id, discount_update)
        if not updated_discount:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discount not found")
        return updated_discount
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{discount_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_discount(
        discount_id: int,
        dao: HolderDao = Depends(dao_provider)
):
    try:
        deleted = await dao.discount.delete_discount(discount_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discount not found")
        return JSONResponse(
            content={"message": "The discount is successfully deleted"},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
