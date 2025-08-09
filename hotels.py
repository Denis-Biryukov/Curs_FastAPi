
from fastapi import Query, Body, APIRouter
from pydantic import BaseModel

from dependencies import PaginationDep

router = APIRouter(prefix="/hotels")

class Hotel(BaseModel):
    title: str
    description: str


hotels = [
    {"id": 1, "title": "Москва", "description": "Hotel in Moscow"},
    {"id": 2, "title": "Лондон", "description": "Hotel in London"},
    {"id": 3, "title": "Париж", "description": "Hotel in Paris"},
    {"id": 4, "title": "Dubai", "description": "Hotel in Dubai"},
    {"id": 5, "title": "Мальдивы", "description": "Hotel in Maldivi"},
    {"id": 6, "title": "Kazan", "description": "Hotel in Kazan"},
    {"id": 7, "title": "New York", "description": "Hotel in New York"},
    {"id": 8, "title": "Saransk", "description": "Hotel in Saransk"}
]


@router.get("/", summary="Показать отели")
async def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="id"),
        title: str | None = Query(None, description="Название отеля")

):
    # global hotels
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    # return [hotel for hotels_ [per_page: page]]

    # return hotels_[((pagination.page - 1) * pagination.per_page):(pagination.per_page * pagination.page)]
    return hotels_[(pagination.page - 1) * pagination.per_page:][:pagination.per_page]


@router.post("", summary="Добавить отель")
async def creat_hotel(data: Hotel
        # title: str = Body(),
        # description: str = Body(),
):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": data.title,
            "description": data.description,
        }
    )
    return {"status": "Ok"}


@router.put("/{hotel_id}", summary="Изменить отель")
async def update_all_hotel(
        hotel_id: int,
        title: str = Body(),
        description: str = Body(),
        ):
    global hotels

    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = title
    hotel["description"] = description

    # for hotel in hotels:
    #     if hotel_id and hotel["id"] == hotel_id:
    #         hotel["title"] = title
    #
    #         hotel["description"] = description
    return {"update": "Ok", "hotels": hotels}


@router.patch("/{hotel_id}", summary="Внести изменения в отель")
async def update_hotel(
        hotel_id: int,
        title: str | None = Body(default=None),
        description: str | None = Body(default=None),
):
    global hotels

    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if title:
        hotel["title"] = title
    if description:
        hotel["description"] = description
    return { "hotel": hotel, "update": "Ok"}
    # for hotel in hotels:
    #     if hotel_id and hotel["id"] == hotel_id and title != "string" and description != "string":
    #         hotel["title"] = title
    #         hotel["description"] = description
    #     elif hotel_id and hotel["id"] == hotel_id and title != "string":
    #         hotel["title"] = title
    #     elif hotel_id and hotel["id"] == hotel_id and description != "string":
    #         hotel["description"] = description
    #     else:
    #         return {"update": False, "message": "Изменений нет"}
    #
    #     return {"update": "Ok", "hotels": hotels}



@router.delete("/{hotel_id}", summary="Удалить отель")
async def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "Ok"}