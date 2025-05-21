import os
from typing import List, Tuple
from openai import OpenAI
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

def generate_rot_variations(text: str) -> List[Tuple[int, str]]:
    # Variations will hold all ROT variations
    variations = []
    
    # Generate all possible rotations (1-25)
    for rotation in range(1, 26):
        decrypted_text = ""
        
        # Process each character in the input text
        for char in text:
            if char.isalpha():
                # Convert to unicode value
                char_code = ord(char.upper()) - ord('A')
                # Apply rotation and wrap around using mod div
                new_code = (char_code - rotation) % 26
                # Convert back to letter
                new_char = chr(new_code + ord('A'))
                decrypted_text += new_char
            else:
                # Keep non-letters unchanged
                decrypted_text += char
        
        # add variation to results
        variations.append((rotation, decrypted_text))
    
    return variations

def analyze_with_chatgpt(variations: List[Tuple[int, str]]) -> Tuple[int, str]:
    """
    Send the variations to ChatGPT to determine which one makes the most sense.
    
    Args:
        variations (List[Tuple[int, str]]): List of (ROT number, decrypted text) tuples
    
    Returns:
        Tuple[int, str]: The most likely (ROT number, decrypted text) combination
    """
    # Initialize the OpenAI client
    client = OpenAI()
    
    # Create a prompt with all variations
    prompt = "Analyze these ROT cipher variations and tell me which one is correct English. IMPORTANT: Your response must start with 'ROT' followed by the number (1-25) of the correct variation. Here are the variations:\n\n"
    
    # Add each variation to the prompt
    for rot, text in variations:
        prompt += f"ROT{rot}: {text}\n"
    
    try:
        # Make the API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a cipher analysis tool. When shown ROT cipher variations, respond with 'ROT' followed by the number of the correct variation, then explain why it's correct."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3 
        )
        
        # Extract the ROT number from the response
        response_text = response.choices[0].message.content.strip()
        print(f"\nAI Response: {response_text}\n")  # Debug output
        
        # Look for "ROT" followed by a number in the response
        rot_match = re.search(r'ROT(\d+)', response_text)
        
        if rot_match:
            rot_number = int(rot_match.group(1))
            if 1 <= rot_number <= 25:
                # Find the corresponding decrypted text
                for rot, text in variations:
                    if rot == rot_number:
                        return (rot, text)
        
        # If no valid ROT number found, analyze the variations manually
        for rot, text in variations:
            # Check if the text appears to be English (contains common words)
            common_words = ['THE', 'BE', 'TO', 'OF', 'AND', 'IN', 'THAT', 'HAVE', 'IT', 'FOR']
            words = text.split()
            for word in words:
                if word in common_words:
                    return (rot, text)
        
        # If still no match found, return the first variation as fallback
        return variations[0]
        
    except Exception as e:
        print(f"Error calling ChatGPT API: {e}")
        # Return the first variation as fallback in case of error
        return variations[0]

def main():
    """
    Main program flow for the ROT cipher decoder.
    """
    print("Welcome to the ROT Cipher Decoder")
    print("This program will try all possible ROT variations and use AI to find the most likely decryption.")
    print("Make sure you have set up your OpenAI API key in an .env file.\n")

    while True:
        try:
            # Get input from user
            encrypted_text = input("Enter the encrypted text (or 'quit' to exit): ").strip()
            
            # Check for quit command
            if encrypted_text.lower() == 'quit':
                print("\nThank you for using the ROT Cipher Decoder")
                break
            
            if not encrypted_text:
                print("Please enter some text to decrypt.\n")
                continue
            
            # Convert to uppercase
            encrypted_text = encrypted_text.upper()
            
            print("\nGenerating ROT variations...")
            variations = generate_rot_variations(encrypted_text)
            
            # Display all variations if the text is short enough
            if len(encrypted_text) <= 50:
                print("\nAll possible variations:")
                for rot, text in variations:
                    print(f"ROT{rot}: {text}")
            
            print("\nAnalyzing variations with AI...")
            rot_number, decrypted_text = analyze_with_chatgpt(variations)
            
            print("\nResults:")
            print(f"Most likely decryption (ROT{rot_number}):")
            print(f"Original text: {encrypted_text}")
            print(f"Decrypted text: {decrypted_text}\n")
            
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try again.\n")

if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key.")
        exit(1)
    
    main() 