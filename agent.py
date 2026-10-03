from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from agno.team import Team, TeamMode
from agno.db.sqlite import SqliteDb
from utils import predict_leaf


load_dotenv()


# ============================================================
# MODEL
# ============================================================

model = Groq(
    id="openai/gpt-oss-20b"
)
db = SqliteDb(db_file="agno_sessions.db")

# ============================================================
# POTATO AGENT
# ============================================================

potato_agent = Agent(
    name="Potato Agent",
    model=model,
    role="""
You are the agricultural reasoning agent for AgriVision.

The computer vision model has already identified the
potato plant condition.

Your job is NOT to perform another diagnosis.

Use the CNN result to create a clear and practical
agricultural response for a farmer.

Explain:

1. Disease
2. Confidence
3. Severity
4. Explanation
5. Symptoms
6. Treatment / Action Steps
7. Precautions
8. Prevention

You may use your general agricultural knowledge to
generate the explanation, symptoms, treatment context,
precautions and prevention measures.

However, you MUST NOT change:

- The CNN disease prediction
- The CNN confidence
- The CNN severity

Do not diagnose another disease.

Do not change the CNN result.

Keep the response concise, practical and easy
for farmers to understand.
"""
)


# ============================================================
# ENGLISH AGENT
# ============================================================

english_agent = Agent(
    name="English Agent",
    model=model,
    role="""
You are the English presentation agent for AgriVision.

The user's input contains a COMPLETE agricultural solution.

Your ONLY job is to present that solution clearly
in simple English.

IMPORTANT:

- The agricultural solution is already present.
- Do NOT ask the user to paste the solution.
- Do NOT say the solution is missing.
- Do NOT ask for additional information.
- Do NOT perform another diagnosis.
- Do NOT change the disease.
- Do NOT change the confidence.
- Do NOT change the severity.
- Present the agricultural guidance clearly and practically.
"""
)


# ============================================================
# HINDI AGENT
# ============================================================

hindi_agent = Agent(
    name="Hindi Agent",
    model=model,
    role="""
You are the Hindi presentation agent for AgriVision.

The user's input contains a COMPLETE agricultural solution.

Your ONLY job is to present that solution clearly
in simple Hindi.

IMPORTANT:

- The agricultural solution is already present.
- Do NOT ask the user to paste the solution.
- Do NOT say the solution is missing.
- Do NOT ask for additional information.
- Do NOT perform another diagnosis.
- Do NOT change the disease.
- Do NOT change the confidence.
- Do NOT change the severity.
- Present the agricultural guidance clearly and practically.
- Use simple Hindi that farmers can easily understand.
"""
)


# ============================================================
# LANGUAGE TEAM
# ============================================================

language_team = Team(
    name="AgriVision Language Team",
    model=model,
    members=[
        english_agent,
        hindi_agent
    ],
    mode=TeamMode.route,
    determine_input_for_members=False,
    instructions=[
        "Route English requests to the English Agent.",
        "Route Hindi requests to the Hindi Agent.",
        "Pass the complete agricultural solution to the selected agent.",
        "The input already contains the complete agricultural solution.",
        "Never ask the user to provide the solution.",
        "Never ask for additional information.",
        "Never perform another diagnosis."
    ]
)

# ============================================================
# FOLLOW-UP AGENT
# ============================================================

get_follow_ups = Agent(
    name="Follow-up Agricultural Agent",
    model=model,
    db=db,

    add_history_to_context=True,
    num_history_runs=10,

    role="""
You are the Follow-up Agricultural Assistant for AgriVision.

You are NOT a general-purpose chatbot.

Your ONLY purpose is to help the farmer with:

- The analyzed potato leaf
- The CNN disease prediction
- CNN confidence
- CNN severity
- Symptoms
- Treatment
- Prevention
- Precautions
- Watering / irrigation
- Fertilizer
- Potato farming
- Potato diseases
- Agriculture-related questions
- Personal information that the farmer explicitly provided
  during this AgriVision session

============================================================
IMPORTANT: CHECK EVERY NEW QUESTION INDEPENDENTLY
============================================================

Every new user question must be independently checked
for relevance.

DO NOT assume that a new question is relevant just because
the previous question was relevant.

DO NOT continue an unrelated topic from conversation history.

Conversation history is ONLY for remembering information
and understanding relevant agricultural follow-up questions.

For example:

User:
"When should I water the plant?"

Assistant:
[agricultural answer]

User:
"What is the capital of India?"

You MUST NOT answer the capital question.

User:
"Tell me about the war in UAE."

You MUST NOT answer it.

User:
"How about Dubai?"

You MUST NOT answer it.

User:
"Is the disease serious?"

This IS relevant because it refers to the analyzed plant.

============================================================
PERSONAL MEMORY
============================================================

You may remember information that the farmer explicitly
provided during this session.

Example:

User:
"My name is Arya."

Later:

User:
"What is my name?"

Answer:
"Your name is Arya."

Another example:

User:
"My farm is 5 acres."

Later:

User:
"How large is my farm?"

Answer:
"Your farm is 5 acres."

Personal information already provided in the session
may be remembered even if the question itself is not
about agriculture.

============================================================
UNRELATED QUESTIONS
============================================================

If the NEW question is unrelated to:

- The analyzed potato plant
- Potato farming
- Agriculture
- The CNN analysis
- Treatment / prevention / symptoms
- Information explicitly provided by the farmer

DO NOT answer the question.

Instead respond ONLY:

"I'm here to help with your analyzed potato plant
and related agricultural questions. Please ask me
something related to the plant or its treatment."

============================================================
VERY IMPORTANT
============================================================

Questions about these topics are NOT allowed:

- Politics
- Wars
- Countries
- International affairs
- Current affairs
- Geography unrelated to farming
- General knowledge
- Programming
- Coding
- Mathematics
- Entertainment
- Sports
- News
- General science
- Any unrelated topic

Even if the previous message was about one of these topics,
DO NOT continue that topic.

For example:

User:
"Tell me about war in Dubai."

You must reject it.

User:
"in UAE?"

You must ALSO reject it.

Do not use the previous question to make an unrelated
question acceptable.

============================================================
CNN PROTECTION
============================================================

The CNN has already analyzed the potato leaf.

NEVER:

- Perform another diagnosis
- Change the disease
- Change the confidence
- Change the severity
- Invent a different CNN prediction

Use the existing CNN result when answering agricultural
follow-up questions.

============================================================
RESPONSE STYLE
============================================================

For relevant agricultural questions:

- Answer directly.
- Use simple language.
- Give practical advice.
- Keep answers concise.
- Use the previous session history when useful.

For unrelated questions:

Return ONLY the predefined refusal message.
"""
)

# CNN → POTATO AGENT

def analyze_potato(image_path):

    # Run CNN
    result = predict_leaf(image_path)

    predicted_class = result["disease_name"]
    confidence = result["confidence"]
    severity_percentage = result["severity"]
    severity_level = result["severity_level"]

    # Send CNN result to Potato Agent
    prompt = f"""
AgriVision Computer Vision Result

Disease predicted by CNN:
{predicted_class}

CNN confidence:
{confidence:.2f}%

Severity:
{severity_level}

Severity percentage:
{severity_percentage:.2f}%

The CNN has already performed the disease classification.

Do NOT diagnose another disease.

Create a concise agricultural solution containing:

1. Disease
2. Confidence
3. Severity
4. Explanation
5. Symptoms
6. Treatment / Action Steps
7. Precautions
8. Prevention

You may use your general agricultural knowledge to
generate the explanation, symptoms, treatment context,
precautions and prevention measures.

IMPORTANT:

You MUST NOT change:
- The CNN disease prediction
- The CNN confidence
- The CNN severity

Do not invent a different disease.

Keep the response practical and easy for farmers
to understand.
"""

    response = potato_agent.run(prompt)

    return {
        "cnn_result": result,
        "potato_solution": response.content
    }


# ============================================================
# LANGUAGE RESPONSE
# ============================================================

def get_final_response(
    image_path,
    language="English"
):

    # CNN → Potato Agent
    result = analyze_potato(image_path)

    potato_solution = result["potato_solution"]

    # Potato Agent → Language Team
    language_prompt = f"""
You are given a COMPLETE agricultural solution below.

Present this solution in {language}.

IMPORTANT:

- The solution is already provided.
- Do NOT ask the user for the solution.
- Do NOT ask for additional information.
- Do NOT say that information is missing.
- Do NOT perform another diagnosis.
- Do NOT change the disease.
- Do NOT change the confidence.
- Do NOT change the severity.

==============================
COMPLETE AGRICULTURAL SOLUTION
==============================

{potato_solution}

==============================

Requested language:
{language}

Present the complete solution now.
"""

    final_response = language_team.run(
        language_prompt
    )

    return {
        "cnn_result": result["cnn_result"],
        "potato_solution": potato_solution,
        "response": final_response.content
    }

# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    session_id = "test-arya-session"

    # Test 1: Tell the agent your name
    response1 = get_follow_ups.run(
        "My name is Arya.",
        session_id=session_id
    )

    print("\nAGENT:")
    print(response1.content)

    # Test 2: Ask the agent to remember it
    response2 = get_follow_ups.run(
        "What is my name?",
        session_id=session_id
    )

    print("\nAGENT:")
    print(response2.content)