# test_app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create a brand new FastAPI app instance
minimal_app = FastAPI()

# Add the most permissive CORS for testing
minimal_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@minimal_app.get("/hello")
def read_root():
    """A simple endpoint with no logic."""
    print("LOG: /hello endpoint was hit successfully!")
    return {"message": "Hello from the minimal test app"}
