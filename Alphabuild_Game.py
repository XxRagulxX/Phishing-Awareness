import random

# Phising Questions 
phishing_messages = [
    "Congratulations! You've won a free vacation. Click the link to claim your prize.",
    "Your bank account has been compromised. Please click the link to reset your password.",     
    "Urgent message: Your email account will be suspended. Verify your account by clicking the link.",
]
# Legit Questions
legitimate_messages = [
    "Hello, this is your friend. Can you please send me the homework?",
    "Your monthly newsletter is ready. Click the link to read it.",
    "You have a new message on your social media account. Log in to check it.",
]

# Score inital value
score = 0

while True:
    print("Welcome to the Phishing Awareness Challenge!")
    print("Is this message a phishing attempt or legitimate?")
    
    is_phishing = random.choice([True, False])
    message = random.choice(phishing_messages if is_phishing else legitimate_messages)
    
    print("\nMessage:")
    print(message)
    
    print("1. Phishing")
    print("2. Legitimate")
    user_input = input("Enter '1' or '2': ")
    
    if (is_phishing and user_input == '1') or (not is_phishing and user_input == '2'):
        print("Correct! This message is", "phishing" if is_phishing else "legitimate")
        score += 1
    else:
        print("Incorrect. This message is", "phishing" if is_phishing else "legitimate")
    
    play_again = input("Play again? (y/n): ").strip().lower()
    
    if play_again != 'y':  # Exit
        break

print(f"Your score is {score} out of messages checked.") #Display the results
