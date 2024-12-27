import openai
import streamlit as st

# Function to generate criteria based on TEKS description
def generate_criteria(teks_description):
    prompt = f"""
    Based on the following TEKS description:
    "{teks_description}"
    Generate specific criteria for creating educational questions suitable for 3rd graders. 
    The criteria should include:
    - Skills to be assessed
    - Constraints on numbers or operations
    - Any special considerations for the type of problems (e.g., one-step, two-step, real-life context).
    Keep the criteria concise and aligned with the TEKS description.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use "gpt-3.5-turbo" if desired
            messages=[{"role": "user", "content": prompt}],
            temperature=0  # Set temperature to 0 for consistent output
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error generating criteria: {e}"

# Function to generate questions based on criteria and TEKS description
def generate_questions(teks_description, sample_questions, criteria):
    prompt = f"""
    You are an educational content creator specializing in test questions aligned with Texas Essential Knowledge and Skills (TEKS).
    Based on the following TEKS description:
    "{teks_description}"
    And the provided sample questions:
    {sample_questions if sample_questions else 'None provided'}
    Please generate 3 original questions. Ensure they meet these criteria:
    - Suitable for 3rd graders
    - Aligned with the provided TEKS
    - {criteria}
    - Vary contexts and ensure clarity. 
    Do not add an introductory or conclusion sentence. Just give the question.
    """
    try:
        response = openai.ChatCompletion.create(
            model="o1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=1
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error generating questions: {e}"

# Function to generate solutions and step-by-step explanations
def generate_solutions(questions):
    prompt = f"""
    You are a math tutor helping 3rd graders learn addition and subtraction. For each math problem I provide, please produce a step-by-step solution that a 3rd grader can easily follow. Use the following guidelines:
    - Clarity for a 3rd Grader: Use simple language and explain what you’re doing in each step, as if you’re talking to a child learning math.
    - Properties of Operations: Mention how properties of operations help solve the problem or check the work.
    - Step-by-Step: Number each step and use clear, short sentences. Explain why you do each step.
    - Encourage Understanding: Show how to check the answer or think about the problem in more than one way, if possible.

    Please solve the following questions:
    {questions}

    Do not add an introductory or conclusion sentence.
    """
    try:
        response = openai.ChatCompletion.create(
            model="o1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=1  # Set temperature to 0 for consistent output
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error generating solutions: {e}"

# Function to display the full output
def display_output(teks_description, questions, solutions):
    print("\n--- TEKS Description ---")
    print(teks_description)
    print("\n--- Generated Questions ---")
    print(questions)
    print("\n--- Step-by-Step Solutions ---")
    print(solutions)

# Streamlit app
st.title("TEKS-Aligned Question Generator")

api_key = st.text_input("Enter your OpenAI API Key:", type="password")

st.write("""
This application generates educational questions aligned with the Texas Essential Knowledge and Skills (TEKS) standards.
Enter a TEKS description and optional sample questions, and the app will generate new questions along with solutions.
""")

# User inputs
teks_description = st.text_area("Enter TEKS Description:", placeholder="e.g., Solve one-step and two-step problems involving addition and subtraction within 1,000...")
sample_questions = st.text_area(
    "Enter Sample Questions (optional):", 
    placeholder="e.g., 1. Roger has two boxes of nails. One box has 438 nails..."
)

if st.button("Generate Questions"):
    if not teks_description:
        st.error("TEKS description is required!")
    elif not api_key:
        st.error("API Key is required!")
    else:
        try:
            # Set API key
            openai.api_key = api_key

            # Generate criteria
            with st.spinner("Generating criteria..."):
                criteria = generate_criteria(teks_description)

            # Generate questions
            with st.spinner("Generating questions..."):
                generated_output = generate_questions(teks_description, sample_questions, criteria)

            # Generate step-by-step solutions
            with st.spinner("Generating solutions..."):
                solutions = generate_solutions(generated_output)

            # Display results
            st.write("### TEKS Description")
            st.write(teks_description)
            st.write("### Generated Questions")
            st.write(generated_output)
            st.write("### Generated Step-by-Step Solutions")
            st.write(solutions)

        except Exception as e:
            st.error(f"Error: {e}")
