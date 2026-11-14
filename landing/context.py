from django.conf import settings


def company(request):
    return {
        'company_address': settings.COMPANY_ADDRESS,
        'company_email': settings.COMPANY_EMAIL,
    }
