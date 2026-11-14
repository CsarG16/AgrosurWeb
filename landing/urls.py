from django.urls import path
from . import views

app_name = 'landing'

urlpatterns = [
    path('', views.index, name='index'),
    path('productos/', views.productos_view, name='productos'),
    path('cotizador/', views.cotizador_view, name='cotizador'),
    path('nosotros/', views.nosotros_view, name='nosotros'),
    path('calidad/', views.calidad_view, name='calidad'),
    path('cotizacion/<uuid:token>/pdf/', views.quote_pdf, name='quote_pdf'),
    path('api/contact/', views.submit_contact, name='submit_contact'),
    path('api/quote/', views.submit_quote, name='submit_quote'),
    path('api/quote/estimate/', views.quote_estimate, name='quote_estimate'),
]
