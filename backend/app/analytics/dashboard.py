from fastapi import APIRouter

from app.services.analytics.analytics_service import AnalyticsDashboard
from app.analytics.recommendation_engine import RecommendationEngine


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# Temporary in-memory data
# Later we connect database/session storage

practice_attempts = []


class DummyAnalyzer:

    def generate_report(self):

        return {

            "total_attempts": 30,

            "accuracy": 76.6,

            "average_confidence": 42.2,

            "strongest_alphabets": [
                "B",
                "A"
            ],

            "weakest_alphabets": [
                "C"
            ],

            "most_mistaken": [
                {
                    "letter": "C",
                    "confused_with": "F",
                    "count": 16
                }
            ]

        }



@router.get("/")
def get_dashboard():

    analyzer = DummyAnalyzer()


    dashboard = AnalyticsDashboard(
        analyzer,
        practice_attempts
    )


    return dashboard.generate()