import google.generativeai as genai
import re

# Initialize game state
game_state = {
    "progress": [],
    "outcome": None,
    "hireability": 50
}

maxSteps = 10

def generate_story_step(current_state):
    # Generate the next story step based on the current game state
    # prompt = f'''
    #   Recent choices: {current_state["progress"]}.
    #   This is an interactive story set in the world of Suits, where the player takes on the role of Mike Ross navigating his interview at Pearson Hardman.
    #   The goal is to reach one of two possible outcomes: getting hired or getting rejected. Adapt the game to end after {maxSteps} steps. 
    #   Narrate the next part of the story based on the current state, then present three distinct and creative choices for the player.
    #   The story and choices should be written in simple vocabulary and concise
      
    #   The entire response should be a json in the following format 

    # '''
    
    prompt = """
    You are narrating an interactive story set in the world of Suits, where the player takes on the role of Mike Ross navigating his interview at Pearson Hardman. The goal is to determine the player's "hireability," starting at 50, which changes based on their choices.

    - Provide a short narration of the next story step based on the player's actions so far.
    - Present exactly three distinct choices the player can make. Each choice should subtly influence the hireability score.
    - Return the result as a JSON object in this format:

    {
      "story": "Narrate the next part of the story.",
      "choices": [
        {
          "text": "Choice A in human words.",
          "effect": "+5"
        },
        {
          "text": "Choice B in human words.",
          "effect": "-10"
        },
        {
          "text": "Choice C in human words.",
          "effect": "0"
        }
      ]
    }

    - Ensure "effect" reflects the impact each choice has on hireability, ranging from -15 to +15.
    - Keep the tone engaging, and align the narrative with Suits' high-stakes legal drama.
    - Do NOT add extra text — only output the JSON object.
    """
    
    response = model.generate_content(prompt)
    return response.text.strip()

# Gemini API Key (replace 'your-api-key' with your actual key)
genai.configure(api_key='AIzaSyCzO8JqOHfdcm8xcKecBA1NpIAj2FsA0V8')
model = genai.GenerativeModel('gemini-1.5-flash')

# Game Loop
currentStep = ""
useCurrentStep = False
while game_state["outcome"] is None:
    ai_response = generate_story_step(game_state) if not useCurrentStep else currentStep
    useCurrentStep = False
    print(ai_response)
    # currentStep = step

    # # get the last line of the message
    # resultReached = step.split("\n")[-1] 

    # # Print the narator message and the next options
    # print(step)

    # # Simulated choice input (replace with input() for real interaction)
    # choice = input("Choose: ").strip()

    # # Map numbers to letters
    # choice_map = {"1": "A", "2": "B", "3": "C"}
    # trait_map = { "A": "confidence", "B": "honesty", "C": "creativity" }
    # mapped_choice = choice_map.get(choice.strip(), choice.upper())

    # if len(choice) == 1:
    #   chosenOption = A if mapped_choice == "A" else B if mapped_choice == "B" else C if mapped_choice == "C" else None
    #   print("Chosen option:", chosenOption)

    #   if chosenOption is not None:
    #     classify = trait_map.get(mapped_choice)
    #   else:
    #     print("Invalid choice. Please try again.")
    #     useCurrentStep = True
    #     continue
    # else:
    #   classify = classify_user_response(choice)

    # print("Classifed As: ", classify)

    # if classify in game_state["traits"]:
    #     game_state["traits"][classify] += 1
    #     game_state["progress"].append(classify)
    # else:
    #     print("Invalid choice. Please try again.")
    #     useCurrentStep = True
    #     continue


# Game Result
print(f"Game Over! Outcome: {game_state['outcome']}")