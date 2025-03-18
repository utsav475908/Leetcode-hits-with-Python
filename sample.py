



import openai
import requests

# Set your OpenAI API key (replace with your actual key)
openai.api_key = "Your_API_KEY_tobereplaced"


# LeetCode API endpoint
LEETCODE_API_URL = "https://leetcode.com/api/problems/all/"

def fetch_leetcode_problem(problem_id):
    """
    Fetch a LeetCode problem by its ID using the LeetCode API.
    """
    try:
        response = requests.get(LEETCODE_API_URL)
        response.raise_for_status()  # Raise an error for bad status codes
        problems = response.json()["stat_status_pairs"]
        for problem in problems:
            if problem["stat"]["frontend_question_id"] == problem_id:
                return {
                    "title": problem["stat"]["question__title"],
                    "slug": problem["stat"]["question__title_slug"],
                    "difficulty": problem["difficulty"]["level"],
                }
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching LeetCode problem: {e}")
        return None

def get_chatgpt_response(prompt):
    """
    Get a response from OpenAI's GPT model.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use "gpt-3.5-turbo" if GPT-4 is not available
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides solutions and hints for LeetCode problems."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
        )
        return response.choices[0].message["content"].strip()
    except openai.error.OpenAIError as e:
        print(f"Error calling OpenAI API: {e}")
        return None

def main():
    print("Welcome to the LeetCode Chatbot!")
    while True:
        try:
            # Ask the user for a LeetCode problem ID
            problem_id = int(input("Enter the LeetCode problem ID (or 0 to exit): "))
            if problem_id == 0:
                print("Exiting the chatbot. Goodbye!")
                break

            # Fetch the problem details
            problem = fetch_leetcode_problem(problem_id)
            if not problem:
                print(f"Problem with ID {problem_id} not found.")
                continue

            print(f"\nProblem: {problem['title']}")
            print(f"Difficulty: {'Easy' if problem['difficulty'] == 1 else 'Medium' if problem['difficulty'] == 2 else 'Hard'}")
            print(f"Slug: {problem['slug']}")

            # Ask the user what they need
            user_input = input("\nWhat do you need? (e.g., solution, hint, explanation): ").lower()

            # Generate a prompt for ChatGPT
            prompt = f"LeetCode Problem: {problem['title']}\nDifficulty: {problem['difficulty']}\n\n{user_input}"
            response = get_chatgpt_response(prompt)

            if response:
                print("\nChatbot Response:")
                print(response)
            else:
                print("Failed to get a response from the chatbot.")

            print("\n" + "=" * 50 + "\n")

        except ValueError:
            print("Please enter a valid problem ID (number).")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
