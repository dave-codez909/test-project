import csv
import logging
from sqlmodel import Session
from model import Question, CorrectOption
from database import engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def import_csv_to_db(csv_file_path: str):
    """Import questions from a CSV file into the database."""
    try:
        with open(csv_file_path, mode="r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            with Session(engine) as session:
                for row in csv_reader:
                    # Validate required columns
                    required_columns = {"Language", "Level", "Question", "Option A", "Option B", "Option C", "Option D", "Correct Option"}
                    if not required_columns.issubset(row.keys()):
                        logger.warning(f"Row skipped due to missing columns: {row}")
                        continue
                    
                    # Ensure that the 'Correct Option' is valid
                    try:
                        correct_option = CorrectOption(row["Correct Option"])
                    except ValueError:
                        logger.warning(f"Invalid 'Correct Option' in row: {row}")
                        continue
                    
                    # Map CSV fields to the Question model
                    question = Question(
                        course_name=row["Language"],  # Map 'Language' to 'course_name'
                        question=row["Question"],  # Map 'Question' to 'question'
                        option_a=row["Option A"],
                        option_b=row["Option B"],
                        option_c=row["Option C"],
                        option_d=row["Option D"],
                        correct_option=correct_option
                    )
                    session.add(question)
                session.commit()
                logger.info(f"CSV data successfully imported from {csv_file_path}.")
    except Exception as e:
        logger.error(f"Error importing CSV data: {e}")

if __name__ == "__main__":
    csv_file_path = "programming_mc_questions_updated.csv"  # Update with your actual CSV file path
    import_csv_to_db(csv_file_path)
