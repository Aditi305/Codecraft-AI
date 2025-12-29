# Setup Guide

## Setting Up Your OpenRouter API Key

To use Codecraft AI, you need to set up your OpenRouter API key.

### Step 1: Get Your OpenRouter API Key

1. Go to [OpenRouter Platform](https://openrouter.ai/keys)
2. Sign in or create an account
3. Click "Create Key" or use an existing key
4. Copy your API key

### Step 2: Create a .env File

Create a file named `.env` in the project root directory (same folder as `requirements.txt`).

**On Windows:**
1. Open a text editor (Notepad, VS Code, etc.)
2. Add these lines:
   ```
   OPENROUTER_API_KEY=your_actual_api_key_here
   OPENROUTER_MODEL=openai/gpt-4o-mini
   ```
3. Replace `your_actual_api_key_here` with your actual OpenRouter API key
4. Optionally change the model (see available models below)
5. Save the file as `.env` (make sure it's exactly `.env`, not `.env.txt`)

**Example .env file content:**
```
OPENROUTER_API_KEY=sk-or-v1-abc123xyz789...
OPENROUTER_MODEL=openai/gpt-4o-mini
```

### Step 3: Available Models

OpenRouter supports many models. You can use any of these by setting `OPENROUTER_MODEL` in your `.env` file:

**OpenAI Models:**
- `openai/gpt-4o-mini` (default, cost-effective)
- `openai/gpt-4o`
- `openai/gpt-4-turbo`
- `openai/gpt-3.5-turbo`

**Other Popular Models:**
- `anthropic/claude-3.5-sonnet`
- `google/gemini-pro`
- `meta-llama/llama-3.1-70b-instruct`
- `mistralai/mistral-large`

See all available models at: https://openrouter.ai/models

### Step 4: Verify Setup

Run this command to check if your API key is loaded:
```bash
python -c "from config import get_openrouter_api_key; print('API Key loaded:', get_openrouter_api_key()[:10] + '...')"
```

### Alternative: Set Environment Variable Directly (Windows)

If you prefer not to use a .env file, you can set it in PowerShell:

**For current session:**
```powershell
$env:OPENROUTER_API_KEY="your_actual_api_key_here"
$env:OPENROUTER_MODEL="openai/gpt-4o-mini"
```

**Permanently (for your user):**
```powershell
[System.Environment]::SetEnvironmentVariable('OPENROUTER_API_KEY', 'your_actual_api_key_here', 'User')
[System.Environment]::SetEnvironmentVariable('OPENROUTER_MODEL', 'openai/gpt-4o-mini', 'User')
```

After setting it permanently, restart your terminal/IDE.

### Step 5: Add Credits (If Needed)

OpenRouter requires credits to use the API:

1. Go to [OpenRouter Credits](https://openrouter.ai/credits)
2. Add credits to your account
3. Check your usage at [OpenRouter Activity](https://openrouter.ai/activity)

### Troubleshooting

- **Error: "OPENROUTER_API_KEY not found"**
  - Make sure the `.env` file is in the project root
  - Check that the file is named exactly `.env` (not `.env.txt`)
  - Verify the format: `OPENROUTER_API_KEY=your_key` (no spaces around `=`)

- **Error: "Invalid API key"**
  - Verify your API key is correct
  - Make sure you copied the entire key
  - Check if your OpenRouter account has credits

- **Error: "Model not found"**
  - Verify the model name is correct
  - Check available models at https://openrouter.ai/models
  - Make sure the model format is correct (e.g., `openai/gpt-4o-mini`)

### Benefits of OpenRouter

- ✅ Access to multiple AI models from one API
- ✅ Competitive pricing
- ✅ Easy model switching
- ✅ No need for multiple API keys
- ✅ Unified interface
