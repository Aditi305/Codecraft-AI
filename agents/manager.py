from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from config import get_openrouter_api_key, get_openrouter_model

def get_llm():
    return ChatOpenAI(
        model=get_openrouter_model(),
        temperature=0,
        api_key=get_openrouter_api_key(),
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "https://github.com/your-repo",
            "X-Title": "Codecraft AI"
        }
    )

def manager_agent(state):
    print("\n[MANAGER] AGENT STARTED")

    llm = get_llm()
    # manager makes the final call
    response = llm.invoke([
        HumanMessage(content=f"""You are a software manager.

Review:
{state['review']}

Reply with ONLY one word:
- rewrite
- approve
""")
    ])

    decision = response.content.lower().strip()

    # parse the decision
    if "rewrite" in decision:
        final_decision = "rewrite"
    else:
        final_decision = "approve"  # default to approve

    print("FINAL DECISION:", final_decision)
    return {"decision": final_decision}
