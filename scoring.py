import json
from models import AttemptAnswer, AttemptResult


def _value_from_question(question, key):
    return question.get(key) if isinstance(question, dict) else getattr(question, key)


def _normal_answer(value):
    if value in (None, "", []):
        return None
    return value


def _parse_correct(question_type, value):
    if question_type == "multiple":
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            text = value.strip()
            if text.startswith("["):
                try:
                    return json.loads(text)
                except Exception:
                    return []
            return [part.strip() for part in text.split(",") if part.strip()]
    if question_type == "numerical":
        try:
            return float(value)
        except Exception:
            return None
    return str(value)


def calculate_score(questions, answers, marks_correct, marks_incorrect) -> AttemptResult:
    total_score = 0.0
    max_score = float(marks_correct) * len(questions)
    correct_count = 0
    wrong_count = 0
    unattempted_count = 0
    not_visited_count = 0
    section_breakdown = {}
    answer_results = {}

    for question in questions:
        qid = _value_from_question(question, "id")
        section = _value_from_question(question, "section")
        qtype = _value_from_question(question, "type")
        correct = _parse_correct(qtype, _value_from_question(question, "correct_answer"))
        raw_info = answers.get(qid, {}) if isinstance(answers, dict) else {}
        if isinstance(raw_info, dict):
            answer = _normal_answer(raw_info.get("answer"))
            time_spent = int(raw_info.get("time_spent_seconds", raw_info.get("time_spent", 0)) or 0)
            marked = bool(raw_info.get("marked_for_review", False))
            status = raw_info.get("status", "visited" if (time_spent > 0 or answer is not None) else "not_visited")
        else:
            answer = _normal_answer(raw_info)
            time_spent = 0
            marked = False
            status = "visited" if answer is not None else "not_visited"

        if section not in section_breakdown:
            section_breakdown[section] = {
                "score": 0.0,
                "correct": 0,
                "wrong": 0,
                "unattempted": 0,
                "not_visited": 0,
                "attempted": 0,
                "total": 0,
                "accuracy": 0.0,
            }
        breakdown = section_breakdown[section]
        breakdown["total"] += 1

        question_score = 0.0
        was_correct = False
        was_wrong = False
        was_not_visited = (status == "not_visited")

        if answer is None:
            if was_not_visited:
                not_visited_count += 1
                breakdown["not_visited"] += 1
            else:
                unattempted_count += 1
                breakdown["unattempted"] += 1
        elif qtype == "single":
            if str(answer) == str(correct):
                question_score = float(marks_correct)
                was_correct = True
            else:
                question_score = float(marks_incorrect)
                was_wrong = True
        elif qtype == "multiple":
            answer_set = set(answer if isinstance(answer, list) else [answer])
            correct_set = set(correct if isinstance(correct, list) else [correct])
            if answer_set == correct_set:
                question_score = float(marks_correct)
                was_correct = True
            elif answer_set and answer_set.issubset(correct_set):
                question_score = 0.0
            else:
                question_score = float(marks_incorrect)
                was_wrong = True
        elif qtype == "numerical":
            try:
                numeric_answer = float(answer)
                if correct is not None and abs(numeric_answer - float(correct)) <= 0.01:
                    question_score = float(marks_correct)
                    was_correct = True
                else:
                    question_score = float(marks_incorrect)
                    was_wrong = True
            except Exception:
                question_score = float(marks_incorrect)
                was_wrong = True

        if answer is not None:
            breakdown["attempted"] += 1
        if was_correct:
            correct_count += 1
            breakdown["correct"] += 1
        if was_wrong:
            wrong_count += 1
            breakdown["wrong"] += 1

        total_score += question_score
        breakdown["score"] += question_score
        denominator = breakdown["correct"] + breakdown["wrong"]
        breakdown["accuracy"] = (breakdown["correct"] / denominator * 100) if denominator else 0.0
        answer_results[qid] = AttemptAnswer(answer, time_spent, marked, status)

    return AttemptResult(
        attempt_id="",
        total_score=round(total_score, 2),
        max_score=round(max_score, 2),
        correct_count=correct_count,
        wrong_count=wrong_count,
        unattempted_count=unattempted_count,
        not_visited_count=not_visited_count,
        section_breakdown=section_breakdown,
        answers=answer_results,
    )
