from dataclasses import dataclass
from typing import Optional


@dataclass
class Question:
    id: str
    mock_id: str
    section: str
    type: str
    text: str
    options: Optional[list[str]]
    correct_answer: str | list[str] | float
    order_index: int


@dataclass
class Mock:
    id: str
    title: str
    duration_minutes: int
    marks_correct: float
    marks_incorrect: float
    sections: list[str]
    created_at: str
    source: str


@dataclass
class AttemptAnswer:
    answer: Optional[str | list[str] | float]
    time_spent_seconds: int
    marked_for_review: bool


@dataclass
class AttemptResult:
    attempt_id: str
    total_score: float
    max_score: float
    correct_count: int
    wrong_count: int
    unattempted_count: int
    section_breakdown: dict
    answers: dict
