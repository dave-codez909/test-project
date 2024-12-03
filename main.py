from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import select
from sqlalchemy.orm import Session
from sqlalchemy import func
from model import Question, Test, UserAnswer
from database import get_session, init_db, engine

app = FastAPI()

# Initialize the database on startup
@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/questions/{course_name}")
def get_questions(course_name: str, session: Session = Depends(get_session)):
    # Fetching questions for a specific course, grouped by course_name
    statement = select(Question).where(Question.course_name.ilike(course_name))
    results = session.execute(statement).scalars().all()

    if not results:
        raise HTTPException(status_code=404, detail=f"No questions found for course '{course_name}'")
    
    # Grouping questions under each course name
    return {"course_name": course_name, "questions": [
        {
            "id": q.id,
            "question": q.question,
            "option_a": q.option_a,
            "option_b": q.option_b,
            "option_c": q.option_c,
            "option_d": q.option_d,
            "correct_option": q.correct_option
        }
        for q in results
    ]}

@app.post("/start-test")
async def start_test(course_name: str):
    with Session(engine) as session:
        # Fetch questions for the specified course
        statement = select(Question).where(func.lower(Question.course_name) == course_name.lower())
        results = session.execute(statement).scalars().all()

        if not results:
            raise HTTPException(status_code=404, detail="No questions found for the given course.")
        
        # Return questions without the 'correct_option' field
        return {"questions": [
            {
                "id": q.id,
                "course_name": q.course_name,
                "question": q.question,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d
            }
            for q in results
        ]}


@app.post("/submit-answers")
async def submit_answers(answers: list[UserAnswer]):
    with Session(engine) as session:
        results = []
        for answer in answers:
            # Fetch the question by ID
            question = session.get(Question, answer.question_id)
            if not question:
                results.append({"question_id": answer.question_id, "error": "Question not found"})
                continue
            
            # Compare the user's answer with the correct option
            is_correct = question.correct_option == answer.user_option.upper()
            results.append({
                "question_id": question.id,
                "correct": is_correct,
                "correct_option": question.correct_option if not is_correct else None,
            })
        
        return {"results": results}

@app.get("/test-history/{user_id}")
def get_test_history(user_id: int, session: Session = Depends(get_session)):
    statement = select(Test).where(Test.user_id == user_id)
    results = session.execute(statement).scalars().all()
    if not results:
        raise HTTPException(status_code=404, detail=f"No test history found for user '{user_id}'")
    return results

@app.get("/debug/questions")
def debug_questions(session: Session = Depends(get_session)):
    statement = select(Question)
    results = session.execute(statement).scalars().all()
    if not results:
        return {"message": "No questions found in the database"}
    return {"total_questions": len(results), "questions": [
        {
            "id": q.id,
            "question": q.question,
            "option_a": q.option_a,
            "option_b": q.option_b,
            "option_c": q.option_c,
            "option_d": q.option_d,
            "correct_option": q.correct_option
        }
        for q in results
    ]}
