# ROT Cipher Decoder

A Python tool that uses AI to automatically decode ROT cipher encrypted text. It generates all possible ROT variations (ROT1 through ROT25) and uses OpenAI's GPT model to identify the most likely correct decryption.

When I started reading a textbook on Cryptography, one of the first ciphers I learned about were mono-alphabetic substitution ciphers, namely the ROT. ROT ciphers replace a letter with the nth letter after it, with n being any number the encrypter chooses. The way you decrypt these is by doing all 25 ROTs (26 letters minus the one you start with), and seeing which one results in english text. My textbook mentioned that one drawback of this method is that its hard to automate it, since computers can't "make sense" of strings of letters like we can. More specifically, computers can't figure out which of the 26 ROTs is correct. But as a CS student living in 2025, I know that AI has done a whole lot in giving computers "sentience". So after finishing the chapter, I got to work on bolting an AI model on to a ROT decoder.

## Features

- Generates all possible ROT cipher variations
- Uses AI to identify the correct decryption
- Handles both uppercase and lowercase text
- Preserves non-alphabetic characters

## Requirements

- Python 3.6 or higher
- OpenAI API key

## Installation

1. Clone this repository:
```bash
git clone https://github.com/pranubot/rot-cipher-decoder.git
cd rot-cipher-decoder
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project directory and add your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

## Usage

Run the program:
```bash
python rot_decoder.py
```

Enter your encrypted text when prompted. The program will:
1. Generate all possible ROT variations
2. Display all variations (for texts ≤ 50 characters)
3. Use AI to identify the most likely correct decryption
4. Show the results

To exit the program, type 'quit'.

## Example

Input:
```
URYYB JBEYQ
```

Output:
```
Most likely decryption (ROT13):
Original text: URYYB JBEYQ
Decrypted text: HELLO WORLD
```
