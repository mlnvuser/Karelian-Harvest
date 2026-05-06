from django import template
from django.utils.translation import gettext_lazy as _

register = template.Library()

MONTHS = {
    1: _('января'),
    2: _('февраля'),
    3: _('марта'),
    4: _('апреля'),
    5: _('мая'),
    6: _('июня'),
    7: _('июля'),
    8: _('августа'),
    9: _('сентября'),
    10: _('октября'),
    11: _('ноября'),
    12: _('декабря'),
}

@register.filter
def ru_month(date, time=False):
    """Форматирует дату на русском, добавляет время, если time=True."""
    if date:
        # Форматируем дату
        formatted_date = f"{date.day} {MONTHS.get(date.month, '')} {date.year} г."

        if time:
            # Если time=True, добавляем время
            formatted_time = date.strftime("%H:%M")  # Формат времени (часы:минуты)
            return f"{formatted_date}, {formatted_time}"

        return formatted_date

    return ''


@register.filter
def reading_time(description):
    """Вычисляет время чтения на основе количества слов, где 100 слов = 1 минута,
    и склоняет слово 'минута' в зависимости от числа."""

    word_count = len(description.split())

    minutes = round(word_count / 100)

    if minutes == 0:
        return "1 минута"

    # Склоняем слово "минута" в зависимости от числа
    if 2 <= minutes <= 4:
        return f"{minutes} минуты"
    elif minutes >= 5:
        return f"{minutes} минут"
    else:
        return f"1 минута"  # Для случая, если меньше 100 слов