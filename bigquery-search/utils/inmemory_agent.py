
import os
import asyncio
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm # For multi-model support
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types # For creating message Content/Parts

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

print("Libraries imported.")
# @title Define and Test GPT Agent

# Make sure 'get_weather' function from Step 1 is defined in your environment.
# Make sure 'call_agent_async' is defined from earlier.

# --- Agent using GPT-4o ---
MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash-exp"

# Note: Specific model names might change. Refer to LiteLLM/Provider documentation.
MODEL_GPT_4O = "openai/gpt-4o"
MODEL_CLAUDE_SONNET = "anthropic/claude-3-sonnet-20240229"

print("\nEnvironment configured.")
weather_agent_gpt = None # Initialize to None
runner_gpt = None      # Initialize runner to None


# @title Define the get_weather Tool
def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city (e.g., "New York", "London", "Tokyo").

    Returns:
        dict: A dictionary containing the weather information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'report' key with weather details.
              If 'error', includes an 'error_message' key.
    """
    # Best Practice: Log tool execution for easier debugging
    print(f"--- Tool: get_weather called for city: {city} ---")
    city_normalized = city.lower().replace(" ", "") # Basic input normalization

    # Mock weather data for simplicity
    mock_weather_db = {
        "newyork": {"status": "success", "report": "The weather in New York is sunny with a temperature of 25°C."},
        "london": {"status": "success", "report": "It's cloudy in London with a temperature of 15°C."},
        "tokyo": {"status": "success", "report": "Tokyo is experiencing light rain and a temperature of 18°C."},
    }

    # Best Practice: Handle potential errors gracefully within the tool
    if city_normalized in mock_weather_db:
        return mock_weather_db[city_normalized]
    else:
        return {"status": "error", "error_message": f"Sorry, I don't have weather information for '{city}'."}

async def agent(query: str):
    try:
        weather_agent_gpt = Agent(
            name="weather_agent_gpt",
            # Key change: Wrap the LiteLLM model identifier
            model=MODEL_GEMINI_2_0_FLASH, #LiteLlm(model=MODEL_GPT_4O),
            description="Provides weather information (using GPT-4o).",
            instruction="You are a helpful weather assistant. "
                        "Use the 'get_weather' tool for city weather requests. "
                        "Clearly present successful reports or polite error messages based on the tool's output status.",
            tools=[get_weather], # Re-use the same tool
        )
        print(f"Agent '{weather_agent_gpt.name}' created using model '{MODEL_GEMINI_2_0_FLASH}'.")

        # InMemorySessionService is simple, non-persistent storage for this tutorial.
        session_service_gpt = InMemorySessionService() # Create a dedicated service

        # Define constants for identifying the interaction context
        APP_NAME_GPT = "weather_tutorial_app_gpt" # Unique app name for this test
        USER_ID_GPT = "user_1_gpt"
        SESSION_ID_GPT = "session_001_gpt" # Using a fixed ID for simplicity

        # Create the specific session where the conversation will happen
        session_gpt = session_service_gpt.create_session(
            app_name=APP_NAME_GPT,
            user_id=USER_ID_GPT,
            session_id=SESSION_ID_GPT
        )
        print(f"Session created: App='{APP_NAME_GPT}', User='{USER_ID_GPT}', Session='{SESSION_ID_GPT}'")

        # Create a runner specific to this agent and its session service
        runner_gpt = Runner(
            agent=weather_agent_gpt,
            app_name=APP_NAME_GPT,       # Use the specific app name
            session_service=session_service_gpt # Use the specific session service
            )
        print(f"Runner created for agent '{runner_gpt.agent.name}'.")

        # Ensure call_agent_async uses the correct runner, user_id, session_id
        return await call_agent_async(query = query, #"What's the weather in Tokyo?",
                            runner=runner_gpt,
                            user_id=USER_ID_GPT,
                            session_id=SESSION_ID_GPT)

    except Exception as e:
        print(f"❌ Could not create or run GPT agent '{MODEL_GEMINI_2_0_FLASH}'. Check API Key and model name. Error: {e}")



async def call_agent_async(query: str,
                           runner,
                           user_id,
                           session_id):
  """Sends a query to the agent and prints the final response."""
  print(f"\n>>> User Query: {query}")

  # Prepare the user's message in ADK format
  content = types.Content(role='user', parts=[types.Part(text=query)])

  final_response_text = "Agent did not produce a final response." # Default

  # Key Concept: run_async executes the agent logic and yields Events.
  # We iterate through events to find the final answer.
  async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
      # You can uncomment the line below to see *all* events during execution
      # print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

      # Key Concept: is_final_response() marks the concluding message for the turn.
      if event.is_final_response():
          if event.content and event.content.parts:
             # Assuming text response in the first part
             final_response_text = event.content.parts[0].text
          elif event.actions and event.actions.escalate: # Handle potential errors/escalations
             final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
          # Add more checks here if needed (e.g., specific error codes)
          break # Stop processing events once the final response is found
  print(f"<<< Agent Response: {final_response_text}")
  return final_response_text

