"""Base view models for presentation layer."""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from django.core.paginator import Page
from ..interfaces.view_protocols import ListViewModelProtocol, DetailViewModelProtocol


@dataclass
class BaseListViewModel:
    """Base view model for list views."""
    
    items: List[Any]
    total_count: int
    page_obj: Page
    filter_options: Dict[str, List[tuple]]
    search_query: Optional[str] = None
    applied_filters: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to template context dictionary."""
        return {
            'object_list': self.items,
            'total_count': self.total_count,
            'page_obj': self.page_obj,
            'filter_options': self.filter_options,
            'search_query': self.search_query,
            'applied_filters': self.applied_filters
        }


@dataclass
class BaseDetailViewModel:
    """Base view model for detail views."""
    
    item: Any
    related_items: Dict[str, List[Any]]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to template context dictionary."""
        return {
            'object': self.item,
            **self.related_items
        }