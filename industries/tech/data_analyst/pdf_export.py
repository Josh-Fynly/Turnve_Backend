"""
PDF Portfolio Exporter

Converts portfolio data into a professional PDF report.
"""

import os
from datetime import datetime
from typing import Dict

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem,
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet


# -------------------------
# Output Directory
# -------------------------

OUTPUT_DIR = "generated_portfolios"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# -------------------------
# PDF Builder
# -------------------------

def export_portfolio_pdf(portfolio: Dict) -> str:
    """
    Generate PDF from portfolio data.
    Returns file path.
    """

    styles = getSampleStyleSheet()
    story = []

    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    # Title
    story.append(
        Paragraph(
            f"{portfolio['role']} Simulation Portfolio",
            title_style,
        )
    )

    story.append(Spacer(1, 12))

    # Summary
    summary = portfolio.get("summary", {})

    story.append(Paragraph("Summary", heading_style))
    story.append(
        Paragraph(
            f"Completed Phases: {summary.get('completed_phases', 0)}",
            body_style,
        )
    )
    story.append(
        Paragraph(
            f"Status: {summary.get('status', 'unknown')}",
            body_style,
        )
    )

    story.append(Spacer(1, 12))

    # Artifacts
    story.append(Paragraph("Artifacts", heading_style))

    for artifact in portfolio.get("artifacts", []):

        story.append(
            Paragraph(artifact.get("title", "Untitled"), body_style)
        )

        skills = artifact.get("skills_demonstrated", [])

        if skills:
            bullet_items = [
                ListItem(Paragraph(skill, body_style))
                for skill in skills
            ]

            story.append(
                ListFlowable(
                    bullet_items,
                    bulletType="bullet",
                )
            )

        story.append(Spacer(1, 12))

    # File name
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    filename = (
        f"{portfolio['role']}_portfolio_{timestamp}.pdf"
    )

    filepath = os.path.join(OUTPUT_DIR, filename)

    # Build PDF
    doc = SimpleDocTemplate(filepath, pagesize=A4)
    doc.build(story)

    return filepath
