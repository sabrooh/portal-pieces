import pandas as pd
from pathlib import Path
from domino.base_piece import BasePiece
from .models import InputModel, OutputModel


# --- Fill these in later ---
FLAMMABLE_SPECIES = set()      
CONIFEROUS_SPECIES = set()      
RAPID_GROWTH_SPECIES = set()   
LARGE_CROWN_SPECIES = set()
LATEST_MODEL_VERSION = "1.0"   


class StatusDecisionPiece(BasePiece):

    def piece_function(self, input_data: InputModel):
        predictions_path = Path(input_data.predictions_file)
        if not predictions_path.exists():
            raise FileNotFoundError(f"Predictions file not found: {predictions_path}")

        df = pd.read_csv(predictions_path)
        total = len(df)

        # --- Compute metrics from CSV ---
        class_conf_min = df["confidence"].min()
        main_class = df["prediction"].mode()[0]

        # 0 until filled in 
        in_class_max = (
            df[df["prediction"].isin(FLAMMABLE_SPECIES)].shape[0] / total * 100
            if FLAMMABLE_SPECIES else 0
        )
        con_vs_dec = (
            df[df["prediction"].isin(CONIFEROUS_SPECIES)].shape[0] / total * 100
            if CONIFEROUS_SPECIES else 0
        )
        class_rapid_growth = (
            df[df["prediction"].isin(RAPID_GROWTH_SPECIES)].shape[0] / total * 100
            if RAPID_GROWTH_SPECIES else 0
        )
        class_large_crown = (
            df[df["prediction"].isin(LARGE_CROWN_SPECIES)].shape[0] / total * 100
            if LARGE_CROWN_SPECIES else 0
        )

        # In_class_differ requires historical data, skipping for now
        in_class_differ = 0

        model_version = LATEST_MODEL_VERSION
  
        # --- Decision logic ---
        # Priority: critical > warning > moderate > ok
        status = "ok"

        if in_class_differ > 20:
            # Unexplained loss of class members — likely data problem or environmental change
            status = "critical"
        elif class_conf_min < 60:
            # Model is not confident enough in its predictions
            status = "warning"
        elif in_class_max > 50:
            # Majority of detected trees belong to a highly flammable species
            status = "warning"
        elif model_version != LATEST_MODEL_VERSION:
            # Running an outdated model — update recommended
            status = "warning"
        elif class_rapid_growth > 50:
            # Majority of detected trees are fast-growing species (informative)
            status = "moderate"
        elif class_large_crown > 50:
            # Majority of detected trees have large crowns (informative)
            status = "moderate"
        # else: all checks passed, status remains ok

        return OutputModel(model_status=status)