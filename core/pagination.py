"""
Pagination Helper - Handle large dataset pagination
"""

from core.logger import get_logger

logger = get_logger('app')


class Paginator:
    """Handle pagination for large datasets"""
    
    def __init__(self, items_per_page=50):
        self.items_per_page = items_per_page
        self.current_page = 1
        self.total_items = 0
        self.total_pages = 0
    
    def paginate(self, query_func, *args, **kwargs):
        """
        Paginate a database query
        query_func should accept limit, offset, count_only parameters
        """
        # Get total count first
        try:
            self.total_items = query_func(*args, count_only=True, **kwargs)
        except TypeError:
            # Fallback if count_only not supported
            logger.warning("Query function doesn't support count_only")
            self.total_items = len(query_func(*args, **kwargs))
        
        # Calculate total pages
        self.total_pages = max(1, (self.total_items + self.items_per_page - 1) // self.items_per_page)
        
        # Ensure current page is valid
        if self.current_page > self.total_pages:
            self.current_page = self.total_pages
        
        # Calculate offset
        offset = (self.current_page - 1) * self.items_per_page
        
        # Get page data
        items = query_func(*args, limit=self.items_per_page, offset=offset, **kwargs)
        
        return {
            'items': items,
            'current_page': self.current_page,
            'total_pages': self.total_pages,
            'total_items': self.total_items,
            'items_per_page': self.items_per_page,
            'has_next': self.current_page < self.total_pages,
            'has_prev': self.current_page > 1,
            'start_item': offset + 1 if items else 0,
            'end_item': min(offset + len(items), self.total_items)
        }
    
    def next_page(self):
        """Go to next page"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            return True
        return False
    
    def prev_page(self):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            return True
        return False
    
    def goto_page(self, page_num):
        """Go to specific page"""
        if 1 <= page_num <= self.total_pages:
            self.current_page = page_num
            return True
        return False
    
    def first_page(self):
        """Go to first page"""
        self.current_page = 1
    
    def last_page(self):
        """Go to last page"""
        self.current_page = self.total_pages
    
    def get_page_info(self):
        """Get current pagination info"""
        return {
            'current_page': self.current_page,
            'total_pages': self.total_pages,
            'total_items': self.total_items,
            'items_per_page': self.items_per_page
        }
