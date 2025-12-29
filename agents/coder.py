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

def coder_agent(state):
    print("\n[CODER] AGENT STARTED")

    llm = get_llm()
    # generate code from the architecture
    prompt = f"""Write Python code based on this architecture:

{state['architecture']}
"""
    response = llm.invoke([HumanMessage(content=prompt)])

    code = response.content
    print("GENERATED CODE:\n", code)
    # could add code formatting here but keeping it simple for now

    return {"code": code}
