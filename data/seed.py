import json

from db import Database


def seed_database(db: Database):
    """Insert sample mock if no mocks exist yet"""
    if db.get_all_mocks():
        return

    mock_id = db.create_mock(
        title="JEE Main Sample Mock #1",
        duration=180,
        marks_correct=4,
        marks_incorrect=-1,
        sections=["Physics", "Chemistry", "Maths"],
    )

    physics_questions = [
        {
            "section": "Physics",
            "type": "single",
            "text": "A particle moves along x-axis with velocity v = 3t² - 2t + 1 m/s. The acceleration at t = 2s is:",
            "options": ["A) 8 m/s²", "B) 10 m/s²", "C) 12 m/s²", "D) 14 m/s²"],
            "correct_answer": "B",
        },
        {
            "section": "Physics",
            "type": "single",
            "text": "A body of mass 2 kg is moving with velocity 10 m/s. A force of 4 N acts on it for 5 seconds. The final kinetic energy is:",
            "options": ["A) 400 J", "B) 450 J", "C) 500 J", "D) 800 J"],
            "correct_answer": "B",
        },
        {
            "section": "Physics",
            "type": "single",
            "text": "The time period of a simple pendulum on the surface of Moon (g_moon = g/6) compared to Earth is:",
            "options": ["A) √6 times", "B) 6 times", "C) 1/6 times", "D) Same"],
            "correct_answer": "A",
        },
        {
            "section": "Physics",
            "type": "single",
            "text": "Two resistors of 4Ω and 6Ω are connected in parallel. The equivalent resistance is:",
            "options": ["A) 10 Ω", "B) 2.4 Ω", "C) 5 Ω", "D) 1.2 Ω"],
            "correct_answer": "B",
        },
        {
            "section": "Physics",
            "type": "single",
            "text": "A wave has frequency 200 Hz and wavelength 1.5 m. The speed of the wave is:",
            "options": ["A) 133 m/s", "B) 200 m/s", "C) 300 m/s", "D) 150 m/s"],
            "correct_answer": "C",
        },
        {
            "section": "Physics",
            "type": "single",
            "text": "The work done in moving a charge of 2C through a potential difference of 12V is:",
            "options": ["A) 6 J", "B) 10 J", "C) 24 J", "D) 14 J"],
            "correct_answer": "C",
        },
        {
            "section": "Physics",
            "type": "single",
            "text": "Photoelectric effect is best explained by which theory of light?",
            "options": ["A) Wave theory", "B) Corpuscular theory", "C) Quantum theory", "D) Electromagnetic theory"],
            "correct_answer": "C",
        },
        {
            "section": "Physics",
            "type": "numerical",
            "text": "A ball is thrown vertically upward with velocity 20 m/s. The maximum height reached (in meters) is: (g = 10 m/s²)",
            "options": None,
            "correct_answer": "20",
        },
        {
            "section": "Physics",
            "type": "numerical",
            "text": "A 5 kg object moves in a circle of radius 2 m at 3 m/s. The centripetal force (in Newtons) is:",
            "options": None,
            "correct_answer": "22.5",
        },
        {
            "section": "Physics",
            "type": "numerical",
            "text": "The de Broglie wavelength (in nm) of an electron moving at 10⁶ m/s is approximately: (h=6.63×10⁻³⁴, m=9.1×10⁻³¹)",
            "options": None,
            "correct_answer": "0.727",
        },
    ]

    chemistry_questions = [
        {
            "section": "Chemistry",
            "type": "single",
            "text": "The hybridization of carbon in CH₄ is:",
            "options": ["A) sp", "B) sp²", "C) sp³", "D) sp³d"],
            "correct_answer": "C",
        },
        {
            "section": "Chemistry",
            "type": "single",
            "text": "Which of the following is NOT a colligative property?",
            "options": ["A) Osmotic pressure", "B) Elevation in boiling point", "C) Optical rotation", "D) Depression in freezing point"],
            "correct_answer": "C",
        },
        {
            "section": "Chemistry",
            "type": "single",
            "text": "The number of sigma bonds in ethyne (C₂H₂) is:",
            "options": ["A) 2", "B) 3", "C) 4", "D) 5"],
            "correct_answer": "B",
        },
        {
            "section": "Chemistry",
            "type": "single",
            "text": "Which quantum number determines the shape of an orbital?",
            "options": ["A) Principal (n)", "B) Azimuthal (l)", "C) Magnetic (m)", "D) Spin (s)"],
            "correct_answer": "B",
        },
        {
            "section": "Chemistry",
            "type": "single",
            "text": "pH of 0.001 M HCl solution is:",
            "options": ["A) 1", "B) 2", "C) 3", "D) 4"],
            "correct_answer": "C",
        },
        {
            "section": "Chemistry",
            "type": "single",
            "text": "The IUPAC name of CH₃-CH(OH)-CH₃ is:",
            "options": ["A) 1-propanol", "B) 2-propanol", "C) propan-1-ol", "D) methylethanol"],
            "correct_answer": "B",
        },
        {
            "section": "Chemistry",
            "type": "single",
            "text": "Which of the following has the highest electronegativity?",
            "options": ["A) Oxygen", "B) Nitrogen", "C) Fluorine", "D) Chlorine"],
            "correct_answer": "C",
        },
        {
            "section": "Chemistry",
            "type": "numerical",
            "text": "The molar mass of H₂SO₄ is (H=1, S=32, O=16):",
            "options": None,
            "correct_answer": "98",
        },
        {
            "section": "Chemistry",
            "type": "numerical",
            "text": "How many moles of NaOH are needed to neutralize 2 moles of H₂SO₄?",
            "options": None,
            "correct_answer": "4",
        },
        {
            "section": "Chemistry",
            "type": "numerical",
            "text": "The van't Hoff factor (i) for NaCl completely dissociated in water is:",
            "options": None,
            "correct_answer": "2",
        },
    ]

    maths_questions = [
        {
            "section": "Maths",
            "type": "single",
            "text": "The derivative of sin(x²) with respect to x is:",
            "options": ["A) cos(x²)", "B) 2x·cos(x²)", "C) 2·cos(x²)", "D) x·cos(x²)"],
            "correct_answer": "B",
        },
        {
            "section": "Maths",
            "type": "single",
            "text": "∫(2x + 3)dx equals:",
            "options": ["A) 2x² + 3x", "B) x² + 3x + C", "C) 2x² + 3", "D) x + 3 + C"],
            "correct_answer": "B",
        },
        {
            "section": "Maths",
            "type": "single",
            "text": "The value of lim(x→0) [sin(x)/x] is:",
            "options": ["A) 0", "B) ∞", "C) 1", "D) undefined"],
            "correct_answer": "C",
        },
        {
            "section": "Maths",
            "type": "single",
            "text": "The sum of roots of x² - 5x + 6 = 0 is:",
            "options": ["A) -5", "B) 5", "C) 6", "D) -6"],
            "correct_answer": "B",
        },
        {
            "section": "Maths",
            "type": "single",
            "text": "If A is a 2×2 matrix and det(A) = 4, then det(2A) =",
            "options": ["A) 8", "B) 12", "C) 16", "D) 32"],
            "correct_answer": "C",
        },
        {
            "section": "Maths",
            "type": "single",
            "text": "The general solution of dy/dx = y is:",
            "options": ["A) y = Ce^x", "B) y = x + C", "C) y = Ce^(-x)", "D) y = ln(x) + C"],
            "correct_answer": "A",
        },
        {
            "section": "Maths",
            "type": "single",
            "text": "In how many ways can 5 people be arranged in a row?",
            "options": ["A) 25", "B) 60", "C) 100", "D) 120"],
            "correct_answer": "D",
        },
        {
            "section": "Maths",
            "type": "numerical",
            "text": "The value of 10C3 (combination) is:",
            "options": None,
            "correct_answer": "120",
        },
        {
            "section": "Maths",
            "type": "numerical",
            "text": "If the arithmetic mean of 5, 10, 15, 20, x is 13, then x =",
            "options": None,
            "correct_answer": "15",
        },
        {
            "section": "Maths",
            "type": "numerical",
            "text": "The area (in square units) of the triangle with vertices (0,0), (4,0), (0,3) is:",
            "options": None,
            "correct_answer": "6",
        },
    ]

    all_questions = physics_questions + chemistry_questions + maths_questions
    for i, question in enumerate(all_questions):
        db.add_question(
            mock_id=mock_id,
            section=question["section"],
            type_=question["type"],
            text=question["text"],
            options=json.dumps(question["options"]) if question["options"] else None,
            correct_answer=str(question["correct_answer"]),
            order_index=i,
        )
