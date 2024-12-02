from sqlmodel import Session, select
from model import Question
from database import engine

def fetch_all_questions():
    """Fetch and print all questions from the database."""
    try:
        with Session(engine) as session:
            statement = select(Question)
            results = session.exec(statement).all()

            if not results:
                print("No questions found in the database.")
                return

            for question in results:
                print(
                    f"Course Name: {question.course_name}\n"
                    f"Question: {question.question}\n"
                    f"Option A: {question.option_a}\n"
                    f"Option B: {question.option_b}\n"
                    f"Option C: {question.option_c}\n"
                    f"Option D: {question.option_d}\n"
                    f"Correct Option: {question.correct_option}\n"
                    f"{'-'*50}\n"
                )
    except Exception as e:
        print(f"Error fetching questions: {e}")

if __name__ == "__main__":
    fetch_all_questions()
