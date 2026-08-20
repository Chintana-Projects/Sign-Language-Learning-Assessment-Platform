from datetime import datetime


class AnalyticsDashboard:
    """
    Formats analytics data for frontend dashboard.
    """


    def __init__(self, analytics_service, attempts):

        self.analytics_service = analytics_service
        self.attempts = attempts


    # -------------------------------------
    # Generate Dashboard
    # -------------------------------------

    def generate(self):

        analytics = self.analytics_service.generate_dashboard(
            self.attempts
        )


        return {

            "success": True,

            "dashboard_generated_at":
                datetime.now().isoformat(),

            "analytics":
                analytics

        }