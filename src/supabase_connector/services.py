"""
Services Management Functions

Functions for managing services in the public.services table.

Main function: get_services() - handles all filtering needs
Helper functions: get_service_categories(), get_services_summary()
Other functions are convenience wrappers around get_services()
"""

from typing import List, Dict, Any, Optional, Union
from .client import get_global_connector


def get_services(
    service_id: Optional[int] = None,
    name: Optional[str] = None,
    category: Optional[str] = None,
    is_active: Optional[bool] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Retrieve services from the public.services table with optional filtering.

    Parameters
    ----------
    service_id : int, optional
        Filter by specific service ID.
    name : str, optional
        Filter by service name (exact match or partial match).
    category : str, optional
        Filter by service category.
    is_active : bool, optional
        Filter by active status.
    limit : int, optional
        Maximum number of records to return.

    Returns
    -------
    List[Dict[str, Any]]
        A list of service records matching the criteria.

    Raises
    -------
    RuntimeError
        If the Supabase client is not initialized or the query fails.
    
    Examples
    --------
    >>> # Get all services
    >>> services = get_services()
    
    >>> # Get specific service by ID
    >>> service = get_services(service_id=1)
    
    >>> # Get services by category
    >>> services = get_services(category="consultation")
    
    >>> # Get active services with name containing "massage"
    >>> services = get_services(name="massage", is_active=True)
    """
    try:
        connector = get_global_connector()
        client = connector.get_client()
        
        # Start building the query
        query = client.table('services').select('*')
        
        # Apply filters
        if service_id is not None:
            query = query.eq('id', service_id)
        
        if name is not None:
            # Use ilike for case-insensitive partial matching
            query = query.ilike('name', f'%{name}%')
        
        if category is not None:
            query = query.eq('category', category)
        
        if is_active is not None:
            query = query.eq('is_active', is_active)
        
        # Apply limit if specified
        if limit is not None:
            query = query.limit(limit)
        
        # Order by name for consistent results
        query = query.order('name')
        
        # Execute query
        response = query.execute()
        return response.data
        
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve services: {e}")


def get_service_by_id(service_id: int) -> Optional[Dict[str, Any]]:
    """
    Get a specific service by its ID.

    Parameters
    ----------
    service_id : int
        The ID of the service to retrieve.

    Returns
    -------
    Optional[Dict[str, Any]]
        The service record if found, None otherwise.

    Raises
    -------
    RuntimeError
        If the query fails.
    ValueError
        If service_id is not a positive integer.
    
    Examples
    --------
    >>> service = get_service_by_id(1)
    >>> if service:
    ...     print(f"Service: {service['name']}")
    """
    if not isinstance(service_id, int) or service_id <= 0:
        raise ValueError("service_id must be a positive integer")
    
    services = get_services(service_id=service_id)
    return services[0] if services else None


def get_services_by_category(category: str, is_active: bool = True) -> List[Dict[str, Any]]:
    """
    Get all services in a specific category.

    Parameters
    ----------
    category : str
        The category to filter by.
    is_active : bool, optional
        Whether to include only active services (default: True).

    Returns
    -------
    List[Dict[str, Any]]
        A list of services in the specified category.

    Raises
    -------
    ValueError
        If category is empty.
    RuntimeError
        If the query fails.
    
    Examples
    --------
    >>> services = get_services_by_category("spa")
    >>> for service in services:
    ...     print(f"{service['name']}: ${service['price']}")
    """
    if not category or not category.strip():
        raise ValueError("category cannot be empty")
    
    return get_services(category=category.strip(), is_active=is_active)


def search_services_by_name(name: str, is_active: bool = True) -> List[Dict[str, Any]]:
    """
    Search services by name (partial matching).

    Parameters
    ----------
    name : str
        The name or part of the name to search for.
    is_active : bool, optional
        Whether to include only active services (default: True).

    Returns
    -------
    List[Dict[str, Any]]
        A list of services matching the name criteria.

    Raises
    -------
    ValueError
        If name is empty.
    RuntimeError
        If the query fails.
    
    Examples
    --------
    >>> # Find all services with "massage" in the name
    >>> services = search_services_by_name("massage")
    
    >>> # Find all services (active and inactive) with "facial" in the name
    >>> services = search_services_by_name("facial", is_active=False)
    """
    if not name or not name.strip():
        raise ValueError("name cannot be empty")
    
    return get_services(name=name.strip(), is_active=is_active)


def get_active_services(limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Get all active services.

    Parameters
    ----------
    limit : int, optional
        Maximum number of services to return.

    Returns
    -------
    List[Dict[str, Any]]
        A list of active services.

    Raises
    -------
    RuntimeError
        If the query fails.
    
    Examples
    --------
    >>> # Get all active services
    >>> services = get_active_services()
    
    >>> # Get top 10 active services
    >>> services = get_active_services(limit=10)
    """
    return get_services(is_active=True, limit=limit)


def get_service_categories() -> List[str]:
    """
    Get all unique service categories.

    Returns
    -------
    List[str]
        A list of unique categories.

    Raises
    -------
    RuntimeError
        If the query fails.
    
    Examples
    --------
    >>> categories = get_service_categories()
    >>> print("Available categories:", categories)
    """
    try:
        connector = get_global_connector()
        client = connector.get_client()
        
        # Get distinct categories
        response = client.table('services').select('category').execute()
        
        # Extract unique categories
        categories = list(set(
            record['category'] 
            for record in response.data 
            if record.get('category')
        ))
        
        return sorted(categories)
        
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve service categories: {e}")


def get_services_summary() -> Dict[str, Any]:
    """
    Get a summary of services including counts by category and status.

    Returns
    -------
    Dict[str, Any]
        A dictionary with service statistics.

    Raises
    -------
    RuntimeError
        If the query fails.
    
    Examples
    --------
    >>> summary = get_services_summary()
    >>> print(f"Total services: {summary['total_services']}")
    >>> print(f"Active services: {summary['active_services']}")
    """
    try:
        all_services = get_services()
        active_services = [s for s in all_services if s.get('is_active', False)]
        categories = get_service_categories()
        
        # Count services by category
        category_counts = {}
        for service in all_services:
            category = service.get('category', 'Unknown')
            category_counts[category] = category_counts.get(category, 0) + 1
        
        return {
            'total_services': len(all_services),
            'active_services': len(active_services),
            'inactive_services': len(all_services) - len(active_services),
            'total_categories': len(categories),
            'categories': categories,
            'services_by_category': category_counts,
            'average_price': sum(s.get('price', 0) or 0 for s in active_services) / len(active_services) if active_services else 0,
            'average_duration': sum(s.get('duration_minutes', 0) or 0 for s in active_services) / len(active_services) if active_services else 0
        }
        
    except Exception as e:
        raise RuntimeError(f"Failed to generate services summary: {e}")