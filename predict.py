import re
from collections import Counter

def preprocess_text(filepath):
    """
    Reads a text file, cleans it, and returns a list of words.
    - Converts to lowercase
    - Removes punctuation
    - Splits into individual words (tokens)
    """
    print(f"Reading file: {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    print(f"File processed. Total words: {len(words)}")
    return words

def build_model(words):
    """
    Builds a trigram model (a dictionary) from the list of words.
    The key is a tuple of two words (word1, word2).
    The value is a list of all words that have followed that pair.
    """
    print("Building model...")
    model = {}
    
    for i in range(2, len(words)):
        word1 = words[i-2]
        word2 = words[i-1]
        next_word = words[i]
        
        key = (word1, word2)
        
        if key not in model:
            model[key] = []
            
        model[key].append(next_word)
        
    print("Model built successfully!")
    return model

def predict_next_word(model, last_two_words):
    """
    Predicts the next word given the last two words (a key).
    It returns the most common word that follows the pair.
    """
   
    key = last_two_words

    if key not in model:
        return None 
        
    possible_words = model[key]
    
    most_common_word = Counter(possible_words).most_common(1)[0][0]
    return most_common_word

def main():
    """
    The main function to run the program.
    """
    try:
        words = preprocess_text('data.txt')
        model = build_model(words)
        
        print("\n--- Predictive Text Generator ---")
        print("Enter two words to get a prediction.")
        print("Type 'quit' to exit.")
        
        while True:
            user_input = input('> ')
          
            if user_input.lower() == 'quit':
                break
          
            input_words = re.sub(r'[^a-z\s]', '', user_input.lower()).split()
            
            if len(input_words) < 2:
                print("Please enter at least two words.")
                continue
         
            key = tuple(input_words[-2:])
            prediction = predict_next_word(model, key)
            
            if prediction:
                print(f"   ... {prediction}")
            else:
                print("   (No prediction found for this pair.)")

    except FileNotFoundError:
        print("\n[ERROR] 'data.txt' not found.")
        print("Please download a plain text file and rename it to 'data.txt' in the same folder as this script.")

if __name__ == "__main__":
    main()