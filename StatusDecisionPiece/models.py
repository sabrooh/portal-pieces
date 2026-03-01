from pydantic import BaseModel, Field

class InputModel(BaseModel):
    predictions_file: str = Field(
        title="Predictions CSV Path",
        description="Path to the CSV file containing predicted labels."
    )

class OutputModel(BaseModel):
    model_status: str = Field(
        description="Status returned by the decision logic."
    )