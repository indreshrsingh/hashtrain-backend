# utils.py
from urllib.parse import urljoin
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseUpload
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, ensure to delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
CREDENTIALS_PATH = "credentials.json"

from google.auth.transport.requests import Request as GoogleRequest

# Other imports and code...
folder_id = "1Y0SPZtxWZPDTfqibm0BGy6NLGAokKkBp"
def upload_to_google_drive(pdf_content, invoice_data):
    creds = None
    # Check if token.json exists
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(GoogleRequest())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.getenv("CRED") , SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save credentials for next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # Build Drive API service
    service = build("drive", "v3", credentials=creds)

    # Create file metadata with parent folder ID
    file_metadata = {
        'name': f"{invoice_data['customer_name']}-{invoice_data['training_name']}-invoice.pdf",
        'parents':[folder_id],
        'supportsAllDrives': True

    }

    # Upload PDF to Google Drive
    media = MediaIoBaseUpload(io.BytesIO(pdf_content), mimetype='application/pdf')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # Check if file creation was successful
    if file:
        # Get link to the uploaded file
        base_url = "https://drive.google.com/file/d/"
        pdf_link = urljoin(base_url, f"{file['id']}/view")
        return pdf_link
    else:
        # Handle case where file creation failed
        return "https://drive.google.com/"


from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.lib.units import inch

def generate_pdf(invoice_data):
    # Create a PDF document
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    heading_style = styles['Heading2']
    body_style = styles['BodyText']

    # Create elements
    elements = []

    # Title
    title = Paragraph("Invoice", title_style)
    elements.append(title)
    elements.append(Paragraph("<br/>" * 2, body_style))  # Add some vertical space

    # Customer Name
    customer_name = Paragraph("<b>Customer Name:</b> " + invoice_data['customer_name'], body_style)
    elements.append(customer_name)

    # Training ID
    training_id = Paragraph("<b>Training ID:</b> " + str(invoice_data['training_id']), body_style)
    elements.append(training_id)

    # Company Name
    company_name = Paragraph("<b>Company Name:</b> " + invoice_data['company_name'], body_style)
    elements.append(company_name)

    # Training Name
    training_name = Paragraph("<b>Training Name:</b> " + invoice_data['training_name'], heading_style)
    elements.append(training_name)

    # Training Description
    training_description = Paragraph("<b>Training Description:</b> " + invoice_data['training_description'], body_style)
    elements.append(training_description)

    # Build the PDF document
    doc.build(elements)

    # Get the PDF content from the buffer
    pdf_content = buffer.getvalue()
    buffer.close()

    return pdf_content
