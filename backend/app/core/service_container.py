"""
============================================================
SignSync Shared Service Container
============================================================

Creates ONE shared AssessmentService instance for the
application.

This is important because AssessmentHistory is currently
stored in memory.

If every router creates its own AssessmentService(),
each router gets a different AssessmentHistory instance.
"""

from app.services.assessment_service import AssessmentService


# ============================================================
# SHARED ASSESSMENT SERVICE
# ============================================================

assessment_service = AssessmentService()