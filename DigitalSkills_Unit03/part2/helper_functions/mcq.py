from IPython.display import HTML
import json


class MCQ:
    """A class to hold the definitions of a multiple choice quiz."""

    div_counter = 0  # class based counter for divs to avoid id collision on the images to be moved around if multiple quizzes

    def __init__(
        self, question: str, option_dict: dict, check_selected_only=True
    ) -> str:
        """creates a html/ javascript multiple choice quiz

        Args:
            question (str): A string based question that the multiple choice options will refer to
            option_dict (dict): A list of dictionary items showing the options, if they are correct and any optional feedback
            check_selected_only (bool, optional): A boolean flag as to whether only ticked items should be marked or all items. Defaults to True.

        Returns:
            str: html/javascript combination for rendering the quiz
        """
        self.question = json.dumps(question)
        self.options = json.dumps(option_dict)
        self.CSO = json.dumps(check_selected_only)
        MCQ.div_counter += 1

    def quiz(self):
        quiz = f"quiz-container-{MCQ.div_counter}"
        html = f"""
        <style>
        #{quiz} {{
            font-family: Arial, sans-serif;
        }}

        .form-check {{
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 5px;
        }}

        .is-correct {{
            border: 2px solid #198754;
            background-color: #d1e7dd;
            color: #0f5132;
        }}

        .is-incorrect {{
            border: 2px solid #dc3545;
            background-color: #f8d7da;
            color: #842029;
        }}

        .feedback {{
            margin-top: 5px;
            font-size: 14px;
        }}

        .correct {{
            color: #198754;
        }}

        .incorrect {{
            color: #dc3545;
        }}

        .quiz-button {{
            margin-top: 15px;
            padding: 8px 15px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }}

        .quiz-button:hover {{
            background-color: #0056b3;
        }}
        </style>

        <div id="{quiz}"></div>

        <script>
        (function() {{
        const quizQuestion = {self.question};
        const quizData = {self.options};
        const CHECK_SELECTED_ONLY = {self.CSO};

        const container = document.getElementById('{quiz}');
        const form = document.createElement('form');
        form.id = 'quizForm';

        const intro = document.createElement('div');
        intro.innerHTML = quizQuestion;
        container.appendChild(intro);

        quizData.forEach((item, index) => {{
            const formCheck = document.createElement('div');
            formCheck.className = 'form-check';

            const input = document.createElement('input');
            input.className = 'form-check-input';
            input.type = 'checkbox';
            input.name = `{quiz}-answer-${{index}}`;
            input.id = `{quiz}-answer-${{index}}`;
            input.dataset.correct = item.correct;

            const label = document.createElement('label');
            label.className = 'form-check-label';
            label.htmlFor = `{quiz}-answer-${{index}}`;
            label.textContent = item.text;

            const feedback = document.createElement('div');
            feedback.className = 'feedback';
            feedback.id = `{quiz}-feedback-${{index}}`;

            formCheck.appendChild(input);
            formCheck.appendChild(label);
            formCheck.appendChild(feedback);
            form.appendChild(formCheck);
        }});

        const button = document.createElement('button');
        button.type = 'submit';
        button.className = 'quiz-button';
        button.textContent = 'Check Answers';
        form.appendChild(button);

        container.appendChild(form);

        form.addEventListener('submit', function (e) {{
            e.preventDefault();

            form.querySelectorAll('.form-check').forEach(div => {{
            div.classList.remove('is-correct', 'is-incorrect');
            }});

            quizData.forEach((item, index) => {{
            const checkbox = document.querySelector(`#{quiz}-answer-${{index}}`);
            const feedback = document.querySelector(`#{quiz}-feedback-${{index}}`);
            const parent = checkbox.closest('.form-check');

            const isChecked = checkbox.checked;
            const isCorrect = checkbox.dataset.correct === "true";
            if (CHECK_SELECTED_ONLY) {{ 
            if (isChecked) {{ 
                let message = isCorrect === isChecked ? "✅ Correct" : "❌ Incorrect";

                if (isCorrect === isChecked && item.feedbackCorrect) {{
                message += ` — ${{item.feedbackCorrect}}`;
                }} else if (isCorrect !== isChecked && item.feedbackIncorrect) {{
                message += ` — ${{item.feedbackIncorrect}}`;
                }}

                feedback.textContent = message;
                parent.classList.add(isCorrect === isChecked ? 'is-correct' : 'is-incorrect');
            }} else {{
                feedback.textContent = '';
            }}
            }} else {{ 
            let message = isCorrect === isChecked ? "✅ Correct" : "❌ Incorrect";

            if (isCorrect === isChecked && item.feedbackCorrect) {{
                message += ` — ${{item.feedbackCorrect}}`;
            }} else if (isCorrect !== isChecked && item.feedbackIncorrect) {{
                message += ` — ${{item.feedbackIncorrect}}`;
            }}

            feedback.textContent = message;
            parent.classList.add(isCorrect === isChecked ? 'is-correct' : 'is-incorrect');
            }}
            }});
        }});
        }})();
        </script>
        """
        return HTML(html)


def mcq_1():
    """Creates a simple mcq question.  The question text is defined and then the options_dict is defined as a list of dictionary
    objects. For each option provide a text for the option and a boolean value to the correct field indicating if the answer is correct
    There are optional feedbackCorrect and feedbackIncorrect fields that can be defined for feedback displayed on submission.
    When we create the quiz we can also pass an optional third boolean argument as to whether to mark only options that are ticked as true (default)
    or show feedback on all options

    Returns:
        HTML:HTML rendering of the quiz
    """

    question = "<p><strong>Analyse the code in the previous cell.  What is the cause of the error?</strong><p>"

    options_dict = [
        {
            "text": "The dictionary is the incorrect length",
            "correct": False,
            "feedbackIncorrect": "The length of the dictionary does nto matter",
        },
        {
            "text": "The dictionary does not contain an entry with a key equal to Vietnam",
            "correct": True,
            "feedbackIncorrect": "Yes! The entry for Vietnam is missing",
        },
        {
            "text": "The dictionary does not contain an entry with a value equal to Vietnam",
            "correct": False,
            "feedbackIncorrect": "The error message tells you the error is with the missing key",
        },        
        ]

    quiz = MCQ(question, options_dict)
    return quiz.quiz()

def mcq_2():
    """Creates a simple mcq question.  The question text is defined and then the options_dict is defined as a list of dictionary
    objects. For each option provide a text for the option and a boolean value to the correct field indicating if the answer is correct
    There are optional feedbackCorrect and feedbackIncorrect fields that can be defined for feedback displayed on submission.
    When we create the quiz we can also pass an optional third boolean argument as to whether to mark only options that are ticked as true (default)
    or show feedback on all options

    Returns:
        HTML:HTML rendering of the quiz
    """

    question = "<p><strong>Analyse the code in the previous cell.  What is the cause of the error?</strong><p>"

    options_dict = [
        {
            "text": "There are a different number of x and y values",
            "correct": True,
            "feedbackCorrect": "Yes we need the same number of x and y values in a scatter plot",
        },
        {
            "text": "The x values are an array",
            "correct": False,
            "feedbackCorrect": "We are able to use arrays in plots",
        },
         {
            "text": "The axes are incorrectly defined",
            "correct": False,
            "feedbackCorrect": "You have defined the axes correctly",
        },
        
         
    ]

    quiz = MCQ(question, options_dict)
    return quiz.quiz()

def mcq_3():
    """Creates a simple mcq question.  The question text is defined and then the options_dict is defined as a list of dictionary
    objects. For each option provide a text for the option and a boolean value to the correct field indicating if the answer is correct
    There are optional feedbackCorrect and feedbackIncorrect fields that can be defined for feedback displayed on submission.
    When we create the quiz we can also pass an optional third boolean argument as to whether to mark only options that are ticked as true (default)
    or show feedback on all options

    Returns:
        HTML:HTML rendering of the quiz
    """

    question = "<p><strong>Analyse the code in the previous cell.  Which one of the following is correct?</strong><p>"

    options_dict = [
        {
            "text": "The capital city is the key and the value is the country",
            "correct": False,
            "feedbackIncorrect": "No! The capital city is the value and the key is the country",
        },
        {
            "text": "The country is the key and the capital city is the value",
            "correct": True,
            "feedbackCorrect": "Yes! The country is the key and the capital city is the value   ",
        },
            {
                "text": "The country and capital city are both keys",
                "correct": False,
                "feedbackIncorrect": "No! The country is the key and the capital city is the value   ",
            },
            {
                "text": "The country and capital city are both values",
                "correct": False,
                "feedbackIncorrect": "No! The country is the key and the capital city is the value   ",
            }
        
         
    ]

    quiz = MCQ(question, options_dict)
    return quiz.quiz()
