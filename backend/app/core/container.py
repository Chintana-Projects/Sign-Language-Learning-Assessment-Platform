from app.services.assessment_service import AssessmentService

from app.services.instructor.instructor_dashboard_service import InstructorDashboardService
assessment_service = AssessmentService()
instructor_dashboard_service = InstructorDashboardService(
    assessment_service.learner_profile_service
)

print("\n========== CONTAINER CREATED ==========")

print(
    "Assessment Service ID:",
    id(assessment_service)
)

print(
    "Session Service ID:",
    id(assessment_service.session_service)
)

print("=======================================\n")