from pydantic import BaseModel, Field


class InputModel(BaseModel):
    name: str = Field(
        default="Model 1",
        title="Model Name",
        description="Name of the model whose status will be sent."
    )
    status: str = Field(
        default="ok",
        title="Status",
        description="Status to be sent to the Portal API."
    )
    portal_url: str = Field(
        default="http://172.24.0.1:8002",
        title="Portal URL",
        description="URL of the Portal API endpoint (defaults to localhost)."
    )


class OutputModel(BaseModel):
    returned_status: dict = Field(
        description="JSON response returned by the Portal API."
    )