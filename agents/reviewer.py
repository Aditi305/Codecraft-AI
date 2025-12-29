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

def reviewer_agent(state):
    print("\n[REVIEWER] AGENT STARTED")

    llm = get_llm()
    # review both code and tests
    response = llm.invoke([
        HumanMessage(content=f"""Review this code and tests. 
Say if changes are required or not.

Code:
{state['code']}

Tests:
{state['tests']}
""")
    ])

    review = response.content
    print("REVIEW FEEDBACK:\n", review)

    return {"review": review}
