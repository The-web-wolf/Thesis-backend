import google.generativeai as genai

# Initialize game state
game_state = {
    "hireability": 50,
    "progress": [],
    "outcome": None
}

maxSteps = 5
hiringThreshold = 70
maxGainPoints = 10
minGainPoints = 10

genai.configure(api_key='AIzaSyCzO8JqOHfdcm8xcKecBA1NpIAj2FsA0V8')
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_story_step(current_state):
    """Generate the next story step based on the current game state."""
    prompt = f'''
      You are narrating an interactive story set in the world of Suits, where the player takes on the role of Mike Ross navigating his interview at Pearson Hardman. The goal is to determine the player's "hireability," starting at 50, which changes based on their choices.
      
      - Begin the story from when the player meets at the reception Donna, the user should have one interaction with Donna and following steps with Harvey.
      - Player's current hireability: {current_state["hireability"]}
      - Recent choices: {current_state["progress"]}
      
      - Provide a short narration of the next story step based on the player's actions so far.
      - Present exactly three distinct concise choices the player can make. Each choice should subtly influence the hireability score.
      - Return the result as a JSON object in this format:

      {{
        "story": "Narrate the next part of the story.",
        "choices": [
          {{
            "text": "Choice A.",
            "effect": "+x"
          }},
          {{
            "text": "Choice B.",
            "effect": "-x"
          }},
          {{
            "text": "Choice C.",
            "effect": "+x"
          }}
        ]
      }}

      - Ensure "effect" reflects the impact each choice has on hireability, ranging FROM -{minGainPoints} to +{maxGainPoints}.
      - Keep the tone engaging, and align the narrative with Suits' high-stakes legal drama.
      - Do NOT add extra text — only output the object WITHOUT ANY FORMATTING.
    '''
    response = model.generate_content(prompt)
    return response.text.strip()

def interpret_user_input(user_input, current_state, step_story):
    """Interpret custom user input and determine its effect on hireability."""
    prompt = f'''
      Player hireability: {current_state["hireability"]}.
      Recent choices: {current_state["progress"]}.
      The player has written a reply: "{user_input}" to the step "{step_story}".
      Score the player's response and determine its effect on hireability.
      Return the response in JSON format like this:
      {{
        "reply": "",
        "effect": "-x",
        "reasoning": ""
      }}
      
      - Ensure "effect" reflects the impact each choice has on hireability, ranging FROM -5 to +5.
      - Do NOT add extra text — only output the object WITHOUT ANY FORMATTING.
    '''
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_conclusion(current_state):
    """Generate a natural conclusion for the interview based on the player's performance."""
    prompt = f'''
      Based on the interview so far, craft a natural-sounding conclusion for the player’s interview with Harvey Specter. Reflect the current hireability score and the choices the player made:
      
      - Hireability: {current_state["hireability"]}
      - Choices: {current_state["progress"]}
      
      Conclude the interview accordingly. If the hireability is greater than {hiringThreshold}, make it sound like the player got hired. If it’s {hiringThreshold} or below, make it clear they got rejected but keep the tone professional and engaging.
      Return only the conclusion as a string without any extra formatting.
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

    # Parse JSON response
    try:
        step_data = eval(step)
        currentStep = step_data
        print(step_data["story"])
        choices = step_data["choices"]
        print("\nChoices", choices, "\n")
        for i, choice in enumerate(choices, 1):
            print(f"{i}) {choice['text']}")
    except Exception as e:
        print("Error parsing step data:", e)
        break

    # Simulated choice input (replace with input() for real interaction)
    choice = input("Choose (1/2/3 or type your response): ").strip()
    
    print("User's choice", choice)

    if choice in ["1", "2", "3"]:
        selected_choice = choices[int(choice) - 1]
        effect = int(selected_choice["effect"])
        game_state["hireability"] += effect
        game_state["progress"].append(selected_choice["text"])
    else:
        # Handle custom user input
        interpretation = interpret_user_input(choice, game_state, currentStep["story"])
        print("\n\n Interpretation: ", interpretation)
        try:
            interpretation_data = eval(interpretation)
            print(interpretation_data["reply"])
            effect = int(interpretation_data["effect"])
            game_state["hireability"] += effect
            game_state["progress"].append(choice)
        except Exception as e:
            print("Error interpreting custom input:", e)
            useCurrentStep = True
            continue

    # Check end condition
    if len(game_state["progress"]) >= maxSteps:
        game_state["outcome"] = "Hired" if game_state["hireability"] > hiringThreshold else "Rejected"

# Game Result
conclusion = generate_conclusion(game_state)
print(conclusion)
print(f"Game Over! Outcome: {game_state['outcome']}")
