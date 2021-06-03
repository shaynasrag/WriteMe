from Exceptions import IncorrectResponse
import Entry

text_dict = {
        "greeting_new": "Hi! What's your name?\n>",
        "greeting_old": "Hi REPLACE, what would you like to do today?",
        "topic": "What best describes what you would like to talk about right now?\nI am experiencing an...",
        "select person": "Please select who you would like to journal about today (If you would like to add a new person, type 'New Person'):",
        "new person": "Please enter the name of the new person you would like to add to your journal:\n>",
        "person exists": "You have written about REPLACE before. Would you like your submission to be about REPLACE or would you like to start again?",
        "another relationship": "Would you like to discuss another relationship? Yes or No.\n>",
        "not another relationship": "It's important to remember that having anxious tendencies doesn't make you a bad person or unworthy of love.\nSecure relationships are possible for you.\n Relationship security is earned through actions and behaviors that build both partners up and bring out the best in them.\nYou may just have more challenges in this space to overcome than others.\nThank you so much for working to understand yourself better and to work toward healthier and fulfilling relationships with the people in your life. See you next time! Type anything to return to the submission menu.\n>",
        "closeness": "How close are you feeling to REPLACE today?\nOptions: Close, Not So Close, Distanced\n>",
        "not valid": "REPLACE is not a valid choice",
        "options/start again": "Options: REPLACE, Start Again\n>",
        "wrong/start again": "Please type either REPLACE or 'Start Again'",
        "glad to hear": "I'm glad to hear things are going well with REPLACE!",
        "sorry to hear": "I'm sorry to hear that you're feeling this way about REPLACE.\nHopefully our work together can make a positive impact on your relationship.",
        "anxiety": "To what extent have you been feeling anxiety in the relationship?\nOptions: High Anxiety, Mid Anxiety, Low Anxiety, No Anxiety\n>",
        "conflict": "Would you like to talk about a conflict you've experienced recently with REPLACE?\nOptions: Yes or No\n>",
        "conflict description": "Conflicts can come in all shapes and sizes.\nPlease describe the conflict you've been experiencing and how it's been making you feel.\n>",
        "space": "Wow, that sounds like it's been really hard for you.\nI definitely understand why you've been feeling some anxiety in the relationship, and I think it's important that we first take a moment to accept that feeling.\nLet me know when you've taken a moment to give yourself space for this.\n>",
        "addressed": "Thank you for allowing yourself some space for self-compassion. Have you addressed this conflict with REPLACE?\nOptions: Yes or No\n>",
        "how addressed": "I'm glad to hear it! In your own words, how has the conflict been addressed?\n>",
        "consent": "I'm glad you took steps to resolve this conflict. Let's talk about your process in terms of healthy communication.\nDid you ask for consent from REPLACE before approaching the conflict?\nOptions: Yes or No\n>",
        "self soothe1": "Next, did you take steps to physically/emotionally soothe yourself?\nOptions: Yes or No\n>",
        "other soothe1": "How about REPLACE. Did you take steps to physically/emotionally soothe each other?\nOptions: Yes or No\n>",
        "communication score": "Remember, when you are close to someone, what you do or say around that person makes an impact, whether positive or negative.\nYour healthy communication score this time with is REPLACE/3. Type anything to continue\n>",
        "effective communication": "Effective, health communication is possible for you, and developing these skills can help you develop and build trust and safety with REPLACE. Type anything to continue\n>",
        "how to begin": "Would you like to brainstorm ways to go about this conflict with REPLACE?\nOptions: Yes or No>",
        "how to approach": "An important aspect of healthy communication is asking consent from REPLACE and allowing both of you the space to address this conflict in the way that is safe for both of you.\n What is one way you could ask consent from REPLACE before entering in this conversation?\n>",
        "their side": "We've already talked about what your experience of the conflict has been. Let's take a moment to think about REPLACE's side of the conflict.\nCan you try to explain what you think is going on with REPLACE in relation to this conflict?\nPerhaps REPLACE doesn't know that there is a conflict, or perhaps this has been bothering them as well. Take a moment to describe what their perspective may be.\n>",
        "health communication": "Thank you for taking the time to empathize with REPLACE's perspective. Empathy is one of the tools you can use to ensure that this conflict can be resolved in a healthy and safe manner.\nBefore we focus on what exactly you might be able to say, let's remember some healthy communication techniques:\n1) Use I-language\n2) Focus on one problem at a time\n3) Make sure to stay in touch with your physical and emotional responses and make sure you feel safe during the conversation\n4) Pay attention to REPLACE's physical and emotional comfort.\n5) Take a temporary break from the conversation if you need to",
        "how to frame": "What is another way you can make sure to have a safe and productive conflict resolution with REPLACE?\n>",
        "intended": "Now that we've brainstormed a bit about how to approach REPLACE about the conflict, what would you like to say to them to resolve it? Keep in mind the empathy and healthy communication practices mentioned previously.\n>",
        "next steps": "That's okay, you'll get there at whatever time is right for you. What steps can you take to feel more secure with REPLACE?\n>",
        "support": "Experiencing a strain in one relationship can sometimes feel destabilizing. It's important that you exercise self compassion in seeking support from others. Where do you feel like you can get support right now?\n>",
        "self compassion": "Let's remember that if you've acted unpleasantly, you're not doing it on purpose. You're just expressing yourself in a way that's familiar to you and trying to get your needs met.\nType anything to continue.\n>Self compassion may be unfamiliar because you've learned to condemn, criticize, or judge yourself when you learn something you don't like about yourself.\nLet's zoom in on how you reacted to the conflict between you and REPLACE.\nZoom in on yourself during your conflict and repeat one or more of the following phrases:\nI see how you suffer just as anyone else does.\nMay you be happy.\nMay you be free from pain.\nAnything else that the you in the scene needs to hear in order to know that this difficulty is seen and acknowledged.\n",
        "appreciate person": "When it comes to anxious attachments, sometimes conflicts can overwhelm our sense of stability in the relationship.\nWe can ground ourselves through gratitude. What is one thing you appreciate about REPLACE?\n>",
        "appreciate self": "We still need to keep in mind self-compassion. What is one thing you appreciate about yourself today?\n>",
        "gratitude": "Finally, sometimes it's important to take the time to focus on the positive. Tell me more about the importance of your relationship with REPLACE and why you're grateful for it.\n>"
    }

def print_error(e):
    print("Please choose from the following choices: ") 
    for choice in e._choices:
        print(choice)

def print_text(key, toReplace=None):
    string = text_dict[key]
    if toReplace:
        altered = string.replace("REPLACE", toReplace)
        string = altered
    print(string)

def get_input(key, toReplace=None):
    string = text_dict[key]
    if toReplace:
        altered = string.replace("REPLACE", toReplace)
        string = altered
    text = input(string)
    return text

def validate(validator, input_string, input_placeholder=None):
    while True:
        try:
            response = get_input(input_string, input_placeholder)
            valid = validator(response)
            break
        except IncorrectResponse as e:
            print_error(e)

    return True if valid else False

def add_and_commit(session, add_list):
    for thingToAdd in add_list:
        session.add(thingToAdd)
    session.commit() 
