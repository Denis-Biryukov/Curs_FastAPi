from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,)

import uvicorn

from test import router as test_router
from hotels import router as hotels_router




app = FastAPI()
app.include_router(test_router, tags=["Тесты"])
app.include_router(hotels_router, tags=["Отели"])







# @app.get("/docs", tags=["docs"])
# async def custom_swagger_ui_html():
#     return get_swagger_ui_html(
#         # openapi_url=app.openapi_url,
#         title=app.title + " - Swagger UI",
#         # oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
#         swagger_js_url="https://unpq.com/swagger-ui-dast@5/swagger-ui-boudle.js",
#     )







if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
