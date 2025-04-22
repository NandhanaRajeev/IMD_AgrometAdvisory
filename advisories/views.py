# views
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from io import BytesIO
from xhtml2pdf import pisa
from .models import Advisory, AgroAdvisory
from .forms import AdvisoryForm

@login_required
def dashboard(request):
    """
    Display the advisory dashboard with a list of all advisories.
    """
    advisories = Advisory.objects.all()
    return render(request, 'advisories/dashboard.html', {
        'advisories': advisories,
        'current_date': timezone.now()
    })

@login_required
def create_advisory(request):
    """
    Handle the creation of a new advisory.
    """
    if request.method == 'POST':
        form = AdvisoryForm(request.POST)
        if form.is_valid():
            advisory = form.save(commit=False)
            advisory.created_by = request.user
            advisory.save()
            return redirect('dashboard')
    else:
        form = AdvisoryForm()
    return render(request, 'advisories/advisory_form.html', {
        'form': form,
        'title': 'Create Advisory'
    })

@login_required
def edit_advisory(request, pk):
    """
    Handle the editing of an existing advisory.
    """
    advisory = get_object_or_404(Advisory, id=pk)
    if request.method == 'POST':
        form = AdvisoryForm(request.POST, instance=advisory)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AdvisoryForm(instance=advisory)
    return render(request, 'advisories/advisory_form.html', {
        'form': form,
        'title': 'Edit Advisory',
        'advisory': advisory
    })

@login_required
def generate_pdf(request):
    """
    Generate a PDF based on selected options (district, date, bulletin number).
    """
    if request.method == 'POST':
        district = request.POST.get('district', 'Thiruvananthapuram')
        date = request.POST.get('date', timezone.now().strftime('%d.%m.%Y'))
        bulletin_number = request.POST.get('bulletin_number', 'TVM-AAS-001')

        # Sample weather data (replace with actual data source, e.g., IMD API or database)
        weather_data = {
            'rainfall': 0,
            'max_temp': '32.6-33.0',
            'min_temp': '20.5-21.2',
            'humidity': '61-93',
            'evaporation': '4.4-4.9',
            'forecast': {
                'rainfall': [0.1, 0.1, 0.2, 1.5, 1.6],
                'max_temp': [34, 34, 32, 32, 32],
                'min_temp': [23, 23, 23, 23, 23],
                'humidity_max': [63, 63, 63, 63, 75],
                'wind_speed': [6, 6, 5, 6, 6],
                'wind_dir': [270, 270, 270, 250, 250],
            },
            'cloud_cover': 4,
            'weather_summary': 'isolated',
        }

        # Fetch agro-advisories related to the latest advisory or all if none specified
        advisories = AgroAdvisory.objects.all()[:3]  # Limit to 3 for sample; adjust as needed

        context = {
            'district': district,
            'date': date,
            'bulletin_number': bulletin_number,
            'rainfall': weather_data['rainfall'],
            'max_temp': weather_data['max_temp'],
            'min_temp': weather_data['min_temp'],
            'humidity': weather_data['humidity'],
            'evaporation': weather_data['evaporation'],
            'forecast': weather_data['forecast'],
            'cloud_cover': weather_data['cloud_cover'],
            'weather_summary': weather_data['weather_summary'],
            'advisories': advisories,
            'current_year': timezone.now().year,
        }

        template = get_template('advisories/advisory_pdf.html')
        html = template.render(context)

        buffer = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=buffer)

        if pisa_status.err:
            return HttpResponse('Error generating PDF', status=500)

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="agromet_advisory_{district}_{date}.pdf"'
        return response
    else:
        return redirect('dashboard')