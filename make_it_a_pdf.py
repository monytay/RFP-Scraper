from web_scrape import scrape_job
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime, timedelta
import os

REPORT_PATH = "jobs_report.pdf"

def build_pdf():
    # ---- Remove the old report if it's older than 1 week ----
    if os.path.exists(REPORT_PATH):
        modified_time = datetime.fromtimestamp(os.path.getmtime(REPORT_PATH))
        age = datetime.now() - modified_time

        if age > timedelta(weeks=1):
            os.remove(REPORT_PATH)
            print(f"Old report ({age.days} days old) removed.")
        else:
            print(f"Existing report is only {age.days} day(s) old — keeping it for now.")

    # ---- Register custom fonts ----
    pdfmetrics.registerFont(TTFont("Montserrat-Bold", "fonts/Montserrat-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("Montserrat-Regular", "fonts/Montserrat-Regular.ttf"))

    # ---- Colors ----
    DARK_BLUE = colors.HexColor("#0B1F3A")
    LIGHT_BLUE_TINT = colors.HexColor("#E8EDF5")

    # ---- Get the data ----
    jobs = scrape_job()

    # ---- Timestamp used in the footer ----
    generated_on = datetime.now().strftime('%d %B %Y, %H:%M')

    # ---- Styles ----
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle", parent=styles["Title"],
        fontName="Montserrat-Bold", fontSize=24, textColor=DARK_BLUE, spaceAfter=20
    )
    summary_style = ParagraphStyle(
        "SummaryStyle", parent=styles["Normal"],
        fontName="Montserrat-Regular", fontSize=11, textColor=DARK_BLUE, spaceAfter=4
    )
    cell_style = ParagraphStyle(
        "CellStyle", parent=styles["BodyText"],
        fontName="Helvetica", fontSize=8, leading=10, textColor=DARK_BLUE
    )

    # ---- Build summary stats ----
    total_jobs = len(jobs)
    countries = set(j["location"] for j in jobs)
    orgs = {}
    for j in jobs:
        orgs[j["organization"]] = orgs.get(j["organization"], 0) + 1

    # ---- Assemble the document content (the "story") ----
    story = []

    story.append(Paragraph("ReliefWeb Jobs Report", title_style))

    story.append(Paragraph(f"<b>Total matching jobs:</b> {total_jobs}", summary_style))
    story.append(Paragraph(f"<b>Unique locations:</b> {len(countries)}", summary_style))
    orgs_text = ", ".join(f"{name} ({count})" for name, count in orgs.items())
    story.append(Paragraph(f"<b>Organizations:</b> {orgs_text}", summary_style))
    story.append(Spacer(1, 20))

    # ---- Build the table ----
    table_data = [["Title", "Location", "Organization", "Posted", "Closing", "Link"]]

    for job in jobs:
        table_data.append([
            Paragraph(job["title"], cell_style),
            Paragraph(job["location"], cell_style),
            Paragraph(job["organization"], cell_style),
            job["posted"],
            job["closing date"],
            Paragraph(f'<link href="{job["link"]}"><font color="#0B1F3A"><u>View</u></font></link>', cell_style),
        ])

    table = Table(table_data, repeatRows=1, colWidths=[130, 70, 80, 55, 55, 40])

    table_style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Montserrat-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, DARK_BLUE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ])

    for i in range(1, len(table_data)):
        if i % 2 == 0:
            table_style.add("BACKGROUND", (0, i), (-1, i), LIGHT_BLUE_TINT)

    table.setStyle(table_style)
    story.append(table)

    # ---- Footer: "Generated on..." + page number, both bottom-right ----
    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(DARK_BLUE)

        # "Generated on..." sits slightly above the page number
        canvas.drawRightString(letter[0] - 40, 34, f"Generated on {generated_on}")
        # Page number sits at the very bottom
        canvas.drawRightString(letter[0] - 40, 20, f"Page {doc.page}")

        canvas.restoreState()

    # ---- Build the PDF ----
    doc = SimpleDocTemplate(REPORT_PATH, pagesize=letter, topMargin=40, bottomMargin=50)
    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)

    print(f"PDF created: {REPORT_PATH} ({total_jobs} jobs)")

if __name__ == "__main__":
    build_pdf()