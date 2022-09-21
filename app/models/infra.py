from pydantic import (
    BaseModel,
    Field
)

class InfraModel(BaseModel):
    hour: int = Field()
    pdis: int = Field()
    cpu: float = Field()
    mem: float = Field()