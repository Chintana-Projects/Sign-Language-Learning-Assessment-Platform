
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle,
)
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
)


class ExportService:

    def __init__(self, report_service):
        self.report_service = report_service

    # ============================================================
    # HELPER - FORMAT PERCENTAGE
    # ============================================================

    def _format_percentage(self, value, decimals=1):

        try:
            value = float(value)

            # Convert 0-1 values into percentages
            if 0 <= value <= 1:
                value *= 100

            value = max(0.0, min(100.0, value))

            return f"{value:.{decimals}f}%"

        except (TypeError, ValueError):
            return "0.0%"

    # ============================================================
    # HELPER - CREATE TABLE STYLE
    # ============================================================

    def _base_table_style(self, header_background="#EEF2FF"):

        return TableStyle([

            # Header
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor(header_background),
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.HexColor("#111827"),
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold",
            ),

            (
                "ALIGN",
                (0, 0),
                (-1, 0),
                "CENTER",
            ),

            # Body
            (
                "FONTNAME",
                (0, 1),
                (-1, -1),
                "Helvetica",
            ),

            (
                "TEXTCOLOR",
                (0, 1),
                (-1, -1),
                colors.HexColor("#374151"),
            ),

            # Grid
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#D1D5DB"),
            ),

            # Padding
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7,
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7,
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                8,
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                8,
            ),

            # Vertical alignment
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE",
            ),
        ])

    # ============================================================
    # EXPORT STUDENT REPORT AS PDF
    # ============================================================

    def generate_student_report_pdf(
        self,
        student_id: str,
    ):

        # ========================================================
        # GET REPORT DATA
        # ========================================================

        report = self.report_service.get_student_report(
            student_id
        )

        if not report or not report.get("success"):
            return None

        # ========================================================
        # PDF BUFFER
        # ========================================================

        buffer = BytesIO()

        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,

            rightMargin=20 * mm,
            leftMargin=20 * mm,
            topMargin=18 * mm,
            bottomMargin=18 * mm,
        )

        # ========================================================
        # STYLES
        # ========================================================

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
            fontSize=21,
            leading=25,
            textColor=colors.HexColor("#111827"),
            spaceAfter=6,
        )

        subtitle_style = ParagraphStyle(
            "ReportSubtitle",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            fontSize=9.5,
            leading=12,
            textColor=colors.HexColor("#6B7280"),
            spaceAfter=18,
        )

        heading_style = ParagraphStyle(
            "SectionHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=17,
            textColor=colors.HexColor("#111827"),
            spaceBefore=14,
            spaceAfter=8,
        )

        normal_style = ParagraphStyle(
            "ReportNormal",
            parent=styles["Normal"],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#374151"),
        )

        small_style = ParagraphStyle(
            "SmallText",
            parent=styles["Normal"],
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#6B7280"),
        )

        # ========================================================
        # STORY
        # ========================================================

        story = []

        # ========================================================
        # TITLE
        # ========================================================

        story.append(
            Paragraph(
                "SignSync - Student Learning Report",
                title_style,
            )
        )

        story.append(
            Paragraph(
                f"Student ID: {student_id}",
                subtitle_style,
            )
        )

        # ========================================================
        # SUMMARY DATA
        # ========================================================

        summary = report.get(
            "summary",
            {},
        )

        story.append(
            Paragraph(
                "Learning Summary",
                heading_style,
            )
        )

        summary_data = [

            [
                "Metric",
                "Value",
            ],

            [
                "Total Attempts",
                str(
                    summary.get(
                        "total_attempts",
                        0,
                    )
                ),
            ],

            [
                "Correct Attempts",
                str(
                    summary.get(
                        "correct_attempts",
                        0,
                    )
                ),
            ],

            [
                "Incorrect Attempts",
                str(
                    summary.get(
                        "incorrect_attempts",
                        0,
                    )
                ),
            ],

            [
                "Accuracy",
                self._format_percentage(
                    summary.get(
                        "accuracy",
                        0,
                    ),
                    decimals=1,
                ),
            ],

            [
                "Average Confidence",
                self._format_percentage(
                    summary.get(
                        "average_confidence",
                        0,
                    ),
                    decimals=1,
                ),
            ],

            [
                "Average Score",
                str(
                    summary.get(
                        "average_score",
                        0,
                    )
                ),
            ],
        ]

        summary_table = Table(
            summary_data,
            colWidths=[
                105 * mm,
                65 * mm,
            ],
            repeatRows=1,
        )

        summary_table.setStyle(
            self._base_table_style()
        )

        # Align values
        summary_table.setStyle(
            TableStyle([
                (
                    "ALIGN",
                    (1, 1),
                    (1, -1),
                    "CENTER",
                ),
            ])
        )

        story.append(summary_table)

        # ========================================================
        # LETTERS PRACTICED
        # ========================================================

        story.append(
            Paragraph(
                "Letters Practiced",
                heading_style,
            )
        )

        letters = report.get(
            "letters_practiced",
            [],
        )

        if letters:

            letters_text = ", ".join(
                str(letter)
                for letter in letters
            )

        else:

            letters_text = (
                "No letters practiced yet."
            )

        letters_box = Table(
            [
                [
                    Paragraph(
                        letters_text,
                        normal_style,
                    )
                ]
            ],
            colWidths=[
                170 * mm
            ],
        )

        letters_box.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#F9FAFB"),
                ),

                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#D1D5DB"),
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
            ])
        )

        story.append(letters_box)

        # ========================================================
        # LETTERS TO IMPROVE
        # ========================================================

        story.append(
            Paragraph(
                "Letters to Improve",
                heading_style,
            )
        )

        weak_letters = report.get(
            "weak_letters",
            [],
        )

        if weak_letters:

            weak_data = [
                [
                    "Letter",
                    "Attempts",
                    "Correct",
                    "Accuracy",
                ]
            ]

            for item in weak_letters:

                accuracy = self._format_percentage(
                    item.get(
                        "accuracy",
                        0,
                    ),
                    decimals=1,
                )

                weak_data.append([
                    str(
                        item.get(
                            "letter",
                            "",
                        )
                    ),

                    str(
                        item.get(
                            "attempts",
                            0,
                        )
                    ),

                    str(
                        item.get(
                            "correct",
                            0,
                        )
                    ),

                    accuracy,
                ])

            weak_table = Table(
                weak_data,
                colWidths=[
                    42.5 * mm,
                    42.5 * mm,
                    42.5 * mm,
                    42.5 * mm,
                ],
                repeatRows=1,
            )

            weak_table.setStyle(
                self._base_table_style(
                    "#FEF3C7"
                )
            )

            weak_table.setStyle(
                TableStyle([

                    (
                        "ALIGN",
                        (0, 1),
                        (-1, -1),
                        "CENTER",
                    ),

                    (
                        "TEXTCOLOR",
                        (3, 1),
                        (3, -1),
                        colors.HexColor("#92400E"),
                    ),
                ])
            )

            story.append(
                weak_table
            )

        else:

            story.append(
                Paragraph(
                    "Great job! No weak letters found.",
                    normal_style,
                )
            )

        # ========================================================
        # RECENT PRACTICE ATTEMPTS
        # ========================================================

        story.append(
            Paragraph(
                "Recent Practice Attempts",
                heading_style,
            )
        )

        recent_attempts = report.get(
            "recent_attempts",
            [],
        )

        if recent_attempts:

            attempts_data = [
                [
                    "Expected",
                    "Predicted",
                    "Result",
                    "Confidence",
                ]
            ]

            for attempt in recent_attempts:

                confidence = attempt.get(
                    "confidence",
                    0,
                )

                confidence_text = (
                    self._format_percentage(
                        confidence,
                        decimals=1,
                    )
                )

                result = (
                    "Correct"
                    if attempt.get(
                        "correct",
                        False,
                    )
                    else "Incorrect"
                )

                attempts_data.append([
                    str(
                        attempt.get(
                            "expected",
                            "-",
                        )
                    ),

                    str(
                        attempt.get(
                            "predicted",
                            "-",
                        )
                    ),

                    result,

                    confidence_text,
                ])

            attempts_table = Table(
                attempts_data,
                colWidths=[
                    42.5 * mm,
                    42.5 * mm,
                    42.5 * mm,
                    42.5 * mm,
                ],
                repeatRows=1,
            )

            attempts_table.setStyle(
                self._base_table_style()
            )

            attempts_table.setStyle(
                TableStyle([

                    (
                        "ALIGN",
                        (0, 1),
                        (-1, -1),
                        "CENTER",
                    ),

                    (
                        "TEXTCOLOR",
                        (2, 1),
                        (2, -1),
                        colors.HexColor("#374151"),
                    ),
                ])
            )

            # Correct / incorrect row formatting
            for row_index, attempt in enumerate(
                recent_attempts,
                start=1,
            ):

                if attempt.get(
                    "correct",
                    False,
                ):

                    attempts_table.setStyle(
                        TableStyle([
                            (
                                "TEXTCOLOR",
                                (2, row_index),
                                (2, row_index),
                                colors.HexColor("#166534"),
                            ),
                            (
                                "FONTNAME",
                                (2, row_index),
                                (2, row_index),
                                "Helvetica-Bold",
                            ),
                        ])
                    )

                else:

                    attempts_table.setStyle(
                        TableStyle([
                            (
                                "TEXTCOLOR",
                                (2, row_index),
                                (2, row_index),
                                colors.HexColor("#B91C1C"),
                            ),
                            (
                                "FONTNAME",
                                (2, row_index),
                                (2, row_index),
                                "Helvetica-Bold",
                            ),
                        ])
                    )

            story.append(
                attempts_table
            )

        else:

            story.append(
                Paragraph(
                    "No recent attempts found.",
                    normal_style,
                )
            )

        # ========================================================
        # REPORT FOOTER
        # ========================================================

        story.append(
            Spacer(
                1,
                22,
            )
        )

        footer_table = Table(
            [
                [
                    Paragraph(
                        "Generated by SignSync",
                        small_style,
                    )
                ]
            ],
            colWidths=[
                170 * mm
            ],
        )

        footer_table.setStyle(
            TableStyle([
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER",
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),

                (
                    "LINEABOVE",
                    (0, 0),
                    (-1, 0),
                    0.5,
                    colors.HexColor("#E5E7EB"),
                ),
            ])
        )

        story.append(
            footer_table
        )

        # ========================================================
        # BUILD PDF
        # ========================================================

        document.build(
            story
        )

        buffer.seek(0)

        return buffer

