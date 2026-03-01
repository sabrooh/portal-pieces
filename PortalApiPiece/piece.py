import requests
from domino.base_piece import BasePiece
from .models import InputModel, OutputModel


class PortalApiPiece(BasePiece):
    """
    Domino piece that sends a model name + status to a Portal API endpoint.
    POSTs to {portal_url}/models with the JSON body:
        {"name": "<model_name>", "status": "<status>"}
    """

    def piece_function(self, input_data: InputModel):
        url = f"{input_data.portal_url.rstrip('/')}/models"

        payload = {
            "name": input_data.name,
            "status": input_data.status
        }

        response = requests.post(
            url,
            json=payload,  
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()

        returned_status = response.json()  
        return OutputModel(returned_status=returned_status)