# Stock Photo Search Agent - Masumi Network

This **Stock Photo Search Agent** is an AI-powered service that intelligently finds and curates stock photos from Pexels based on natural language prompts. Built with CrewAI and integrated with Masumi's decentralized payment solution.

[Follow this guide](https://docs.masumi.network/documentation/how-to-guides/agent-from-zero-to-hero)

**What it does:**

- Takes natural language descriptions of photo needs
- Intelligently searches Pexels API with optimized search terms
- Curates and selects the most relevant high-quality photos
- Returns 8-12 perfectly matched stock photos with full attribution

**Key benefits:**

- AI-powered search: Understands context and finds the perfect photos
- Simple setup: Just clone, configure, and deploy
- Integrated with Masumi for automated decentralized payments on Cardano
- Production-ready API built with FastAPI

---

## 🚀 Quick Start Commands

```bash
# Navigate to project
cd /Users/joshuakuski/Desktop/MacroLab/Masumi/StockPhotosagent

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
open .env  # Add your PEXELS_API_KEY and OPENAI_API_KEY

# Test locally (no payments, direct results)
python main.py

# OR run the API server (with Masumi payments)
python main.py api
```

**Local mode:** Direct results in terminal (no Masumi needed)  
**API mode:** Visit **http://localhost:8000/docs**

---

Follow these steps to quickly get your CrewAI agents live and monetized on Masumi.

### **1. Setup Environment**

Prerequisites:

- Python >= 3.10 and < 3.13
- pip (Python package manager)

Navigate to the project directory:

```bash
cd /Users/joshuakuski/Desktop/MacroLab/Masumi/StockPhotosagent
```

Create and activate virtual environment:

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### **2. Configure Your Environment Variables**

Copy `.env.example` to `.env` and fill with your own data:

```bash
cp .env.example .env

# Edit the .env file with your favorite editor
nano .env
# OR
open .env
```

Example `.env` configuration:

```ini
# Payment Service
PAYMENT_SERVICE_URL=http://localhost:3001/api/v1
PAYMENT_API_KEY=your_payment_key

# Agent Configuration
AGENT_IDENTIFIER=your_agent_identifier_from_registration
PAYMENT_AMOUNT=10000000
PAYMENT_UNIT=lovelace
SELLER_VKEY=your_selling_wallet_vkey

# Network
NETWORK=PREPROD

# OpenAI API
OPENAI_API_KEY=your_openai_api_key

# Pexels API (for stock photo search)
PEXELS_API_KEY=your_pexels_api_key
```

#### Get your API keys:

- **OpenAI API**: Get it from the [OpenAI Developer Portal](https://platform.openai.com/api-keys)
- **Pexels API**:
  1. Visit [Pexels API](https://www.pexels.com/api/)
  2. Click "Get Started" (it's free!)
  3. Create an account or sign in
  4. Your API key will be shown on your dashboard
  5. Free tier includes 200 requests/hour and 20,000/month

---

### **3. Understand the Stock Photo Agent**

The `crew_definition.py` file contains a `PhotoSearchCrew` with three specialized agents:

1. **Query Analyst**: Analyzes user prompts and extracts optimal search terms
2. **Photo Curator**: Searches Pexels and selects the most relevant photos
3. **Results Formatter**: Organizes photos with full attribution and download links

The agent workflow:

- User submits a natural language prompt (e.g., "cozy coffee shop atmosphere")
- Query Analyst creates 2-4 optimized search queries
- Photo Curator searches Pexels and selects top 8-12 photos
- Results Formatter presents photos with all necessary URLs and credits

#### Test your agent locally:

You can test the agent without Masumi payments by running it directly:

```bash
python main.py
```

This will:

- ✅ Run the agent locally without API or payment setup
- ✅ Use the test prompt: "modern coffee shop with cozy atmosphere and natural lighting"
- ✅ Display results directly in your terminal
- ✅ Take about 30-60 seconds to complete

To customize the test prompt, edit the `test_standalone()` function in `main.py`:

```python
input_data = {"prompt": "your custom prompt here"}
```

**No Masumi setup needed for local testing!** Just PEXELS_API_KEY and OPENAI_API_KEY.

---

### **4. Expose Your Agent via API**

Now we'll expose the agent via a FastAPI interface that follows the [MIP-003](https://github.com/masumi-network/masumi-improvement-proposals/blob/main/MIPs/MIP-003/MIP-003) standard.

Return `main.py` to its original state.

The API provides these endpoints:

- `GET /input_schema` - Returns input requirements
- `GET /availability` - Checks server status
- `POST /start_job` - Starts a new AI task
- `GET /status` - Checks job status
- `POST /provide_input` - Provides additional input

```
Temporary job storage warning: For simplicity, jobs are stored in memory (jobs = {}). In production, use a database like PostgreSQL and consider message queues for background processing.
```

#### Run the API server:

```python
python main.py api
```

Access the interactive API documentation at:
http://localhost:8000/docs

---

### 💳 **5. Install the Masumi Payment Service**

The Masumi Payment Service handles all blockchain payments for your agent.

Follow the [Installation Guide](https://docs.masumi.network/documentation/get-started/installation) to set up the payment service.

Once installed (locally), your payment service will be available at:

- Admin Dashboard: http://localhost:3001/admin
- API Documentation: http://localhost:3001/docs

If you used some other way of deployment, for example with Rialway, you have to find the URL there.

Verify it's running:

```bash
curl -X GET 'http://localhost:3001/api/v1/health/' -H 'accept: application/json'
```

You should receive:

```
{
  "status": "success",
  "data": {
    "status": "ok"
  }
}
```

---

### **6. Top Up Your Wallet with Test ADA**

Get free Test ADA from Cardano Faucet:

- Copy your Selling Wallet address from the Masumi Dashboard.
- Visit the [Cardano Faucet](https://docs.cardano.org/cardano-testnets/tools/faucet) or the [Masumi Dispencer](https://dispenser.masumi.network/).
- Request Test ADA (Preprod network).

---

### **7. Register Your Crew on Masumi**

Before accepting payments, register your agent on the Masumi Network.

1. Get your payment source information using [/payment-source/](https://docs.masumi.network/api-reference/payment-service/get-payment-source) endpoint, you will need `walletVkey` from the Selling Wallet (look for `"network": "PREPROD"`).:

2.Register your CrewAI agent via Masumi’s API using the [POST /registry](https://docs.masumi.network/api-reference/payment-service/post-registry) endpoint.

It will take a few minutes for the agnet to register, you can track it's state in the admin dashboard.

3. Once the agent is rerigstered, get your agent identifier [`GET /registry/`](https://docs.masumi.network/api-reference/payment-service/get-registry)

Note your `agentIdentifier` from the response and update it in your `.env` file and update`PAYMENT_API_KEY`

Create an PAYMENT_API key using [`GET /api-key/`](https://docs.masumi.network/api-reference/registry-service/get-api-key)

---

### **8. Test Your Monetized Agent**

Your agent is now ready to accept payments! Test the complete workflow:

Start a paid job:

```bash
curl -X POST "http://localhost:8000/start_job" \
-H "Content-Type: application/json" \
-d '{
    "identifier_from_purchaser": "<put HEX of even character>",
    "input_data": {"prompt": "modern tech startup office with diverse team"}
}'
```

This returns a `job_id`.

Check job status:

`curl -X GET "http://localhost:8000/status?job_id=your_job_id"`

Make the payment (from another agent or client):

```bash
curl -X POST 'http://localhost:3001/api/v1/purchase' \
  -H 'Content-Type: application/json' \
  -H 'token: purchaser_api_key' \
  -d '{
    "agent_identifier": "your_agent_identifier"
  }'
```

## Your agent will process the job and return results once payment is confirmed!

---

## **Important: Pexels Attribution Requirements**

When using photos from this agent, users must provide attribution:

1. **Include photographer credit**: Link to the photographer's Pexels profile
2. **Link back to Pexels**: Mention that photos are from Pexels
3. **Example attribution**: "Photos by [Photographer Name](profile-url) from [Pexels](https://www.pexels.com)"

The agent automatically includes all necessary attribution information in the results.

---

## **Production Deployment Notes**

**Next Steps for Production:**

1. Replace the in-memory job store (`jobs = {}`) with a persistent database (PostgreSQL, MongoDB, etc.)
2. Implement proper error handling and retry logic for API failures
3. Add rate limiting to prevent abuse
4. Consider caching popular searches to reduce API calls
5. Monitor Pexels API usage to stay within rate limits (200/hour, 20k/month free tier)

---

## **Useful Resources**

- [Pexels API Documentation](https://www.pexels.com/api/documentation/)
- [CrewAI Documentation](https://docs.crewai.com)
- [Masumi Documentation](https://docs.masumi.network)
- [FastAPI](https://fastapi.tiangolo.com)
- [Cardano Testnet Faucet](https://docs.cardano.org/cardano-testnets/tools/faucet)
# StockPhotoAgent
# StockPhotoAgent
