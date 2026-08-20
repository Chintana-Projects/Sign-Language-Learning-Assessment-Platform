import json
import uuid

from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER


class ReportGenerator:
    """
    Generates Assessment Reports.

    Supports:
    - JSON Report
    - PDF Report
    - Excel Report (Future)
    """

    def __init__(
        self,
        analytics,
        student_id="Unknown"
    ):

        self.analytics = analytics
        self.student_id = student_id

    # -------------------------------------------------
    # Generate Report Object
    # -------------------------------------------------

    def generate_json(self):

        report = {

            "report_id":
                f"RPT-{str(uuid.uuid4())[:8].upper()}",

            "student_id":
                self.student_id,

            "generated_at":
                datetime.now().isoformat(),

            "report_type":
                "Sign Language Assessment Report",

            "summary":
                self.analytics
        }

        return report

    # -------------------------------------------------
    # Save JSON
    # -------------------------------------------------

    def save_json(
        self,
        filename="assessment_report.json"
    ):

        report = self.generate_json()

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4
            )

        return filename

    # -------------------------------------------------
    # Save PDF
    # -------------------------------------------------

    def save_pdf(
        self,
        filename="assessment_report.pdf"
    ):

        report = self.generate_json()

        document = SimpleDocTemplate(filename)

        styles = getSampleStyleSheet()

        title_style = styles["Title"]
        title_style.alignment = TA_CENTER

        heading = styles["Heading2"]

        normal = styles["BodyText"]

        elements = []

        # ==========================================
        # TITLE
        # ==========================================

        elements.append(
            Paragraph(
                "SignSync Assessment Report",
                title_style
            )
        )

        elements.append(Spacer(1, 20))

        # ==========================================
        # REPORT DETAILS TABLE
        # ==========================================

        report_table = Table(

            [

                ["Report ID", report["report_id"]],

                ["Student ID", report["student_id"]],

                ["Generated At", report["generated_at"]],

                ["Report Type", report["report_type"]]

            ],

            colWidths=[140, 330]

        )

        report_table.setStyle(

            TableStyle([

                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#1E3A8A")),

                ("TEXTCOLOR", (0, 0), (0, -1), colors.white),

                ("BACKGROUND", (1, 0), (1, -1), colors.whitesmoke),

                ("GRID", (0, 0), (-1, -1), 1, colors.grey),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

                ("TOPPADDING", (0, 0), (-1, -1), 8)

            ])

        )

        elements.append(report_table)

        elements.append(Spacer(1, 20))

        summary = report["summary"]

        # ==========================================
        # SUMMARY
        # ==========================================

        elements.append(
            Paragraph(
                "Assessment Summary",
                heading
            )
        )

        summary_data = [

            ["Metric", "Value"]

        ]

        for key, value in summary.items():

            if key in [

                "alphabet_scores",
                "recent_history"

            ]:
                continue

            summary_data.append([

                key.replace("_", " ").title(),

                str(value)

            ])

        summary_table = Table(

            summary_data,

            colWidths=[250, 220]

        )

        summary_table.setStyle(

            TableStyle([

                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563EB")),

                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("GRID", (0, 0), (-1, -1), 1, colors.grey),

                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

                ("TOPPADDING", (0, 0), (-1, -1), 8)

            ])

        )

        elements.append(summary_table)

        elements.append(Spacer(1, 20))

        # ==========================================
        # ALPHABET PERFORMANCE
        # ==========================================

        elements.append(
            Paragraph(
                "Alphabet Performance",
                heading
            )
        )

        alphabet_data = [

            ["Alphabet", "Accuracy (%)"]

        ]

        for letter, score in summary["alphabet_scores"].items():

            alphabet_data.append([

                letter,

                f"{score}%"

            ])

        alphabet_table = Table(

            alphabet_data,

            colWidths=[150, 150]

        )

        alphabet_table.setStyle(

            TableStyle([

                ("BACKGROUND", (0, 0), (-1, 0), colors.green),

                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("GRID", (0, 0), (-1, -1), 1, colors.grey),

                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke)

            ])

        )

        elements.append(alphabet_table)

        elements.append(Spacer(1, 20))

        # ==========================================
        # RECENT ATTEMPTS
        # ==========================================

        elements.append(

            Paragraph(

                "Recent Attempts",

                heading

            )

        )

        attempt_data = [

            [

                "Expected",

                "Predicted",

                "Confidence",

                "Correct"

            ]

        ]

        for attempt in summary["recent_history"]:

            attempt_data.append([

                attempt["expected_alphabet"],

                attempt["predicted_alphabet"],

                f"{round(attempt['confidence'] * 100, 2)}%",

                "Yes" if attempt["correct"] else "No"

            ])

        attempts_table = Table(

            attempt_data,

            colWidths=[80, 80, 120, 80]

        )

        attempts_table.setStyle(

            TableStyle([

                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("GRID", (0, 0), (-1, -1), 1, colors.grey),

                ("BACKGROUND", (0, 1), (-1, -1), colors.lavender)

            ])

        )

        elements.append(attempts_table)

        elements.append(Spacer(1, 30))

        # ==========================================
        # FOOTER
        # ==========================================

        elements.append(

            Paragraph(

                "<b>Generated Automatically by SignSync AI Learning Platform</b>",

                normal

            )

        )

        document.build(elements)

        return filename