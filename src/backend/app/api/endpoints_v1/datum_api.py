from typing import Annotated
from fastapi import APIRouter, HTTPException, Query
from fastapi.params import Body
from sqlalchemy import select

from app.core.dependencies import SessionDepends
from app.models.datum_model import KelasModel
from app.schemas.datums_schema import CreateKelasSchema, KelasOutSchema

router = APIRouter()


# NOTE: Datum Kelas


@router.post("/kelas", status_code=201)
async def crate_kelas(
    *,
    db: SessionDepends,
    kelas: CreateKelasSchema = Body(..., examples=[{"kelas": "nama kelas"}])
):
    query = await db.execute(select(KelasModel).filter_by(kelas=kelas.kelas))
    result = query.scalar()
    if result:
        raise HTTPException(status_code=409, detail="Data kelas is already exists")

    data = KelasModel(kelas=kelas.kelas)
    db.add(data)
    await db.commit()
    await db.refresh(data)
    return {"msg": "Succesfully"}


@router.get(
    "/kelas",
    response_model=list[KelasOutSchema],
)
async def read_all_kelas(
    *,
    db: SessionDepends,
    order_by: Annotated[
        str,
        Query(
            description="order by kelas [asc|des] = default is **asc**",
            enum=["asc", "desc"],
        ),
    ] = "asc"
):
    if order_by == "asc":
        ordered = KelasModel.kelas.asc()
    elif order_by == "desc":
        ordered = KelasModel.kelas.desc()
    else:
        ordered = None

    query = await db.execute(select(KelasModel).order_by(ordered))
    results = query.scalars()

    data: list[dict[str, any]] = []
    for kelas in results:
        data.append({"id": kelas.id, "kelas": kelas.kelas})

    return data
