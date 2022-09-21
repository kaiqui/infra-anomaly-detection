from endpoint import infra_monitor
from fastapi import FastAPI
from fastapi.responses import RedirectResponse


app = FastAPI()


app.include_router(
    infra_monitor.router,
    prefix="/v1",
    responses={418: {"description": "only a test"}},
)

@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')

@app.get('/ping', include_in_schema=True)
async def ping():
    return {'ping':'pong'}