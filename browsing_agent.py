from browser_use import Agent, ChatOpenAI
from dotenv import load_dotenv
import asyncio
from scrape import generate_test_cases, ExtractedWebsiteData, scrape_website, extract_website_intelligence
import json

load_dotenv()

async def main():
    with open("tests.json", "r") as f:
        tests = json.load(f)
    for i in range(len(tests)):
        task = tests[i]
        llm = ChatOpenAI(model="gpt-4.1-mini")
        agent = Agent(task=task, llm=llm)
        await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
