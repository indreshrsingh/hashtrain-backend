from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from .forms import InvoiceForm
from .utils import generate_pdf

@staff_member_required
def generate_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            # Save form data
            invoice_data = form.cleaned_data
            form.save()
            # Generate PDF
            pdf = generate_pdf(invoice_data)
            return pdf
    else:
        form = InvoiceForm()
    return render(request, 'invoice_form.html', {'form': form})
