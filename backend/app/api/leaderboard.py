from fastapi import APIRouter

from app.services.learner.learner_profile_service import (
    LearnerProfileService
)

router = APIRouter(
    prefix="/leaderboard",
    tags=["Leaderboard"]
)

# Create service instance
learner_profile_service = (
    LearnerProfileService()
)


@router.get("/stats")
def leaderboard_stats():

    profiles = (
        learner_profile_service
        .get_all_profiles()
    )

    stats = {
        "Beginner": 0,
        "Intermediate": 0,
        "Advanced": 0,
        "Professional": 0
    }

    for profile in profiles:

        level = profile.get(
            "certification_level",
            "Beginner"
        )

        if level not in stats:
            stats[level] = 0

        stats[level] += 1

    return stats

@router.get("/overview")
def leaderboard_overview():

    profiles = learner_profile_service.get_all_profiles()

    total_students = len(profiles)

    certified_students = len([
        p for p in profiles
        if p.get("certificate_id")
    ])

    avg_accuracy = round(
        sum(
            p.get("overall_accuracy", 0)
            for p in profiles
        ) / max(total_students, 1),
        2
    )

    top_score = max(
        [
            p.get("overall_accuracy", 0)
            for p in profiles
        ],
        default=0
    )

    return {
        "total_students": total_students,
        "certified_students": certified_students,
        "average_accuracy": avg_accuracy,
        "top_score": top_score
    }
@router.get("/recent")
def recent_certifications():

    profiles = (
        learner_profile_service
        .get_all_profiles()
    )

    certified = []

    for profile in profiles:

        if profile.get("certificate_id"):

            certified.append({
                "student_id": profile.get(
                    "student_id"
                ),
                "certification_level": profile.get(
                    "certification_level"
                ),
                "certificate_id": profile.get(
                    "certificate_id"
                )
            })

    return certified[-10:]