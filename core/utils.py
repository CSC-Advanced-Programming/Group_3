"""
Utility functions and mixins for core application.
Provides common functionality for filtering, searching, and pagination.
"""

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class SearchFilterMixin:
    """
    Mixin to add search and filter functionality to ListView classes.
    Follows SoC principle by separating search/filter logic from view logic.
    """
    search_fields = []  # Fields to search in
    filter_fields = {}  # Fields to filter by with their choices
    items_per_page = 10  # Default pagination
    sortable_fields = []  # Fields that can be sorted
    
    def get_search_query(self):
        """Extract search query from request parameters."""
        return self.request.GET.get('search', '').strip()
    
    def get_filter_params(self):
        """Extract filter parameters from request."""
        filters = {}
        for field_name in self.filter_fields.keys():
            value = self.request.GET.get(field_name, '').strip()
            if value:
                filters[field_name] = value
        return filters
    
    def get_sort_param(self):
        """Extract sort parameter from request."""
        sort_param = self.request.GET.get('sort', '').strip()
        # Validate sort parameter against allowed fields
        if sort_param:
            field_name = sort_param.lstrip('-')
            if field_name in self.sortable_fields:
                return sort_param
        return None
    
    def get_items_per_page(self):
        """Get items per page from request, with validation."""
        try:
            per_page = int(self.request.GET.get('per_page', self.items_per_page))
            # Limit to reasonable values
            if per_page in [10, 15, 25, 50, 100]:
                return per_page
        except (ValueError, TypeError):
            pass
        return self.items_per_page
    
    def apply_search(self, queryset, search_query):
        """Apply search across specified fields."""
        if not search_query or not self.search_fields:
            return queryset
        
        # Build Q objects for OR search across fields
        search_q = Q()
        for field in self.search_fields:
            if '__' in field:  # Handle related field searches
                search_q |= Q(**{f"{field}__icontains": search_query})
            else:
                search_q |= Q(**{f"{field}__icontains": search_query})
        
        return queryset.filter(search_q)
    
    def apply_filters(self, queryset, filter_params):
        """Apply filters to queryset."""
        for field_name, value in filter_params.items():
            if value:
                queryset = queryset.filter(**{field_name: value})
        return queryset
    
    def apply_sorting(self, queryset, sort_param):
        """Apply sorting to queryset."""
        if sort_param:
            return queryset.order_by(sort_param)
        return queryset
    
    def get_paginated_queryset(self, queryset):
        """Apply pagination to queryset."""
        items_per_page = self.get_items_per_page()
        paginator = Paginator(queryset, items_per_page)
        page = self.request.GET.get('page', 1)
        
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        
        return objects
    
    def get_context_data(self, **kwargs):
        """Add search and filter context to template."""
        context = super().get_context_data(**kwargs)
        
        # Add search and filter parameters to context
        context['search_query'] = self.get_search_query()
        context['filter_params'] = self.get_filter_params()
        context['filter_fields'] = self.filter_fields
        context['current_sort'] = self.get_sort_param()
        context['sortable_fields'] = self.sortable_fields
        
        # Add pagination info
        if hasattr(context['object_list'], 'has_other_pages'):
            context['is_paginated'] = context['object_list'].has_other_pages()
            context['page_obj'] = context['object_list']
            context['paginator'] = context['object_list'].paginator
        
        return context


def get_model_field_choices(model, field_name):
    """
    Utility function to get choices for a model field.
    Useful for dynamically generating filter options.
    """
    field = model._meta.get_field(field_name)
    if hasattr(field, 'choices') and field.choices:
        return field.choices
    return []


def get_related_model_choices(model, field_name):
    """
    Get choices for related model fields (ForeignKey, etc.).
    Returns tuples of (id, str_representation) for dropdown filters.
    """
    field = model._meta.get_field(field_name)
    if hasattr(field, 'related_model'):
        related_model = field.related_model
        return [(obj.pk, str(obj)) for obj in related_model.objects.all()]
    return []
