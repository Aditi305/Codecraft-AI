# Codecraft AI

A multi-agent AI system that generates code through a collaborative workflow using OpenRouter API. The system uses 5 specialized agents working together to design, implement, test, review, and approve code.

## Features

- **5-Agent Workflow**: Architect → Coder → Tester → Reviewer → Manager
- **Modern Web UI**: Interactive interface to test the API directly from browser
- **OpenRouter Integration**: Access to multiple AI models through unified API
- **RESTful API**: Clean API endpoints for integration
- **Full-Width Code Display**: Optimized for viewing generated code

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```
OPENROUTER_API_KEY=sk-or-v1-your-key-here
OPENROUTER_MODEL=openai/gpt-4o-mini
```

Get your API key from: [OpenRouter Settings](https://openrouter.ai/settings/keys)

### 3. Run the Server

**Option 1: Using the run script**
```bash
python run_server.py
```

**Option 2: Using uvicorn directly**
```bash
uvicorn api.main:app --reload
```

### 4. Access the Application

- **Web UI**: http://127.0.0.1:8000/
- **API Docs**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## Agent Workflow

The system uses a sequential workflow with conditional looping:

1. **Architect** - Designs high-level architecture and system structure
2. **Coder** - Implements the code based on architecture
3. **Tester** - Creates comprehensive test cases
4. **Reviewer** - Reviews code quality and test coverage
5. **Manager** - Makes final decision (approve/rewrite)

If the manager decides to rewrite, the process loops back to the coder for improvements.

## API Endpoints

### Generate Code
```
POST /api/v1/generate
```

**Request:**
```json
{
  "task": "Create a Python function to calculate fibonacci numbers"
}
```

**Response:**
```json
{
  "architecture": "...",
  "code": "...",
  "tests": "...",
  "review": "...",
  "final_decision": "approve"
}
```

### Health Check
```
GET /health
```

### Status
```
GET /status
```

## Project Structure

```
.
├── api/
│   ├── main.py          # FastAPI application with web UI
│   └── routes.py        # API routes
├── agents/
│   ├── architect.py     # Architect agent
│   ├── coder.py         # Coder agent
│   ├── tester.py        # Tester agent
│   ├── reviewer.py      # Reviewer agent
│   └── manager.py       # Manager agent
├── orchestration/
│   ├── graph.py         # LangGraph workflow definition
│   └── state.py         # State definition
├── config.py            # Configuration and env loading
├── requirements.txt     # Python dependencies
├── run_server.py        # Server startup script
└── .env                 # Environment variables (create this)
```

## Configuration

### OpenRouter API Key

1. Sign up at [OpenRouter](https://openrouter.ai/)
2. Get your API key from [Settings](https://openrouter.ai/settings/keys)
3. Add to `.env` file: `OPENROUTER_API_KEY=sk-or-v1-your-key-here`

### Available Models

You can change the model by updating `OPENROUTER_MODEL` in your `.env` file:

- `openai/gpt-4o-mini` (default, cost-effective)
- `openai/gpt-4o`
- `openai/gpt-4-turbo`
- `anthropic/claude-3.5-sonnet`
- `google/gemini-pro`

See all models: https://openrouter.ai/models

### Credits

Make sure you have credits in your OpenRouter account:
- Check credits: https://openrouter.ai/credits
- Add credits if needed

## Usage Examples

### Using the Web UI

1. Visit http://127.0.0.1:8000/
2. Enter your task description (e.g., "Create a calculator class")
3. Click "Generate Code"
4. View results: Architecture, Code, Tests, Review, and Final Decision

### Using the API

**Python:**
```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/api/v1/generate",
    json={"task": "Create a Python function to calculate fibonacci numbers"}
)
print(response.json())
```

**cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{"task": "Create a Python function to calculate fibonacci numbers"}'
```

## Troubleshooting

### API Key Issues

**Error: "OPENROUTER_API_KEY not found"**
- Make sure `.env` file exists in project root
- Verify it contains: `OPENROUTER_API_KEY=sk-or-v1-...`
- Restart the server after updating `.env`

**Error: "API Key Issue"**
- Verify your key is active at https://openrouter.ai/settings/keys
- Check you have credits at https://openrouter.ai/credits
- Make sure you're using `OPENROUTER_API_KEY` (not `OPENAI_API_KEY`)

### Quota Errors

**Error: "API Quota Exceeded"**
- Add credits to your OpenRouter account
- Check usage at https://openrouter.ai/activity
- Wait for quota reset or upgrade plan

### Server Issues

**Error: "Attribute api not found"**
- Use correct command: `uvicorn api.main:app --reload`
- Note: Use `app` not `api` at the end

## Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `langgraph` - Agent orchestration
- `langchain-openai` - LLM integration
- `langchain-core` - Core LangChain components
- `pydantic` - Data validation
- `python-dotenv` - Environment variable loading

## Development

### Running in Development Mode

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Project Architecture

The system uses LangGraph to orchestrate the agent workflow:
- Each agent is a node in the graph
- State is passed between agents
- Conditional edges handle the rewrite loop
- See `orchestration/graph.py` for workflow definition

## License

This project is open source and available for use.

## Support

- OpenRouter Docs: https://openrouter.ai/docs
- OpenRouter Models: https://openrouter.ai/models
- OpenRouter Credits: https://openrouter.ai/credits
