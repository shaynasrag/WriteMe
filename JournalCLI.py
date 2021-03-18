from Journal import Journal
from Exceptions import IncorrectResponse

class JournalCLI():
    def __init__(self):
        self._journal = Journal()
        self._name = None
        self._choices = {
            "add submission": self._create_submission,
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
            
    def _create_submission(self):
        new_submission = Submission()
        self._check_temperature()
        person = self._show_people()
        discuss = True
        while discuss:
            new_entry = self._create_entry(person)
            new_submission.add_entry(person, new_entry)
            cont = input("Would you like to discuss another relationship? Yes or No. \n")
            if (cont.lower() == "no"):
                discuss = False
                print("It's important to remember that having anxious tendencies doesn't make you a bad person or unworthy of love.\nYou can have a secure relationship regardless of your inidividual insecurity score.\nRelationship security is earned through actions and behaviors that build both partners up and bring out the best in them.\nHaving a high insecurity score just means that you might encounter more challenges.\n")
                next = print("Thank you so much for working to understand yourself better and to work toward healthier and fulfilling relationships with the people in your life. See you next time! Type anything to complete this submission")
        self._journal.add_submission(new_submission)



    def _check_stats(self):
        pass
    
    def _quit(self):
        sys.exit(0)
    
    def _check_temperature(self):

        response = input("Hi {0}, how are you today? Great or Not Great".format(self._name))

        if response.lower() == "great":
            print("I'm glad to hear it! Let's get started.")
        elif response.lower() == "not great":
            print("I'm sorry to hear you're not feeling so great. Maybe our work together will help us today. Let's get started.")
        else:
            raise IncorrectResponse()
    
    def _show_people(self):
        for i in self._journal._people:
            print(i + '\n')

        print("New Person\n")
        choice = input("Please select who you would like to journal about today: ")
        if choice in self._journal._people:
            return person
        elif choice == "New Person":
            person = input("Please enter the name of the new person you would like to add to your journal")
        else:
            raise IncorrectResponse()
    
    def _create_entry(self, person):
        new_entry = Entry()
        new_entry.add_person(person)
        communal_strength = input("Great Choice! How close are you feeling to {0} today?\nClose, Not So Close, Distanced".format(person))
        new_entry.add_communal_strength(communal_strength)
        if communal_strength == "Close":
            anxiety = input("I'm glad to hear things are going well with {0}! To what extend have you been feeling anxiety in the relationship?".format(person))
        else:
            anxiety = input("I'm sorry to hear that you're feeling this way. To what extend have you been feeling anxiety in the relationship?")
        new_entry.add_anxiety(anxiety)

        talk_conflict = input("Would you like to talk about a conflict you've experienced recently with {0}?".format(person))
        if entry._talk_about_conflict(talk_conflict):
            conflict_description = input("Conflicts can come in all shapes and sizes.\nPlease describe the conflict you've been experiencing and how it's been making you feel.\n")
            new_entry.add_conflict(conflict_description)
            space = input("Wow, that sounds like it's been really hard for you.\nI definitely understand why you've been feeling some anxiety in the relationship, and I think it's important that we first take a moment to accept that feeling.\nLet me know when you've taken a moment to give yourself space for this.\n")
            addressed = input("Thank you for allowing yourself some space for self-compassion. Have you addressed this conflict with {0}?Yes or No\n".format(person))
            if new_entry._addressed_conflict(addressed):
                how_addressed = input("I'm glad to hear it! In your own words, how has the conflict been addressed?\n")
                new_entry.add_addressed(how_addressed)
                consent = input("I'm glad you took steps to resolve this conflict. Let's talk about your process in terms of healthy communication.\nDid you ask for consent from {0} before approaching the conflict?\n(Yes or No)\n".format(person))
                new_entry._consent(consent)
                self_soothe1 = input("Next, did you take steps to physically soothe yourself? Yes or No\n")
                new_entry.add_self_soothe1(self_soothe1)
                other_soothe1 = input("How about {0}. Did they take steps to physically soothe you? Yes or No\n".format(person))
                new_entry.add_other_soothe1(other_soothe1)
                self_soothe2 = input("Let's talk emotionally. Did you take steps to soothe yourself, emotionally? Yes or No\n")
                new_entry.add_self_soothe2(self_soothe2)
                other_soothe2 = input("And finally, how about {0}. Did they take steps to soothe you, relationally? (1 for yes, 0 for no)\n".format(person))
                new_entry.add_other_soothe2(self_soothe2)
                print("Remember, when you are close to someone, what you do or say around that person makes an impact, whether positive or negative.\nYour healthy communication score this time with {0} is {1}".format(person, new_entry._communication_score))
                print("Effective, health communication is possible for you, and developing these skills can help you develop and build trust and safety with {0}.".format(person))
            else:
                next_steps = input("That's okay, you'll get there. What steps can you take to feel more secure with {0}?\n".format(person))
                new_entry._steps_to_secure(next_steps)

            print("Let's remember that if you've acted unpleasantly, you're not doing it on purpose. You're just expressing yourself in a way that's familiar to you and trying to get your needs met.")
            print("Self compassion may be unfamiliar because you've learned to condemn, criticize, or judge yourself when you learn something you don't like about yourself.\nLet's zoom in on how you reacted to the conflict between you and {0}.".format(person))
            filler = input("Zoom in on yourself during your conflict and repeat one or more of the following phrases:\nI see how you suffer just as anyone else does.\nMay you be happy.\nMay you be free from pain.\nAnything else that the you in the scene needs to hear in order to know that this difficulty is seen and acknowledged.\nLet me know when you're done.\n")
            
            appreciate_person = input("When it comes to anxious attachments, sometimes conflicts can overwhelm our sense of stability in the relationship.\nWe can ground ourselves through gratitude. What is one thing you appreciate about {0}?\n".format(person))
            new_entry.add_appreciate_other(appreciate_person)
            appreciate_self = input("We still need to keep in mind self-compassion. What is one thing you appreciate about yourself today?\n")
            new_entry.add_appreciate_self(appreciate_self)
        else:
            gratitude = input("Sometimes it's important to take the time to focus on the positive. Tell me more about the importance of this relationship in your life and why you're grateful for it.\n".format(person))
            new_entry.add_gratitude(gratitude)
        
        return new_entry




        