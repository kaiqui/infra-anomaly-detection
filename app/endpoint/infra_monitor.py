from fastapi import APIRouter
from models.infra import InfraModel
from task.predict import run

router = APIRouter(
    tags=["infra_monitor"],
    responses={404: {"description": "Not found"}},)


@router.post("/anomaly", include_in_schema=True)
async def infra_data(info: InfraModel):
    infra_data = {
        'hour':info.hour,
        'pdis':info.pdis,
        'cpu': info.cpu,
        'mem': info.mem
    }
    res = run.delay(infra_data)
    anomaly = {
        'id':res.id,
        'state':res.state,
        'task_payload':[{
        'result':res.get(timeout=10)}]}
    return anomaly