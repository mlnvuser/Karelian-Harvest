from .models import ContactInformation

def contact_info(request):
    return {
        'contact': ContactInformation.get_info()
    }
