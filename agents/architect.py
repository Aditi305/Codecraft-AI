from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from config import get_openrouter_api_key, get_openrouter_model

def get_llm():
    # using openrouter instead of direct openai
    return ChatOpenAI(
        model=get_openrouter_model(),
        temperature=0,  # keep it deterministic
        api_key=get_openrouter_api_key(),
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "https://github.com/your-repo",
            "X-Title": "Codecraft AI"
        }
    )

def architect_agent(state):
    print("\n[ARCHITECT] AGENT STARTED")
    print("Task:", state["task"])

    llm = get_llm()
    # ask it to design the architecture
    response = llm.invoke([
        HumanMessage(content=f"Design a high-level architecture for: {state['task']}")
    ])

    architecture = response.content
    print("ARCHITECT OUTPUT:\n", architecture)

    return {"architecture": architecture}
