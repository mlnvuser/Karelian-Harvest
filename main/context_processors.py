from .models import ContactInformation

def contact_info(request):
    """Добавляет контакты во все шаблоны сайта"""
    try:
        contact = ContactInformation.get_info()
    except Exception:
        contact = None

    return {'contact': contact}
