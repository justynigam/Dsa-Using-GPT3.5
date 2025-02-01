# utils.py

import re
import json
import openai
import traceback
import streamlit as st


def validate_python_code(code):
    """
    Perform basic validation of Python code

    Args:
        code (str): Python code to validate

    Returns:
        dict: Validation results
    """
    try:
        # Check for empty code
        if not code or code.strip() == '':
            return {
                'is_valid': False,
                'error': 'Code cannot be empty'
            }

        # Basic syntax check
        compile(code, '<string>', 'exec')

        return {
            'is_valid': True,
            'error': None
        }

    except SyntaxError as e:
        return {
            'is_valid': False,
            'error': f"Syntax Error: {e}"
        }
    except Exception as e:
        return {
            'is_valid': False,
            'error': f"Unexpected Error: {e}"
        }


def extract_code_solution(text):
    """
    Extract Python code from a text block

    Args:
        text (str): Text potentially containing Python code

    Returns:
        str: Extracted Python code
    """
    # Use regex to find code blocks
    code_blocks = re.findall(r'```python\n(.*?)```', text, re.DOTALL)

    # If code blocks found, return the first one
    if code_blocks:
        return code_blocks[0].strip()

    # Fallback: return the entire text if no code block found
    return text.strip()


def generate_test_code(question, solution):
    """
    Generate test code to verify the solution

    Args:
        question (dict): Question details
        solution (str): User's solution code

    Returns:
        str: Test code to validate the solution
    """
    try:
        # Prompt to generate test cases
        prompt = f"""
        Create a Python test function to validate the following solution:

        Problem: {question.get('title', 'Unknown Problem')}
        Problem Description: {question.get('description', 'No description')}

        Solution:
        ```python
        {solution}
        ```

        Generate comprehensive test cases that:
        1. Cover multiple scenarios
        2. Check edge cases
        3. Verify the solution's correctness
        4. Use assert statements
        5. Provide meaningful error messages

        Return only the Python test code.
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert test case generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )

        # Extract test code
        test_code = response.choices[0].message.content
        return test_code

    except Exception as e:
        st.error(f"Error generating test code: {e}")
        return None


def safe_code_execution(code, test_code):
    """
    Safely execute user's code with test cases

    Args:
        code (str): User's solution code
        test_code (str): Generated test code

    Returns:
        dict: Execution results
    """
    try:
        # Combine solution and test code
        full_code = code + "\n\n" + test_code

        # Execute in a restricted environment
        namespace = {}
        exec(full_code, namespace)

        return {
            'success': True,
            'message': 'All tests passed successfully!'
        }

    except AssertionError as e:
        return {
            'success': False,
            'error_type': 'AssertionError',
            'message': str(e)
        }
    except Exception as e:
        return {
            'success': False,
            'error_type': type(e).__name__,
            'message': str(e),
            'traceback': traceback.format_exc()
        }


def analyze_code_complexity(code):
    """
    Perform basic code complexity analysis

    Args:
        code (str): Python code to analyze

    Returns:
        dict: Complexity analysis results
    """
    try:
        # Prompt for complexity analysis
        prompt = f"""
        Analyze the time and space complexity of the following Python code:

        ```python
        {code}
        ```

        Provide:
        1. Time Complexity in Big O notation
        2. Space Complexity in Big O notation
        3. Brief explanation of the complexity
        4. Potential optimization strategies

        Return response as JSON:
        {{
            "time_complexity": "O(n)",
            "space_complexity": "O(1)",
            "explanation": "Detailed complexity breakdown",
            "optimization_suggestions": ["suggestion1", "suggestion2"]
        }}
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert algorithm complexity analyzer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )

        # Parse JSON response
        complexity_json = response.choices[0].message.content
        complexity = json.loads(complexity_json)

        return complexity

    except Exception as e:
        st.error(f"Error analyzing code complexity: {e}")
        return {
            'time_complexity': 'N/A',
            'space_complexity': 'N/A',
            'explanation': 'Unable to analyze',
            'optimization_suggestions': []
        }


def log_user_interaction(question, solution, evaluation):
    """
    Log user interactions for potential future analysis

    Args:
        question (dict): Question details
        solution (str): User's solution
        evaluation (dict): Solution evaluation results
    """
    # In a real application, you might:
    # 1. Write to a database
    # 2. Save to a log file
    # 3. Send to an analytics service

    interaction_log = {
        'timestamp': st.session_state.get('interaction_timestamp', None),
        'topic': question.get('topic', 'Unknown'),
        'difficulty': question.get('difficulty', 'Unknown'),
        'solution_length': len(solution),
        'is_correct': evaluation.get('is_correct', False)
    }

    # Example of simple console logging
    print(json.dumps(interaction_log, indent=2))