from django import template

register = template.Library()


@register.filter
def mediapath(value):
    """Фильтр для создания маршрута к медиа"""
    return '/media/' + str(value)


@register.simple_tag
def mediapath(value):
    """Тег для создания маршрута к медиа"""
    return '/media/' + str(value)
