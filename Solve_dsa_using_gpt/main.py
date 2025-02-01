import streamlit as st
import openai
import json
import os

# Configuration - ensure you have your OpenAI API key
openai.api_key = os.getenv("bce4e89902160a5eed7d2279b4685a2a")


def generate_dsa_question(topic, difficulty):
    """
    Generate a dynamic DSA question using OpenAI API
    """
    try:
        prompt = f"""
        Create a comprehensive {difficulty.lower()} level coding problem for {topic} 
        that can be solved in a programming interview setting.

        Provide a response in strict JSON format with these exact keys:
        {{
            "title": "Concise problem title",
            "description": "Detailed problem description explaining the challenge",
            "input_format": "Explanation of input parameters",
            "output_format": "Explanation of expected output",
            "example": "Code or text example demonstrating problem solving",
            "constraints": [
                "Specific technical constraints for the solution",
                "Performance or implementation restrictions"
            ],
            "test_cases": [
                {{
                    "input": "First test case input",
                    "expected_output": "Corresponding output",
                    "explanation": "Why this test case matters"
                }},
                {{
                    "input": "Second test case input", 
                    "expected_output": "Corresponding output",
                    "explanation": "Alternative scenario testing"
                }}
            ]
        }}

        Requirements:
        - Problem must be solvable in Python
        - Include clear, unambiguous instructions
        - Provide meaningful test cases
        - Ensure problem demonstrates core concepts of the topic
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert coding interview question generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        # Extract and parse the JSON response
        question_json = response['choices'][0]['message']['content']
        question = json.loads(question_json)

        return question

    except Exception as e:
        st.error(f"Error generating question: {e}")
        return None


def evaluate_solution(question, user_code):
    """
    Evaluate user's solution using OpenAI API
    """
    try:
        prompt = f"""
        Evaluate the following solution for the problem:

        Problem: {question['title']}
        Description: {question['description']}

        User's Code:
        ```python
        {user_code}
        ```

        Provide a detailed evaluation including:
        1. Is the solution correct?
        2. Time and space complexity
        3. Potential improvements
        4. Correct implementation if the solution is incorrect

        Response Format:
        {{
            "is_correct": true/false,
            "feedback": "Detailed code analysis",
            "correct_solution": "Correct Python implementation",
            "time_complexity": "Big O notation",
            "space_complexity": "Big O notation",
            "improvements": ["Optimization suggestions"]
        }}
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert code reviewer and algorithm specialist."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        # Extract and parse the JSON response
        evaluation_json = response['choices'][0]['message']['content']
        evaluation = json.loads(evaluation_json)

        return evaluation

    except Exception as e:
        st.error(f"Error evaluating solution: {e}")
        return None


def main():
    # Set page title and icon
    st.set_page_config(page_title="DSA Learning Platform", page_icon="🧠")

    # Initialize session state
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None

    # Main title
    st.title("🧠 Dynamic DSA Learning Platform")

    # Sidebar for topic and difficulty selection
    st.sidebar.header("🔍 Problem Configuration")

    # List of DSA topics
    dsa_topics = [
        "Arrays", "Linked Lists", "Trees", "Graphs",
        "Dynamic Programming", "Strings", "Recursion",
        "Sorting", "Searching", "Stack", "Queue"
    ]

    # Topic and difficulty selection
    selected_topic = st.sidebar.selectbox("Select Topic", dsa_topics)
    selected_difficulty = st.sidebar.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])

    # Generate Question Button
    if st.sidebar.button("Generate Question"):
        # Generate question dynamically
        st.session_state.current_question = generate_dsa_question(selected_topic, selected_difficulty)

    # Display Question if exists
    if st.session_state.current_question:
        question = st.session_state.current_question

        # Two-column layout
        col1, col2 = st.columns(2)

        with col1:
            # Problem Details
            st.header(f"🎯 {question['title']}")
            st.subheader("Problem Description")
            st.write(question['description'])

            st.subheader("Example")
            st.code(question.get('example', 'No example provided'), language='python')

            st.subheader("Constraints")
            for constraint in question.get('constraints', []):
                st.markdown(f"- {constraint}")

        with col2:
            # Code Submission Area
            st.header("💻 Your Solution")
            user_code = st.text_area("Write your Python solution here", height=400, key="user_solution")

            # Submit Solution
            if st.button("Submit Solution"):
                # Evaluate solution
                evaluation = evaluate_solution(question, user_code)

                if evaluation:
                    # Display evaluation results
                    st.subheader("🔍 Evaluation Results")

                    # Correctness
                    if evaluation['is_correct']:
                        st.success("✅ Solution is Correct!")
                    else:
                        st.error("❌ Solution needs improvement")

                    # Feedback
                    st.subheader("Feedback")
                    st.write(evaluation['feedback'])

                    # Complexity Analysis
                    st.subheader("Complexity")
                    col_time, col_space = st.columns(2)
                    with col_time:
                        st.metric("Time Complexity", evaluation.get('time_complexity', 'N/A'))
                    with col_space:
                        st.metric("Space Complexity", evaluation.get('space_complexity', 'N/A'))

                    # Correct Solution
                    if not evaluation['is_correct']:
                        st.subheader("Suggested Solution")
                        st.code(evaluation.get('correct_solution', 'No solution provided'), language='python')

                    # Improvements
                    st.subheader("Potential Improvements")
                    for improvement in evaluation.get('improvements', []):
                        st.markdown(f"- {improvement}")


if __name__ == "__main__":
    main()
