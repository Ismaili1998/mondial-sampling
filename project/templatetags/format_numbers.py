from django import template
import locale

register = template.Library()

@register.filter
def thousand_separator(value):
    if not value:
        return '' 

    # Set the desired locale
    locale.setlocale(locale.LC_ALL, 'de_DE.utf8')

    # Format the number with dot as the thousand separator and comma as the decimal separator
    return locale.format_string('%.2f', value, grouping=True)
