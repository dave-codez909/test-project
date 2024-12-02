from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum
from pydantic import BaseModel

# Enum for storing the correct answer option
class CorrectOption(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"

# Model to represent each multiple-choice question
class Question(SQLModel, table=True):
    """
    Represents a multiple-choice question.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    course_name: str = Field(index=True, max_length=100)
    question: str = Field(max_length=1000)
    option_a: str = Field(max_length=200)
    option_b: str = Field(max_length=200)
    option_c: str = Field(max_length=200)
    option_d: str = Field(max_length=200)
    correct_option: CorrectOption

# Model to represent a test that a user takes
class Test(SQLModel, table=True):
    """
    Represents a test taken by a user.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)  # Foreign key to the user who took the test
    course_name: str = Field(max_length=100)
    score: Optional[int] = Field(default=None, ge=0, le=30)  # Score should be between 0 and 30

# Model to capture a user's answer during test submission
class UserAnswer(BaseModel):
    question_id: int
    user_option: str
