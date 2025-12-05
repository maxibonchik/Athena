from django import template

register = template.Library()

@register.filter
def get_field_label(form, field_prefix):
    """Получить label поля формы по префиксу"""
    field_name = f"{field_prefix}"
    if hasattr(form, field_name):
        return form[field_name].label
    return ""

@register.filter
def get_field_choices(form, field_prefix):
    """Получить choices поля формы по префиксу"""
    field_name = f"{field_prefix}"
    if hasattr(form, field_name):
        return form[field_name].field.choices
    return []
