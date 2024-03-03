from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(invoice_data):
    # Construct filename based on customer name and training name
    filename = f"{invoice_data['customer_name']}-{invoice_data['training_name']}-invoice.pdf"
    
    # Create a response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Create a canvas
    p = canvas.Canvas(response, pagesize=letter)
    
    # Define fonts and styles
    p.setFont("Helvetica", 12)
    
    # Set initial y coordinate
    y = 750
    
    # Write invoice details
    p.drawString(50, y, "Invoice for: " + invoice_data['customer_name'])
    y -= 20
    p.drawString(50, y, "Training ID: " + str(invoice_data['training_id']))
    y -= 20
    p.drawString(50, y, "Company Name: " + invoice_data['company_name'])
    y -= 20
    p.drawString(50, y, "Training Name: " + invoice_data['training_name'])
    y -= 20
    p.drawString(50, y, "Training Description: " + invoice_data['training_description'])
    y -= 20
    
    # Draw a line
    y -= 20
    p.line(50, y, 550, y)

    # Add more drawing for other fields
    
    # Save the PDF
    p.showPage()
    p.save()
    
    return response
