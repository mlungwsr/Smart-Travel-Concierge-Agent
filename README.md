# 🌍 Smart Travel Concierge Agent

**Build Your First AI Agent on AWS: A Hands-On Demo with Amazon Bedrock AgentCore**

> Presented at the AI Festival Summit — June 10-11, 2026

## What Is This?

A production-ready **Smart Travel Concierge Agent** built with [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/) and [Strands Agents](https://strandsagents.com). This demo shows how to go from zero to a deployed AI agent in under 40 minutes.

The agent can:
- ✈️ Search flights between cities worldwide
- 🌤️ Check weather and forecasts at any destination
- 📊 Generate price comparison charts (Code Interpreter)
- 🧠 Remember user preferences across conversations (Memory)
- 🔍 Full observability with OpenTelemetry tracing

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                Amazon Bedrock AgentCore              │
│  ┌───────────┐  ┌──────────┐  ┌─────────────────┐  │
│  │  Runtime   │  │  Memory  │  │  Observability  │  │
│  └─────┬─────┘  └────┬─────┘  └────────┬────────┘  │
│        │              │                  │           │
│  ┌─────┴──────────────┴──────────────────┴───────┐  │
│  │          Strands Agent (Claude Sonnet)         │  │
│  └─────┬──────────────┬──────────────────┬───────┘  │
│        │              │                  │           │
│  ┌─────┴─────┐ ┌─────┴──────┐ ┌────────┴────────┐  │
│  │  Gateway   │ │  Gateway   │ │ Code Interpreter│  │
│  │  (Flights) │ │  (Weather) │ │   (Built-in)    │  │
│  └─────┬─────┘ └─────┬──────┘ └─────────────────┘  │
└────────┼──────────────┼─────────────────────────────┘
         │              │
   ┌─────┴─────┐ ┌─────┴──────┐
   │  Lambda:   │ │  Lambda:   │
   │  Flight    │ │  Weather   │
   │  Search    │ │  Lookup    │
   └───────────┘ └────────────┘
```

## AgentCore Features Demonstrated

| Feature | Description |
|---------|-------------|
| **AgentCore CLI** | Create, develop, and deploy agents |
| **Runtime** | Serverless, auto-scaling agent hosting |
| **Gateway** | Convert Lambda functions into MCP-compatible tools |
| **Code Interpreter** | Built-in Python execution for charts and calculations |
| **Memory** | Managed user preference storage across sessions |
| **Observability** | OpenTelemetry tracing and monitoring |

## Project Structure

```
Smart-Travel-Concierge-Agent/
├── agent/
│   └── agent.py              # Main agent code (Strands Agents)
├── lambda/
│   ├── flight-search/
│   │   └── index.py          # Flight search Lambda function
│   └── weather-lookup/
│       └── index.py          # Weather lookup Lambda function
├── infrastructure/
│   └── template.yaml         # CloudFormation template for pre-deployed resources
├── notebook/
│   └── Smart_Travel_Concierge_Demo.ipynb  # Demo notebook
├── slides/
│   └── outline.md            # Slide deck outline
├── requirements.txt
├── .gitignore
└── README.md
```

## Prerequisites

- AWS Account with credentials configured (`aws configure`)
- [Node.js 20.x](https://nodejs.org/) or later
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (for Python agent)
- Model Access: Anthropic Claude Sonnet enabled in [Amazon Bedrock console](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access-modify.html)
- AWS Permissions: `BedrockAgentCoreFullAccess` + `AmazonBedrockFullAccess`

## Quick Start

### 1. Deploy Pre-Built Resources

```bash
aws cloudformation deploy \
    --template-file infrastructure/template.yaml \
    --stack-name travel-concierge-prereqs \
    --capabilities CAPABILITY_NAMED_IAM \
    --region us-west-2
```

### 2. Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the Agent Locally

```bash
cd agent
python agent.py
```

### 4. Run the Demo Notebook

```bash
python -m ipykernel install --user --name=travel-demo --display-name="Python (Travel Demo)"
jupyter notebook notebook/Smart_Travel_Concierge_Demo.ipynb
```

### 5. Deploy with AgentCore CLI

```bash
npm install -g @aws/agentcore
agentcore create   # or use the existing agent/ directory
agentcore dev      # local development
agentcore deploy   # deploy to production
```

### 6. Create the AgentCore Gateway (Console)

The Gateway exposes your Lambda functions as MCP-compatible tools that the deployed agent can discover automatically.

1. Navigate to **Amazon Bedrock → AgentCore → Gateway → Create gateway**
2. **Name:** `travel-concierge-gateway`, **Inbound Auth:** `None`
3. **Add Target — Flight Search:**
   - Type: `Lambda function ARN`
   - ARN: `travel-flight-search` Lambda ARN
   - Inline schema:
   ```json
   [
     {
       "name": "search_flights",
       "description": "Search for flights between two cities.",
       "inputSchema": {
         "type": "object",
         "properties": {
           "origin": { "type": "string", "description": "Departure city" },
           "destination": { "type": "string", "description": "Arrival city" },
           "date": { "type": "string", "description": "YYYY-MM-DD (empty=today)" },
           "num_results": { "type": "number", "description": "Results count" }
         },
         "required": ["origin", "destination"]
       }
     }
   ]
   ```
4. **Add Target — Weather Lookup:**
   - Type: `Lambda function ARN`
   - ARN: `travel-weather-lookup` Lambda ARN
   - Inline schema:
   ```json
   [
     {
       "name": "check_weather",
       "description": "Check current weather and 5-day forecast for a city.",
       "inputSchema": {
         "type": "object",
         "properties": {
           "city": { "type": "string", "description": "City name" }
         },
         "required": ["city"]
       }
     }
   ]
   ```
5. **Review & Create**

### 7. Link Gateway and Deploy

```bash
cd /tmp/travelagent
agentcore add gateway --name travel-concierge-gateway
agentcore deploy
```

> **Note:** During local development (`agentcore dev`), the agent calls Lambda directly via boto3. After deployment, the agent discovers tools via Gateway using MCP — same agent code, different tool delivery.

## Cleanup

```bash
aws cloudformation delete-stack \
    --stack-name travel-concierge-prereqs \
    --region us-west-2
```

## Resources

- [Amazon Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/)
- [AgentCore Samples](https://github.com/awslabs/agentcore-samples)
- [AgentCore CLI](https://github.com/aws/agentcore-cli)
- [Strands Agents](https://strandsagents.com)
- [Getting Started Workshop](https://catalog.us-east-1.prod.workshops.aws/workshops/850fcd5c-fd1f-48d7-932c-ad9babede979/en-US)

## License

This project is provided for educational and demonstration purposes.
