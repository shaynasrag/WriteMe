from Journal import Journal

class JournalCLI():
    def __init__(self):
        self._journal = Journal()
        self._name = None
        self._choices = {
            "add submission": self._add_submission,
            "check stats": self._check_stats,
            "quit": self._quit,
        }

    def _display_menu(self):
        if self._name = None:
            print("Hi! What's your name?")
            self._name = input()
        else:
            print("Hi {0}, what would you like to do today?".format(self._name))
        options = ", ".join(self._choices.keys())
        print(options)

    def run(self):
        while True:
            self._display_menu()
            choice = input(">")
            action = self._choices.get(choice)
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))
            
    def _add_submission(self):
        pass

    def _check_stats(self):
        pass
    
    def _quit(self):
        sys.exit(0)





def main():
    intro = input("Hi Shayna, how are you today? great, or not so great?\n")
    if (intro == "great"):
        print("I'm glad to hear it! Let's get started.")
    else:
        print("I'm sorry to hear you're not feeling so great. Maybe our work together will help us today. Let's get started")
    person = input("Which relationship would you like to reflect on, today?\n")
    analysis = True
    while (analysis == True):
        communal_strength = int(input("Great choice! On a scale of 1-5, what do you feel is your communal strength with {0}?\n".format(person)))
        if (communal_strength >= 4):
            anxiety = int(input("Wow, I'm glad to hear things are going well with {0} this week.\nOn a scale of 1-10, to what extent have you felt anxiety this week in this relationship?\n".format(person)))
        elif (communal_strength < 3):
            anxiety = int(input("I'm sorry to hear that things feel hard with {0} this week.\nOn a scale of 1-10, to what extent have you felt anxiety this week in this relationship?\n".format(person)))
        if (anxiety > 0):
            conflict_description = input("Conflicts can come in all shapes and sizes.\nPlease describe the conflict you've been experiencing and how it's been making you feel.\n")
            space = input("Wow, that sounds like it's been really hard for you.\nI definitely understand why you've been feeling some anxiety in the relationship, and I think it's important that we first take a moment to accept that feeling.\nLet me know when you've taken a moment to give yourself space for this.\n")
            addressed = input("Thank you for allowing yourself some space for self-compassion. Have you addressed this conflict?\n")
            if (addressed == "yes"):
                how_addressed = input("I'm glad to hear it! In your own words, how has the conflict been addressed?\n")
                healthy_communication = int(input("I'm glad you took steps to resolve this conflict. Let's talk about your process in terms of healthy communication.\nDid you ask for consent from {0} before approaching the conflict?\n(1 for yes, 0 for no)\n".format(person)))
                healthy_communication += int(input("Next, did you take steps to physically soothe yourself? (1 for yes, 0 for no)\n"))
                healthy_communication += int(input("How about {0}. Did they take steps to physically soothe you? (1 for yes, 0 for no)\n".format(person)))
                healthy_communication += int(input("Let's talk relationally. Did you take steps to soothe yourself, relationally? (1 for yes, 0 for no)\n"))
                healthy_communication += int(input("And finally, how about {0}. Did they take steps to soothe you, relationally? (1 for yes, 0 for no)\n".format(person)))
                print("Remember, when you are close to someone, what you do or say around that person makes an impact, whether positive or negative.\nYour healthy communication score this week with {0} is {1}".format(person, healthy_communication))
                print("Effective, health communication is possible for you, and developing these skills can help you develop and build trust and safety with {0}.".format(person))
            else:
                next_steps = input("That's okay, you'll get there. What steps can you take to feel more secure with {0}?\n".format(person))
            print("Let's remember that if you've acted unpleasantly, you're not doing it on purpose. You're just expressing yourself in a way that's familiar to you and trying to get your needs met.")
            print("Yes, self compassion is unfamiliar because you've learned to condemn, criticize, or judge yourself when you learn something you don't like about yourself.\nLet's zoom in on how you reacted to the conflict between you and {0}.".format(person))
            filler = input("Zoom in on yourself during your conflict and repeat one or more of the following phrases:\nI see how you suffer just as anyone else does.\nMay you be happy.\nMay you be free from pain.\nAnything else that the you in the scene needs to hear in order to know that this difficulty is seen and acknowledged.\nLet me know when you're done.\n")
            
            appreciate_person = input("When it comes to anxious attachments, sometimes conflicts can overwhelm our sense of stability in the relationship.\nWe can ground ourselves through gratitude. What is one thing you appreciate about {0}?\n".format(person))
            appreciate_self = input("We still need to keep in mind self-compassion. What is one thing you appreciate about yourself today?\n")
        else:
            gratitude = input("I'm glad to hear things are going well with {0} this week! Tell me more about the importance of this relationship in your life and why you're grateful for it.\n".format(person))
            cont = input("Would you like to discuss another relationship? yes or no. \n")
            if (cont == "yes"):
                person = input("Which relationship would you like to reflect on next?\n")
            else:
                analysis = False
                print("It's important to remember that having anxious tendencies doesn't make you a bad person or unworthy of love.\nYou can have a secure relationship regardless of your inidividual insecurity score.\nRelationship security is earned through actions and behaviors that build both partners up and bring out the best in them.\nHaving a high insecurity score just means that you might encounter more challenges.\n")
                print("Thank you so much for working to understand yourself better and to work toward healthier and fulfilling relationships with the people in your life. See you next week!")
                return
