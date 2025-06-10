from langgraph.graph import StateGraph, MessagesState
from dotenv import load_dotenv
import os
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from rich import print # laat prints mooi zien in de terminal

load_dotenv()

def get_azure_chat_openai(model = "o3-mini"):
    import os
    from langchain_openai import AzureChatOpenAI

    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    subscription_key = os.environ["AZURE_OPENAI_API_KEY"]
    api_version = os.environ["AZURE_API_VERSION"]

    return AzureChatOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=subscription_key,
        model=model,
        temperature=None
    )

tavily_key = os.environ["TAVILY_API_KEY"]

if __name__ == "__main__":
    o3_mini_chat = get_azure_chat_openai()
    # Create a message
    msg = HumanMessage(content="Hello world", name="Lance")
    # Message list
    messages = [msg]
    # Invoke the model with a list of messages
    response = o3_mini_chat.invoke(messages)
    # Print the response
    print(response.content)
    print("---------------------------------------------")
    print(response)

    print("Tavily---------------------------------------------")
    tavily_search = TavilySearchResults(max_results=3, api_key=tavily_key)
    search_docs = tavily_search.invoke("What is LangGraph?")
    print(search_docs)