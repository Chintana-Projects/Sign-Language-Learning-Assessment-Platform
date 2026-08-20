from datetime import datetime


class AnalyticsDashboard:
    """
    Generates student progress dashboard.
    Combines:
    - Attempt history
    - Accuracy analysis
    - Performance statistics
    """


    def __init__(self, analyzer, attempts):
        """
        analyzer:
            Object responsible for generating performance reports

        attempts:
            List containing student's practice attempts
        """

        self.analyzer = analyzer
        self.attempts = attempts



    # -------------------------------------
    # Recent practice history
    # -------------------------------------

    def recent_history(self, limit=10):

        return self.attempts[-limit:]



    # -------------------------------------
    # Generate dashboard
    # -------------------------------------

    def generate(self):

        report = self.analyzer.generate_report()


        return {

            "success": True,

            "dashboard_generated_at":
                datetime.now().isoformat(),


            "performance": {

                "total_practice_attempts":
                    report.get("total_attempts", 0),


                "accuracy_percentage":
                    report.get("accuracy", 0),


                "average_confidence":
                    report.get("average_confidence", 0)

            },


            "alphabet_analysis": {

                "strongest_alphabets":
                    report.get(
                        "strongest_alphabets",
                        []
                    ),


                "weakest_alphabets":
                    report.get(
                        "weakest_alphabets",
                        []
                    ),


                "most_mistaken_alphabets":
                    report.get(
                        "most_mistaken",
                        []
                    )

            },


            "recent_practice_history":
                self.recent_history()

        }