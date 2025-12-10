import os
import uvicorn
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field, field_validator
from masumi.config import Config
from masumi.payment import Payment, Amount
from crew_definition import PhotoSearchCrew
from logging_config import setup_logging

# Configure logging
logger = setup_logging()

# Load environment variables
load_dotenv(override=True)

# Retrieve API Keys and URLs
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PAYMENT_SERVICE_URL = os.getenv("PAYMENT_SERVICE_URL")
PAYMENT_API_KEY = os.getenv("PAYMENT_API_KEY")
NETWORK = os.getenv("NETWORK")

logger.info("Starting application with configuration:")
logger.info(f"PAYMENT_SERVICE_URL: {PAYMENT_SERVICE_URL}")

# Initialize FastAPI
app = FastAPI(
    title="Stock Photo Search Agent - Masumi API",
    description="AI-powered stock photo search agent using Pexels API with Masumi payment integration",
    version="1.0.0"
)

# ─────────────────────────────────────────────────────────────────────────────
# Temporary in-memory job store (DO NOT USE IN PRODUCTION)
# ─────────────────────────────────────────────────────────────────────────────
jobs = {}
payment_instances = {}

# ─────────────────────────────────────────────────────────────────────────────
# Initialize Masumi Payment Config
# ─────────────────────────────────────────────────────────────────────────────
config = Config(
    payment_service_url=PAYMENT_SERVICE_URL,
    payment_api_key=PAYMENT_API_KEY
)

# ─────────────────────────────────────────────────────────────────────────────
# Pydantic Models
# ─────────────────────────────────────────────────────────────────────────────
class StartJobRequest(BaseModel):
    identifier_from_purchaser: str = Field(..., min_length=1, description="Unique identifier from the purchaser")
    input_data: dict[str, str] = Field(..., description="Input data containing the photo search prompt")
    
    @field_validator('input_data')
    @classmethod
    def validate_input_data(cls, v):
        if not v or 'prompt' not in v:
            raise ValueError('input_data must contain a "prompt" field with the photo search query')
        if not v['prompt'] or len(v['prompt'].strip()) < 5:
            raise ValueError('prompt field must contain at least 5 characters')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "identifier_from_purchaser": "example_purchaser_123",
                "input_data": {
                    "prompt": "modern tech startup office with diverse team collaborating"
                }
            }
        }

class ProvideInputRequest(BaseModel):
    job_id: str

# ─────────────────────────────────────────────────────────────────────────────
# CrewAI Task Execution
# ─────────────────────────────────────────────────────────────────────────────
async def execute_crew_task(input_data: dict) -> str:
    """ Execute a CrewAI task with Photo Search Agents """
    prompt = input_data.get("prompt", "")
    logger.info(f"Starting photo search task with prompt: {prompt[:100]}...")
    
    try:
        logger.info("Initializing Photo Search Crew...")
        crew = PhotoSearchCrew(logger=logger)
        logger.info("Photo Search Crew initialized successfully")
        
        logger.info("Starting crew execution...")
        logger.info(f"LLM model being used: {crew.llm.model if hasattr(crew.llm, 'model') else 'Unknown'}")
        logger.info(f"OpenAI API Key present: {bool(os.getenv('OPENAI_API_KEY'))}")
        
        result = crew.crew.kickoff(inputs={"prompt": prompt})
        logger.info("Photo search task completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error during crew execution: {str(e)}", exc_info=True)
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"OpenAI API Key configured: {bool(os.getenv('OPENAI_API_KEY'))}")
        if hasattr(e, 'response'):
            logger.error(f"API Response: {e.response}")
        raise

# ─────────────────────────────────────────────────────────────────────────────
# 1) Start Job (MIP-003: /start_job)
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/start_job")
async def start_job(data: StartJobRequest):
    """ Initiates a job and creates a payment request """
    print(f"Received data: {data}")
    print(f"Received data.input_data: {data.input_data}")
    try:
        job_id = str(uuid.uuid4())
        agent_identifier = os.getenv("AGENT_IDENTIFIER")
        
        # Log the input prompt (truncate if too long)
        input_prompt = data.input_data.get("prompt", "")
        truncated_input = input_prompt[:100] + "..." if len(input_prompt) > 100 else input_prompt
        logger.info(f"Received photo search request: '{truncated_input}'")
        logger.info(f"Starting job {job_id} with agent {agent_identifier}")

        # Define payment amounts
        payment_amount = os.getenv("PAYMENT_AMOUNT", "10000000")  # Default 10 ADA
        payment_unit = os.getenv("PAYMENT_UNIT", "lovelace") # Default lovelace

        amounts = [Amount(amount=payment_amount, unit=payment_unit)]
        logger.info(f"Using payment amount: {payment_amount} {payment_unit}")
        
        # Create a payment request using Masumi
        payment = Payment(
            agent_identifier=agent_identifier,
            amounts=amounts,
            config=config,
            identifier_from_purchaser=data.identifier_from_purchaser,
            input_data=data.input_data,
            network=NETWORK
        )
        
        logger.info("Creating payment request...")
        payment_request = await payment.create_payment_request()
        blockchain_identifier = payment_request["data"]["blockchainIdentifier"]
        payment.payment_ids.add(blockchain_identifier)
        logger.info(f"Created payment request with blockchain identifier: {blockchain_identifier}")

        # Store job info (Awaiting payment)
        jobs[job_id] = {
            "status": "awaiting_payment",
            "payment_status": "pending",
            "blockchain_identifier": blockchain_identifier,
            "input_data": data.input_data,
            "result": None,
            "identifier_from_purchaser": data.identifier_from_purchaser
        }

        async def payment_callback(blockchain_identifier: str):
            await handle_payment_status(job_id, blockchain_identifier)

        # Start monitoring the payment status
        payment_instances[job_id] = payment
        logger.info(f"Starting payment status monitoring for job {job_id}")
        await payment.start_status_monitoring(payment_callback)

        # Return the response in the required format
        return {
            "status": "success",
            "job_id": job_id,
            "blockchainIdentifier": blockchain_identifier,
            "submitResultTime": payment_request["data"]["submitResultTime"],
            "unlockTime": payment_request["data"]["unlockTime"],
            "externalDisputeUnlockTime": payment_request["data"]["externalDisputeUnlockTime"],
            "agentIdentifier": agent_identifier,
            "sellerVKey": os.getenv("SELLER_VKEY"),
            "identifierFromPurchaser": data.identifier_from_purchaser,
            "amounts": amounts,
            "input_hash": payment.input_hash,
            "payByTime": payment_request["data"]["payByTime"],
        }
    except ValueError as e:
        logger.error(f"Validation error in request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail=f"Validation error: {str(e)}"
        )
    except KeyError as e:
        logger.error(f"Missing required field in request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail="Bad Request: Missing required field in request data."
        )
    except Exception as e:
        logger.error(f"Error in start_job: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error occurred while processing the request."
        )

# ─────────────────────────────────────────────────────────────────────────────
# 2) Process Payment and Execute AI Task
# ─────────────────────────────────────────────────────────────────────────────
async def handle_payment_status(job_id: str, payment_id: str) -> None:
    """ Executes CrewAI task after payment confirmation """
    try:
        logger.info(f"Payment {payment_id} completed for job {job_id}, executing task...")
        
        # Update job status to running
        jobs[job_id]["status"] = "running"
        logger.info(f"Input data: {jobs[job_id]["input_data"]}")

        # Execute the AI task
        result = await execute_crew_task(jobs[job_id]["input_data"])
        logger.info(f"Crew task completed for job {job_id}")
        
        # Convert result to string for payment completion
        # Check if result has .raw attribute (CrewOutput), otherwise convert to string
        result_string = result.raw if hasattr(result, "raw") else str(result)
        
        # Mark payment as completed on Masumi
        await payment_instances[job_id].complete_payment(payment_id, result_string)
        logger.info(f"Payment completed for job {job_id}")

        # Update job status
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["payment_status"] = "completed"
        jobs[job_id]["result"] = result

        # Stop monitoring payment status
        if job_id in payment_instances:
            payment_instances[job_id].stop_status_monitoring()
            del payment_instances[job_id]
    except Exception as e:
        logger.error(f"Error processing payment {payment_id} for job {job_id}: {str(e)}", exc_info=True)
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        
        # Still stop monitoring to prevent repeated failures
        if job_id in payment_instances:
            payment_instances[job_id].stop_status_monitoring()
            del payment_instances[job_id]

# ─────────────────────────────────────────────────────────────────────────────
# 3) Check Job and Payment Status (MIP-003: /status)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/status")
async def get_status(job_id: str):
    """ Retrieves the current status of a specific job """
    logger.info(f"Checking status for job {job_id}")
    if job_id not in jobs:
        logger.warning(f"Job {job_id} not found")
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs[job_id]

    # Check latest payment status if payment instance exists
    if job_id in payment_instances:
        try:
            status = await payment_instances[job_id].check_payment_status()
            job["payment_status"] = status.get("data", {}).get("status")
            logger.info(f"Updated payment status for job {job_id}: {job['payment_status']}")
        except ValueError as e:
            logger.warning(f"Error checking payment status: {str(e)}")
            job["payment_status"] = "unknown"
        except Exception as e:
            logger.error(f"Error checking payment status: {str(e)}", exc_info=True)
            job["payment_status"] = "error"


    result_data = job.get("result")
    result = result_data.raw if result_data and hasattr(result_data, "raw") else None

    return {
        "job_id": job_id,
        "status": job["status"],
        "payment_status": job["payment_status"],
        "result": result
    }

# ─────────────────────────────────────────────────────────────────────────────
# 4) Check Server Availability (MIP-003: /availability)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/availability")
async def check_availability():
    """ Checks if the server is operational """
    agent_identifier = os.getenv("AGENT_IDENTIFIER")
    
    return {
        "status": "available", 
        "type": "masumi-agent", 
        "agent_type": "stock-photo-search",
        "agentIdentifier": agent_identifier,
        "version": "1.0.0",
        "message": "Stock Photo Search Agent operational and ready to process photo search queries."
    }

# ─────────────────────────────────────────────────────────────────────────────
# 5) Retrieve Input Schema (MIP-003: /input_schema)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/input_schema")
async def input_schema():
    """
    Returns the expected input schema for the /start_job endpoint.
    Fulfills MIP-003 /input_schema endpoint.
    """
    return {
        "input_data": [
            {
                "id": "prompt",
                "type": "string",
                "name": "Photo Search Prompt",
                "required": True,
                "data": {
                    "description": "Describe the type of stock photos you need for your project. Be specific about mood, style, subject matter, and context.",
                    "placeholder": "e.g., 'modern office space with natural lighting' or 'outdoor adventure hiking'",
                    "examples": [
                        "modern tech startup office with diverse team collaborating",
                        "cozy coffee shop with warm atmosphere and natural lighting",
                        "outdoor adventure hiking mountain trail",
                        "minimalist workspace with plants and natural light"
                    ]
                }
            }
        ]
    }

# ─────────────────────────────────────────────────────────────────────────────
# 6) Agent Metadata (Required for Sokosumi)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/metadata")
async def get_agent_metadata():
    """
    Returns agent metadata for Sokosumi marketplace listing.
    """
    agent_identifier = os.getenv("AGENT_IDENTIFIER")
    payment_amount = os.getenv("PAYMENT_AMOUNT", "10000000")
    payment_unit = os.getenv("PAYMENT_UNIT", "lovelace")
    
    return {
        "agentIdentifier": agent_identifier,
        "name": "Stock Photo Search Agent",
        "description": "AI-powered agent that intelligently searches and curates the top 5 highest-quality stock photos from Pexels. Get perfectly matched photos for your projects with markdown-formatted links, full attribution, multiple size options, and professional curation.",
        "version": "1.0.0",
        "category": "Media & Design",
        "tags": ["stock-photos", "pexels", "image-search", "design", "photography", "media"],
        "pricing": {
            "amount": payment_amount,
            "unit": payment_unit,
            "currency": "ADA"
        },
        "capabilities": [
            "Intelligent photo search using natural language",
            "Curated selection of top 5 highest-quality photos",
            "Original high-resolution photo downloads",
            "Full photographer attribution and Pexels links",
            "Optimized search query generation",
            "Markdown-formatted links for easy integration"
        ],
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Natural language description of the photos you need",
                    "examples": [
                        "modern coffee shop with cozy atmosphere",
                        "outdoor adventure hiking mountain",
                        "tech startup office with diverse team"
                    ]
                }
            },
            "required": ["prompt"]
        },
        "outputFormat": "Markdown-formatted list of 5 curated photos with Pexels page links, original photo download links, photographer info, and attribution",
        "averageProcessingTime": "30-60 seconds",
        "supportedNetworks": ["PREPROD", "MAINNET"],
        "contact": {
            "website": "https://docs.masumi.network",
            "support": "https://docs.masumi.network/documentation"
        }
    }

# ─────────────────────────────────────────────────────────────────────────────
# 7) Health Check
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/health")
async def health():
    """
    Returns the health of the server.
    """
    return {
        "status": "healthy"
    }

# ─────────────────────────────────────────────────────────────────────────────
# Main Logic if Called as a Script
# ─────────────────────────────────────────────────────────────────────────────
def test_standalone():
    """
    Standalone test function for Stock Photo Search Agent
    Usage: python main.py
    """
    print("\n" + "="*80)
    print("🧪 Stock Photo Search Agent - Standalone Test")
    print("="*80 + "\n")
    
    # Example prompts you can test with
    input_data = {"prompt": "modern coffee shop with cozy atmosphere and natural lighting"}
    
    print("🔍 Searching for: " + input_data["prompt"])
    print("\n" + "⏳ This will take 30-60 seconds as the AI agents work...\n")
    
    crew = PhotoSearchCrew(logger=logger)
    result = crew.crew.kickoff(inputs=input_data)
    
    print("\n" + "="*80)
    print("📸 STOCK PHOTO SEARCH RESULTS:")
    print("="*80)
    print(result.raw if hasattr(result, 'raw') else result)
    print("="*80 + "\n")

if __name__ == "__main__":
    import sys
    
    # Check if running in production (Railway sets PORT environment variable)
    if os.getenv("PORT") or (len(sys.argv) > 1 and sys.argv[1] == "api"):
        print("\n" + "="*80)
        print("🚀 Starting Stock Photo Search Agent API Server")
        print("="*80)
        print("\n📡 API will be available at:")
        print("   • API Docs: http://localhost:8000/docs")
        print("   • Redoc: http://localhost:8000/redoc")
        print("   • Health: http://localhost:8000/health")
        print("   • Availability: http://localhost:8000/availability")
        print("\n" + "="*80 + "\n")
        
        # Use PORT from environment if available (Railway), otherwise default to 8000
        port = int(os.getenv("PORT", 8000))
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        test_standalone()
