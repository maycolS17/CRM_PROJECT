from django.shortcuts import render
from core.models import Customer
from django.db.models import Max
from datetime import date, timedelta

def crm_view(request):
    customers = Customer.objects.all()
    name_query = request.GET.get("name")
    if name_query:
        customers = customers.filter(name__icontains=name_query)

    if request.GET.get("birthday") == "this_week":
        today = date.today()
        end_week = today + timedelta(days=7)
        customers = customers.filter(
            birthay__month=today.month,
            birthay__day__range=(today.day, end_week.day)
        )

    from core.models import Interaction
    latest_interactions = Interaction.objects.values('customer').annotate(latest=Max('timestamp'))

    context = {
        'customers': customers,
        'latest_interactions': {item['customer']: item['latest'] for item in latest_interactions}
    }
    return render(request, "core/crm.html", context)