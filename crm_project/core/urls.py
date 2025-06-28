from django.urls import path
from .views import crm_view

urlpatterns = [
    path('crm/', crm_view, name='crm'),
    path('', crm_view, name='home'),
]
