import pyttsx3
import speech_recognition as sr
import random
import time

class TechnicalInterviewer:
    def __init__(self):
        self.engine = pyttsx3.init()
        
        # Questions categorized by topic and difficulty
        self.questions = {
            "dsa": {
                "Easy": [
                    "Which data structure follows FIFO principle?",         # queue
                    "What search has O(1) complexity?",                     # hash
                    "Which sort compares adjacent elements?",               # bubble
                    "What data structure stores key-value pairs?",          # dictionary
                    "Which traversal visits root node first?",              # preorder
                    "What structure allows duplicate elements?",            # list
                    "Which search needs sorted array?"                      # binary
                ],
                "Medium": [
                    "Which tree has height difference of 1?",               # avl
                    "What algorithm finds shortest path?",                  # dijkstra
                    "Which sort uses pivot element?",                       # quick
                    "What balances search trees?",                         # rotation
                    "Which traversal visits leaves first?",                # postorder
                    "What detects cycles in graph?",                       # dfs
                    "Which structure implements LIFO?"                      # stack
                ],
                "Hard": [
                    "What algorithm uses dynamic programming?",             # floyd
                    "Which tree stores strings efficiently?",               # trie
                    "What structure has O(1) operations?",                  # heap
                    "Which algorithm uses greedy approach?",                # prims
                    "What detects negative cycles?",                        # bellman
                    "Which structure implements sets?",                     # hashtable
                    "What traverses graph level-wise?"                      # bfs
                ]
            },
            "web": {
                "Easy": [
                    "What defines webpage structure?",                      # html
                    "Which property changes text color?",                   # color
                    "What attribute links pages?",                         # href
                    "Which tag creates buttons?",                          # button
                    "What defines webpage styles?",                        # css
                    "Which property sets width?",                          # width
                    "What makes pages interactive?"                        # javascript
                ],
                "Medium": [
                    "What enables async operations?",                      # promises
                    "Which framework Meta created?",                       # react
                    "What manages application state?",                     # redux
                    "Which protocol secures websites?",                    # https
                    "What caches browser data?",                          # localstorage
                    "Which format transfers data?",                       # json
                    "What validates form data?"                           # validation
                ],
                "Hard": [
                    "Which hook manages state?",                          # usestate
                    "What bundles JavaScript modules?",                   # webpack
                    "Which database is document-based?",                  # mongodb
                    "What enables server-push?",                         # websockets
                    "Which runtime executes JavaScript?",                # nodejs
                    "What encrypts passwords?",                         # bcrypt
                    "Which header prevents XSS?"                        # csp
                ]
            }
        }

        # Answers for evaluation
        self.answers = {
            # DSA Easy
            "Which data structure follows FIFO principle?": "queue",
            "What search has O(1) complexity?": "hash",
            "Which sort compares adjacent elements?": "bubble",
            "What data structure stores key-value pairs?": "dictionary",
            "Which traversal visits root node first?": "preorder",
            "What structure allows duplicate elements?": "list",
            "Which search needs sorted array?": "binary",
            
            # DSA Medium
            "Which tree has height difference of 1?": "avl",
            "What algorithm finds shortest path?": "dijkstra",
            "Which sort uses pivot element?": "quick",
            "What balances search trees?": "rotation",
            "Which traversal visits leaves first?": "postorder",
            "What detects cycles in graph?": "dfs",
            "Which structure implements LIFO?": "stack",
            
            # DSA Hard
            "What algorithm uses dynamic programming?": "floyd",
            "Which tree stores strings efficiently?": "trie",
            "What structure has O(1) operations?": "heap",
            "Which algorithm uses greedy approach?": "prims",
            "What detects negative cycles?": "bellman",
            "Which structure implements sets?": "hashtable",
            "What traverses graph level-wise?": "bfs",
            
            # Web Easy
            "What defines webpage structure?": "html",
            "Which property changes text color?": "color",
            "What attribute links pages?": "href",
            "Which tag creates buttons?": "button",
            "What defines webpage styles?": "css",
            "Which property sets width?": "width",
            "What makes pages interactive?": "javascript",
            
            # Web Medium
            "What enables async operations?": "promises",
            "Which framework Meta created?": "react",
            "What manages application state?": "redux",
            "Which protocol secures websites?": "https",
            "What caches browser data?": "localstorage",
            "Which format transfers data?": "json",
            "What validates form data?": "validation",
            
            # Web Hard
            "Which hook manages state?": "usestate",
            "What bundles JavaScript modules?": "webpack",
            "Which database is document-based?": "mongodb",
            "What enables server-push?": "websockets",
            "Which runtime executes JavaScript?": "nodejs",
            "What encrypts passwords?": "bcrypt",
            "Which header prevents XSS?": "csp"
        }

    def speak(self, text: str) -> None:
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self) -> str:
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Listening for response...")
                audio = recognizer.listen(source, timeout=3)  # Reduced timeout to 3 seconds
                try:
                    response = recognizer.recognize_google(audio)
                    print(f"User said: {response}")
                    return response
                except sr.UnknownValueError:
                    return ""
                except sr.RequestError:
                    print("Couldn't connect to the speech recognition service.")
                    return ""
        except OSError as e:
            print("Microphone not available or not found.")
            return ""

    def ask_topic_preference(self):
        """Ask user which topic they would like to practice."""
        self.speak("Which topic would you like to practice? DSA or Web Development?")
        topic_response = self.listen().lower()
        
        if "dsa" in topic_response or "data" in topic_response:
            return "dsa"
        elif "web" in topic_response or "development" in topic_response:
            return "web"
        else:
            self.speak("Invalid choice. Defaulting to DSA questions.")
            return "dsa"

    def conduct_interview(self, num_questions: int, difficulty: str, topic: str):
        """Conduct the interview with topic-specific questions."""
        if difficulty not in self.questions[topic]:
            self.speak("Invalid difficulty level.")
            return

        selected_questions = random.sample(self.questions[topic][difficulty], min(num_questions, 7))

        for question in selected_questions:
            print(f"\nQuestion: {question}")
            self.speak(question)

            # 3-second pause for the user to respond
            print("Waiting for 3 seconds...")
            time.sleep(3)

            candidate_response = self.listen()

            if candidate_response:
                correct_answer = self.answers[question]
                if correct_answer.lower() == candidate_response.lower().strip():
                    self.speak("Good, well done.")
                else:
                    self.speak("No problem, coming to the next question.")
            else:
                self.speak("No problem, coming to the next question.")

    def ask_difficulty_and_num_questions(self):
        self.speak("Please choose a difficulty level: Easy, Medium, or Hard.")
        difficulty_response = self.listen().lower()

        if "easy" in difficulty_response:
            difficulty = "Easy"
        elif "medium" in difficulty_response:
            difficulty = "Medium"
        elif "hard" in difficulty_response:
            difficulty = "Hard"
        else:
            difficulty = "Easy"
            self.speak("Invalid choice. Defaulting to Easy level.") 

        num_questions = random.randint(5, 7)
        self.speak(f"I will ask you {num_questions} questions.")
        return num_questions, difficulty

def main():
    interviewer = TechnicalInterviewer() 
    
    # First ask for topic preference
    topic = interviewer.ask_topic_preference()
    
    # Then ask for difficulty and set random number of questions (5-7)
    num_questions, difficulty = interviewer.ask_difficulty_and_num_questions()
    
    # Conduct the interview with topic-specific questions
    interviewer.conduct_interview(num_questions, difficulty, topic)

if __name__ == "__main__":
    main()