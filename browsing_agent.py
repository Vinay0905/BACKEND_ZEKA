from browser_use import Agent, ChatOpenAI, sandbox, Browser
from dotenv import load_dotenv
import asyncio
import json
import os

load_dotenv()


from e2b_desktop import Sandbox

# Create a new desktop sandbox


async def main():
    desktop = Sandbox.create()

    # Launch an application
    desktop.launch('google-chrome')  # or vscode, firefox, etc.

    # Wait 10s for the application to open
    desktop.wait(10000)
    chrome_url = desktop.get_chrome_endpoint()
    print(f"Chrome URL: {chrome_url}")

    # Stream the application's window
    # Note: There can be only one stream at a time
    # You need to stop the current stream before streaming another application
    desktop.stream.start(
        window_id=desktop.get_current_window_id(), # if not provided the whole desktop will be streamed
        require_auth=True
    )

    # Get the stream auth key
    auth_key = desktop.stream.get_auth_key()

    # Print the stream URL
    print('Stream URL:', desktop.stream.get_url(auth_key=auth_key))

    # Kill the sandbox after the tasks are finished
    # desktop.kill()
    if not os.path.exists("tests.json"):
        print("tests.json not found!")
        return
    
    try:
        with open("tests.json", "r", encoding='utf-8') as f:
            tests = json.load(f)
        print(f"Loaded {len(tests)} tests")
    except Exception as e:
        print(f"Error loading tests: {e}")
        return
    
    for i, test in enumerate(tests):
        # Extract task description as STRING for browser-use Agent
        task_description = test.get("description", "Navigate and test website functionality")
        task_prompt = f"""
Test Case: {test.get('title', 'Unknown')}
Type: {test.get('type', 'positive').upper()}
Expected: {test.get('expected_result', 'Success')}
Description: {task_description}

Execute these steps:
{chr(10).join([f"- {step}" for step in test.get('steps', [])])}

Report PASS/FAIL with screenshots.
"""
        
        print(f"Running test {i+1}/{len(tests)}: {test.get('title', 'Unknown')}")
        
        llm = ChatOpenAI(model="gpt-4.1-mini")
        agent = Agent(task=task_prompt, llm=llm) 
        await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
