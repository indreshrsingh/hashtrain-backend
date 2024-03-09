from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import InvoiceForm
from .models import Invoice
from .utils import generate_pdf, upload_to_google_drive
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

import logging

logger = logging.getLogger(__name__)
@staff_member_required
def generate_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            # Save form data
            invoice_data = form.cleaned_data

            # Generate PDF content
            pdf_content = generate_pdf(invoice_data)

            # Upload PDF to Google Drive
            pdf_link = upload_to_google_drive(pdf_content, invoice_data)
            
            # Save invoice data and PDF link only if pdf_link is not None or empty
            if pdf_link:
                invoice = Invoice.objects.create(
                    customer_name=invoice_data['customer_name'],
                    training_id=invoice_data['training_id'],
                    company_name=invoice_data['company_name'],
                    training_name=invoice_data['training_name'],
                    training_description=invoice_data['training_description'],
                    pdf_link=pdf_link
                )
                
                # Redirect to success page or another view
                return redirect('invoice_detail', pk=invoice.pk)
            else:
                logger.error("PDF upload to Google Drive failed.")
                # You can render an error page or handle the error as per your requirement
                return HttpResponse("PDF upload failed. Please try again later.")
    
    # If form is not valid or PDF upload failed, render the form again
    form = InvoiceForm()
    return render(request, 'invoice_form.html', {'form': form})
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'invoice_detail.html', {'invoice': invoice})
