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

def tester_agent(state):
    print("\n[TESTER] AGENT STARTED")

    llm = get_llm()
    # create test cases for the generated code
    response = llm.invoke([
        HumanMessage(content=f"""Write pytest test cases for the following code:

{state['code']}
""")
    ])

    tests = response.content
    print("GENERATED TESTS:\n", tests)

    return {"tests": tests}
