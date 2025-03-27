import google.generativeai as genai
import re

# Initialize game state
game_state = {
    "hiring_chance": 50,
    "progress": [],
    "outcome": None
}

maxSteps = 5

# Gemini API Key (replace 'your-api-key' with your actual key)
genai.configure(api_key='AIzaSyCzO8JqOHfdcm8xcKecBA1NpIAj2FsA0V8')
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_story_step(current_state, user_input=None):
    """Generate the next story step based on the current game state."""
    prompt = f'''
      Player hiring chance: {current_state["hiring_chance"]}%.
      Recent choices: {current_state["progress"]}.
      This is an interactive story set in the world of Suits, where the player takes on the role of Mike Ross navigating his interview at Pearson Hardman.
      The goal is to reach one of three possible outcomes: getting hired, being rejected, or being chased out by security. Adapt the game to end after {maxSteps} steps.
      On the {maxSteps} step, attach the decision on the last line (hired/rejected/chased).
      Narrate the next part of the story based on the current state, then present three distinct and creative choices for the player.
      The choices should be written in simple human vocabulary, relatable, and subtly influence the hiring chance.
      Avoid labeling the traits directly in the options. The choices should start with either A), B), or C).
      {f'Player input: "{user_input}". Adapt the story accordingly.' if user_input else ''}
    '''
    response = model.generate_content(prompt)
    return response.text.strip()

# Game Loop
currentStep = ""
useCurrentStep = False
while game_state["outcome"] is None:
    step = generate_story_step(game_state) if not useCurrentStep else currentStep
    useCurrentStep = False
    print(game_state)
    currentStep = step

    # Use regex to match the options
    matches = re.findall(r'[A-C]\)(.*?)(?=\n[A-C]\)|$)', step, re.S)
    A, B, C = matches

    # get the last line of the message
    resultReached = step.split("\n")[-1]

    # Print the narrator message and the next options
    print(step)

    # Simulated choice input (replace with input() for real interaction)
    choice = input("Choose or type your action: ").strip()

    # Map numbers to letters
    choice_map = {"1": "A", "2": "B", "3": "C"}
    mapped_choice = choice_map.get(choice, choice.upper())

    if mapped_choice in ["A", "B", "C"]:
        chosenOption = A if mapped_choice == "A" else B if mapped_choice == "B" else C
        print("Chosen option:", chosenOption)
        game_state["progress"].append(chosenOption)
    else:
        print("Free input detected, adapting story...")
        game_state["progress"].append(choice)
        step = generate_story_step(game_state, user_input=choice)
        currentStep = step
        useCurrentStep = True

# Game Result
print(f"Game Over! Outcome: {game_state['outcome']}")
