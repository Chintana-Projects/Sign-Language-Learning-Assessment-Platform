from app.assessment.sign_score import SignScoreCalculator


calculator = SignScoreCalculator()


result = calculator.calculate(
    correct=True,
    confidence=0.85,
    stability=90,
    time_taken=2
)


print(result)