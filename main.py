from fastapi import FastAPI, Query, Body
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html)
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


import uvicorn


app = FastAPI()



@app.get("/docs")
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpq.com/swagger-ui-dast@5/swagger-ui-boudle.js",
    )




hotels = [
    {"id": 1, "title": "Москва", "description": "Hotel in Moscow"},
    {"id": 2, "title": "Лондон", "description": "Hotel in London"},
    {"id": 3, "title": "Париж", "description": "Hotel in Paris"},
]


@app.get("/hotels", summary="Показать отели")
async def get_hotels(
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
    return hotels_

@app.post("/hotels", summary="Добавить отель")
async def creat_hotel(
        title: str = Body(embed=True),
        description: str = Body(embed=True),
):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": title,
            "description": description,
        }
    )
    return {"status": "Ok"}


@app.put("/hotels/{hotel_id}", summary="Изменить отель")
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


@app.patch("/hotels/{hotel_id}", summary="Внести изменения в отель")
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



@app.delete("/hotels/{hotel_id}", summary="Удалить отель")
async def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "Ok"}




if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
