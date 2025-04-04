import os
import glob
import requests
import json
import time
from pathlib import Path

def get_manuscript_files():
    """Get all manuscript files from the test_manuscripts directory."""
    base_dir = "test_manuscripts"
    if not os.path.exists(base_dir):
        print("No test_manuscripts directory found. Please run combine_subtitles.py first.")
        return []
    
    # Get all .txt files from the directory
    manuscript_files = []
    for txt_file in glob.glob(os.path.join(base_dir, "*.txt")):
        # Get the filename without extension
        filename = os.path.splitext(os.path.basename(txt_file))[0]
        manuscript_files.append({
            'path': txt_file,
            'name': filename
        })
    
    return manuscript_files

def display_manuscripts(manuscript_files):
    """Display all available manuscript files in a numbered list."""
    if not manuscript_files:
        print("No manuscript files found.")
        return
    
    print("\nAvailable manuscript files:")
    print("-" * 80)
    for i, manuscript in enumerate(manuscript_files, 1):
        print(f"{i}. {manuscript['name']}")
    print("-" * 80)

def read_manuscript_file(file_path):
    """Read and return the contents of a manuscript file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return ""

def generate_test_with_free_api(content, num_questions, difficulty):
    """Generate a test using a free API."""
    # Using the Hugging Face Inference API with a free model
    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
    
    # Prepare the prompt
    prompt = f"""
    Create a {difficulty} difficulty test with {num_questions} multiple choice questions based on the following content.
    Format each question as:
    
    Q1. [Question text]
    A) [Option A]
    B) [Option B]
    C) [Option C]
    D) [Option D]
    
    Answer: [Correct option letter]
    
    Content:
    {content[:4000]}  # Limit content length to avoid API limits
    """
    
    # Prepare headers (no API key needed for some models)
    headers = {"Content-Type": "application/json"}
    
    # Prepare payload
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 1000,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True
        }
    }
    
    try:
        # Make API request
        response = requests.post(API_URL, headers=headers, json=payload)
        
        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', '')
            else:
                return "Failed to generate test. API response format unexpected."
        else:
            # If rate limited, wait and try again
            if response.status_code == 429:
                print("API rate limited. Waiting 20 seconds before retrying...")
                time.sleep(20)
                return generate_test_with_free_api(content, num_questions, difficulty)
            else:
                return f"API request failed with status code: {response.status_code}"
    except Exception as e:
        return f"Error generating test: {str(e)}"

def save_test(test_content, manuscript_name, num_questions, difficulty):
    """Save the generated test to a file."""
    try:
        # Create output directory if it doesn't exist
        output_dir = "generated_tests"
        os.makedirs(output_dir, exist_ok=True)
        
        # Create filename
        filename = f"{manuscript_name}_{num_questions}q_{difficulty}.txt"
        output_path = os.path.join(output_dir, filename)
        
        # Save the test
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        print(f"\nTest saved to: {output_path}")
        return True
    except Exception as e:
        print(f"Error saving test: {str(e)}")
        return False

def main():
    # Get all manuscript files
    manuscript_files = get_manuscript_files()
    
    # Display available manuscripts
    display_manuscripts(manuscript_files)
    
    if not manuscript_files:
        return
    
    # Get user selection
    while True:
        try:
            selection = input("\nEnter the number of the manuscript to use (1-{}): ".format(len(manuscript_files)))
            index = int(selection) - 1
            
            # Validate selection
            if index < 0 or index >= len(manuscript_files):
                print("Invalid selection. Please enter a number from the list above.")
                continue
            
            selected_manuscript = manuscript_files[index]
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Get number of questions
    while True:
        try:
            num_questions = int(input("\nEnter the number of questions (1-10): "))
            if num_questions < 1 or num_questions > 10:
                print("Please enter a number between 1 and 10.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Get difficulty level
    print("\nSelect difficulty level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    
    while True:
        try:
            difficulty_choice = int(input("\nEnter your choice (1-3): "))
            if difficulty_choice < 1 or difficulty_choice > 3:
                print("Please enter a number between 1 and 3.")
                continue
            
            difficulty_map = {1: "Easy", 2: "Medium", 3: "Hard"}
            difficulty = difficulty_map[difficulty_choice]
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Read the manuscript content
    content = read_manuscript_file(selected_manuscript['path'])
    
    if not content:
        print("Failed to read manuscript content.")
        return
    
    print("\nGenerating test... This may take a minute.")
    
    # Generate the test
    test_content = generate_test_with_free_api(content, num_questions, difficulty)
    
    # Save the test
    save_test(test_content, selected_manuscript['name'], num_questions, difficulty)

if __name__ == "__main__":
    main() 