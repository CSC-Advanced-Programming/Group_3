"""Query service for handling database operations."""
from typing import Dict, List, Any, Type
from django.db.models import QuerySet, Q
from django.core.paginator import Paginator
from ...utils import get_model_field_choices, get_related_model_choices


class QueryService:
    """Service for handling database queries with search and filtering."""
    
    def __init__(
        self, 
        model: Type[Any],
        search_fields: List[str],
        filter_fields: Dict[str, bool],
        items_per_page: int = 15
    ):
        self.model = model
        self.search_fields = search_fields
        self._filter_field_names = filter_fields
        self.items_per_page = items_per_page
        self.filter_fields = self._initialize_filter_fields()
    
    def _initialize_filter_fields(self) -> Dict[str, List[tuple]]:
        """Initialize filter field choices."""
        fields = {}
        for field_name, should_populate in self._filter_field_names.items():
            if should_populate:
                if '__' in field_name:  # Related field
                    fields[field_name] = get_related_model_choices(self.model, field_name.split('__')[0])
                else:
                    fields[field_name] = get_model_field_choices(self.model, field_name)
        return fields
    
    def execute(
        self, 
        search_query: str = '', 
        filters: Dict[str, Any] = None,
        sort_field: str = None
    ) -> QuerySet:
        """Execute query with search and filters."""
        queryset = self.get_base_queryset()
        
        if search_query:
            queryset = self._apply_search(queryset, search_query)
        
        if filters:
            queryset = self._apply_filters(queryset, filters)
            
        if sort_field:
            queryset = self._apply_sorting(queryset, sort_field)
            
        return queryset
    
    def get_base_queryset(self) -> QuerySet:
        """Get base queryset with necessary joins."""
        return self.model.objects.all()
    
    def _apply_search(self, queryset: QuerySet, search_query: str) -> QuerySet:
        """Apply search filter to queryset."""
        if not search_query:
            return queryset

        q_objects = Q()
        for field in self.search_fields:
            q_objects |= Q(**{f"{field}__icontains": search_query})
        return queryset.filter(q_objects)
    
    def _apply_filters(self, queryset: QuerySet, filters: Dict[str, Any]) -> QuerySet:
        """Apply filters to queryset."""
        valid_filters = {
            k: v for k, v in filters.items() 
            if k in self.filter_fields and v
        }
        if valid_filters:
            return queryset.filter(**valid_filters)
        return queryset
    
    def _apply_sorting(self, queryset: QuerySet, sort_field: str) -> QuerySet:
        """Apply sorting to queryset."""
        return queryset.order_by(sort_field)
    
    def get_filter_choices(self) -> Dict[str, List[tuple]]:
        """Get available filter choices."""
        return self.filter_fields