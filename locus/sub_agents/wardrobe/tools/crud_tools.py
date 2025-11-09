from typing import Dict, Optional
from .db_utils import get_db, close_db, item_to_dict, handle_db_error, WardrobeItem


def create_wardrobe_item(
    category: str,
    description: Optional[str] = None,
    color_primary: Optional[str] = None,
    size: Optional[str] = None,
    season: Optional[str] = None,
    occasion: Optional[str] = None,
    price: Optional[float] = None,
    user_id: Optional[int] = None,
) -> Dict:
    """
    Create a new wardrobe item.

    Args:
        category: Item category (required)
        description: Item description
        color_primary: Primary color
        size: Item size
        season: Suitable season
        occasion: Suitable occasions
        price: Item price
        user_id: User ID (optional)

    Returns:
        Dictionary containing creation result
    """
    try:
        db = get_db()
        new_item = WardrobeItem(
            category=category,
            description=description,
            color_primary=color_primary,
            size=size,
            season=season,
            occasion=occasion,
            price=price,
            user_id=user_id,
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)

        item_dict = item_to_dict(new_item)
        close_db(db)

        return {
            "success": True,
            "item": item_dict,
            "message": "Wardrobe item created successfully",
        }

    except Exception as e:
        return handle_db_error(e, "Failed to create wardrobe item")


def update_wardrobe_item(
    item_id: int,
    category: Optional[str] = None,
    description: Optional[str] = None,
    color_primary: Optional[str] = None,
    size: Optional[str] = None,
    season: Optional[str] = None,
    occasion: Optional[str] = None,
    price: Optional[float] = None,
    is_favorite: Optional[bool] = None,
    is_available: Optional[bool] = None,
    last_worn_date: Optional[str] = None,
) -> Dict:
    """
    Update an existing wardrobe item.

    Args:
        item_id: ID of the item to update
        Other parameters: Fields to update (all optional)

    Returns:
        Dictionary containing update result
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

        # Update fields if provided
        if category is not None:
            item.category = category
        if description is not None:
            item.description = description
        if color_primary is not None:
            item.color_primary = color_primary
        if size is not None:
            item.size = size
        if season is not None:
            item.season = season
        if occasion is not None:
            item.occasion = occasion
        if price is not None:
            item.price = price
        if is_favorite is not None:
            item.is_favorite = is_favorite
        if is_available is not None:
            item.is_available = is_available
        if last_worn_date is not None:
            from datetime import datetime

            item.last_worn_date = datetime.fromisoformat(
                last_worn_date.replace("Z", "+00:00")
            )

        db.commit()
        db.refresh(item)

        item_dict = item_to_dict(item)
        close_db(db)

        return {
            "success": True,
            "item": item_dict,
            "message": "Wardrobe item updated successfully",
        }

    except Exception as e:
        return handle_db_error(e, "Failed to update wardrobe item")


def delete_wardrobe_item(item_id: int) -> Dict:
    """
    Delete a wardrobe item.

    Args:
        item_id: ID of the item to delete

    Returns:
        Dictionary containing deletion result
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

        db.delete(item)
        db.commit()
        close_db(db)

        return {
            "success": True,
            "message": f"Wardrobe item with ID {item_id} deleted successfully",
        }

    except Exception as e:
        return handle_db_error(e, "Failed to delete wardrobe item")


def mark_item_worn(item_id: int) -> Dict:
    """
    Mark an item as worn (update last_worn_date to now).

    Args:
        item_id: ID of the item that was worn

    Returns:
        Dictionary containing update result
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

        from datetime import datetime

        item.last_worn_date = datetime.utcnow()
        db.commit()
        db.refresh(item)

        item_dict = item_to_dict(item)
        close_db(db)

        return {
            "success": True,
            "item": item_dict,
            "message": "Item marked as worn",
        }

    except Exception as e:
        return handle_db_error(e, "Failed to mark item as worn")
