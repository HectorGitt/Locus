from typing import Dict, Optional
from sqlalchemy import or_, func
from .db_utils import get_db, close_db, item_to_dict, handle_db_error, WardrobeItem


def get_outfits_for_event(
    event_type: str,
    weather: Optional[str] = None,
    formality: Optional[str] = None,
    limit: int = 5,
) -> Dict:
    """
    Fetch outfit recommendations from the wardrobe database based on event type and conditions.
    """
    try:
        db = get_db()

        # Build query with flexible filtering
        query = db.query(WardrobeItem).filter(WardrobeItem.is_available)

        # Lenient occasion filtering
        if event_type:
            query = query.filter(WardrobeItem.occasion.ilike(f"%{event_type}%"))

        # Lenient weather/season filtering
        if weather:
            weather_filter = or_(
                WardrobeItem.season.ilike(f"%{weather}%"),
                WardrobeItem.occasion.ilike(f"%{weather}%"),
            )
            query = query.filter(weather_filter)

        # Lenient formality filtering
        if formality:
            formality_filter = or_(
                WardrobeItem.category.ilike(f"%{formality}%"),
                WardrobeItem.occasion.ilike(f"%{formality}%"),
                WardrobeItem.description.ilike(f"%{formality}%"),
            )
            query = query.filter(formality_filter)

        # Order by: unworn items first, then by last worn date, then favorites, then newest
        query = query.order_by(
            func.coalesce(WardrobeItem.last_worn_date, func.now()).asc(),
            WardrobeItem.is_favorite.desc(),
            WardrobeItem.created_at.desc(),
        ).limit(limit)

        results = query.all()
        items = [item_to_dict(item) for item in results]

        close_db(db)

        return {
            "success": True,
            "items": items,
            "count": len(items),
            "event_type": event_type,
            "filters": {"weather": weather, "formality": formality},
        }

    except Exception as e:
        return handle_db_error(e, "Failed to fetch wardrobe items from database")


def get_outfit_details(item_id: int) -> Dict:
    """
    Get detailed information about a specific wardrobe item.

    Args:
        item_id: The ID of the wardrobe item to retrieve

    Returns:
        Dictionary containing detailed item information
    """
    try:
        db = get_db()
        item = db.query(WardrobeItem).filter(WardrobeItem.id == item_id).first()

        if not item:
            close_db(db)
            return {
                "success": False,
                "error": f"Wardrobe item with ID {item_id} not found",
            }

        item_dict = item_to_dict(item)
        close_db(db)

        return {"success": True, "item": item_dict}

    except Exception as e:
        return handle_db_error(e, f"Failed to fetch wardrobe item {item_id}")


def list_wardrobe_items(
    category: Optional[str] = None,
    season: Optional[str] = None,
    occasion: Optional[str] = None,
    is_available: Optional[bool] = None,
    is_favorite: Optional[bool] = None,
    limit: int = 50,
    offset: int = 0,
) -> Dict:
    """
    List wardrobe items with optional filtering.

    Args:
        category: Filter by category (optional)
        season: Filter by season (optional)
        occasion: Filter by occasion (optional)
        is_available: Filter by availability (optional)
        is_favorite: Filter by favorite status (optional)
        limit: Maximum number of items to return (default 50)
        offset: Number of items to skip (default 0)

    Returns:
        Dictionary containing list of items and metadata
    """
    try:
        db = get_db()

        # Build query with filters
        query = db.query(WardrobeItem)

        if category:
            query = query.filter(WardrobeItem.category.ilike(f"%{category}%"))
        if season:
            query = query.filter(WardrobeItem.season.ilike(f"%{season}%"))
        if occasion:
            query = query.filter(WardrobeItem.occasion.ilike(f"%{occasion}%"))
        if is_available is not None:
            query = query.filter(WardrobeItem.is_available == is_available)
        if is_favorite is not None:
            query = query.filter(WardrobeItem.is_favorite == is_favorite)

        # Get total count before pagination
        total_count = query.count()

        # Apply pagination
        query = (
            query.order_by(WardrobeItem.created_at.desc()).limit(limit).offset(offset)
        )

        results = query.all()
        items = [item_to_dict(item) for item in results]

        close_db(db)

        return {
            "success": True,
            "items": items,
            "count": len(items),
            "total_count": total_count,
            "limit": limit,
            "offset": offset,
            "filters": {
                "category": category,
                "season": season,
                "occasion": occasion,
                "is_available": is_available,
                "is_favorite": is_favorite,
            },
        }

    except Exception as e:
        return handle_db_error(e, "Failed to list wardrobe items")
