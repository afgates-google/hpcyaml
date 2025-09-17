# src/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yaml

# We don't need to import Depends anymore for this logic.
# We will import the client factory and classes directly.
from src.dependencies import get_gcp_client
from src.gcp_client import GcpClient
from src.validator import Validator
from src.cost_estimator import estimate_cost

app = FastAPI()

# Your CORS configuration is perfect. Do not change it.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ApiRequest(BaseModel):
    yaml_content: str
    region: str
    zone: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/validate")
def validate_yaml(request: ApiRequest): # We removed: gcp_client: GcpClient = Depends(...)
    """
    Validates a given YAML content against GCP resources.
    """
    try:
        blueprint = yaml.safe_load(request.yaml_content)
    except yaml.YAMLError as e:
        raise HTTPException(status_code=400, detail=f"Invalid YAML content: {e}")

    if not blueprint:
        raise HTTPException(status_code=400, detail="YAML content is empty or invalid.")

    project_id = blueprint.get("vars", {}).get("project_id")
    if not project_id:
        raise HTTPException(status_code=400, detail="Google Cloud project ID not found in YAML vars.")

    # --- THIS IS THE CORRECT LOGIC ---
    # We instantiate the client AFTER we have the project_id from the YAML.
    gcp_client = get_gcp_client(project_id=project_id)

    validator = Validator(gcp_client)
    is_valid = validator.validate_yaml_content(
        yaml_content=request.yaml_content,
        # It's safer to get the region/zone from the blueprint if they exist
        region=blueprint.get("vars", {}).get("region", request.region),
        zone=blueprint.get("vars", {}).get("zone", request.zone)
    )
    errors = validator.get_errors()

    return {"is_valid": is_valid, "errors": errors}


@app.post("/cost")
def get_cost(request: ApiRequest): # We removed: gcp_client: GcpClient = Depends(...)
    """
    Estimates the cost of a given YAML content.
    """
    try:
        blueprint = yaml.safe_load(request.yaml_content)
    except yaml.YAMLError as e:
        raise HTTPException(status_code=400, detail=f"Invalid YAML content: {e}")

    if not blueprint:
        raise HTTPException(status_code=400, detail="YAML content is empty or invalid.")

    project_id = blueprint.get("vars", {}).get("project_id")
    if not project_id:
        raise HTTPException(status_code=400, detail="Google Cloud project ID not found in YAML vars.")

    # --- THIS IS THE CORRECT LOGIC ---
    # We instantiate the client AFTER we have the project_id from the YAML.
    gcp_client = get_gcp_client(project_id=project_id)

    validator = Validator(gcp_client)
    extracted_resources = validator._extract_resources(blueprint)

    total_cost, cost_breakdown = estimate_cost(
        extracted_resources=extracted_resources,
        region=blueprint.get("vars", {}).get("region", request.region),
        zone=blueprint.get("vars", {}).get("zone", request.zone),
        gcp_client=gcp_client
    )

    return {"total_cost": total_cost, "cost_breakdown": cost_breakdown}