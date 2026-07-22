from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import tempfile


def create_pdf_report(insights):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    doc = SimpleDocTemplate(temp_file.name)
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>InsightPilot AI</b>", styles["Title"]))
    story.append(Paragraph("AI Business Analytics Report", styles["Heading2"]))
    story.append(Paragraph("<br/><br/>", styles["Normal"]))

    for line in insights.split("\n"):
        if line.strip():
            story.append(Paragraph(line, styles["BodyText"]))

    doc.build(story)

    return temp_file.name