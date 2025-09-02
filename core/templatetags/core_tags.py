"""
Custom template filters for the core application.
"""

from django import template

register = template.Library()


@register.filter
def lookup(dictionary, key):
    """
    Template filter to lookup dictionary values by key.
    Usage: {{ dict|lookup:key }}
    """
    if dictionary and hasattr(dictionary, 'get'):
        return dictionary.get(key, '')
    return ''


@register.filter
def get_item(dictionary, key):
    """
    Alternative template filter for dictionary lookup.
    Usage: {{ dict|get_item:key }}
    """
    return dictionary.get(key) if dictionary else None


@register.filter
def format_choice_field(value):
    """
    Format choice field values for better display.
    Replaces underscores with spaces and capitalizes words.
    """
    if not value:
        return value
    return str(value).replace('_', ' ').title()


@register.simple_tag
def url_replace(request, field, value):
    """
    Template tag to generate URLs with modified query parameters.
    Preserves existing parameters while updating specific ones.
    """
    query_dict = request.GET.copy()
    query_dict[field] = value
    return query_dict.urlencode()


@register.simple_tag
def url_remove(request, field):
    """
    Template tag to generate URLs with a parameter removed.
    """
    query_dict = request.GET.copy()
    if field in query_dict:
        del query_dict[field]
    return query_dict.urlencode()


@register.inclusion_tag('core/includes/table_header.html', takes_context=True)
def table_header(context, field_name, display_name, current_sort=None):
    """
    Inclusion tag for sortable table headers.
    """
    if current_sort == field_name:
        sort_direction = 'asc'
        next_sort = f'-{field_name}'
        icon = 'fas fa-sort-up'
    elif current_sort == f'-{field_name}':
        sort_direction = 'desc'
        next_sort = field_name
        icon = 'fas fa-sort-down'
    else:
        sort_direction = None
        next_sort = field_name
        icon = 'fas fa-sort'
    
    return {
        'field_name': field_name,
        'display_name': display_name,
        'next_sort': next_sort,
        'sort_direction': sort_direction,
        'icon': icon,
        'request': context.get('request'),  # Pass request from parent context
    }
