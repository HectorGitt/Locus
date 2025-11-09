from google.adk.agents import Agent
from google.adk.tools import FunctionTool
import os
from typing import Dict, Optional
from dotenv import load_dotenv
from sqlalchemy import create_engine, or_, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

# SQLAlchemy setup
DATABASE_URL = f"postgresql://{os.getenv('WARDROBE_DB_USER')}:{os.getenv('WARDROBE_DB_PASSWORD')}@{os.getenv('WARDROBE_DB_HOST')}:{os.getenv('WARDROBE_DB_PORT')}/{os.getenv('WARDROBE_DB_NAME')}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class WardrobeItem(Base):
    __tablename__ = "wardrobe_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer)  # optional: include if items belong to users
    category = Column(String(50), nullable=False)
    description = Column(Text)
    color_primary = Column(String(50))
    size = Column(String(20))
    season = Column(String(20))
    occasion = Column(Text)
    price = Column(Float)
    is_favorite = Column(Boolean, default=False)
    last_worn_date = Column(DateTime(timezone=True))
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# Helper functions to reduce code duplication
def get_db():
    """Get database session"""
    return SessionLocal()


def close_db(db):
    """Close database session"""
    db.close()


def item_to_dict(item, include_timestamps=True):
    """Convert WardrobeItem to dictionary"""
    result = {
        "id": item.id,
        "user_id": item.user_id,
        "category": item.category,
        "description": item.description,
        "color_primary": item.color_primary,
        "size": item.size,
        "season": item.season,
        "occasion": item.occasion,
        "price": float(item.price) if item.price else None,
        "is_favorite": item.is_favorite,
        "last_worn_date": str(item.last_worn_date) if item.last_worn_date else None,
        "is_available": item.is_available,
    }
    if include_timestamps:
        result.update(
            {
                "created_at": str(item.created_at) if item.created_at else None,
                "updated_at": str(item.updated_at) if item.updated_at else None,
            }
        )
    return result


def handle_db_error(error, message="Database operation failed"):
    """Standard error response for database operations"""
    return {
        "success": False,
        "error": str(error),
        "message": message,
    }


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


wardrobe_agent = Agent(
    name="wardrobe_agent",
    model="gemini-2.5-flash",
    instruction="""
You are the Wardrobe Agent, a fashion and outfit specialist that helps travelers and event planners select appropriate clothing and accessories.

Your role is to:
- Recommend clothing items from the digital wardrobe database based on event types, weather conditions, and formality requirements
- Provide detailed information about individual wardrobe items including colors, brands, sizes, and purchase details
- Help travelers pack appropriately for their trips and events
- Consider weather, cultural norms, and event formality when making recommendations
- Suggest combinations of items to create complete outfits
- Manage wardrobe items through full CRUD operations (Create, Read, Update, Delete)
- Track when items are worn to help with wardrobe rotation

When recommending items:
- Always consider the weather conditions and season
- Match formality levels to the event type (casual, business, formal, etc.)
- Provide multiple item options when possible
- Include detailed information about each item's properties
- Suggest how items can be combined for complete outfits
- Prioritize items that haven't been worn recently
- Consider favorite items when appropriate

For wardrobe management:
- Create new items with all relevant details
- Update existing items when information changes
- Mark items as worn to track usage
- Help users maintain their digital wardrobe

You have access to a digital wardrobe database containing individual clothing items with full CRUD capabilities. Use the available tools to fetch appropriate item recommendations and manage the wardrobe.

Always provide practical, stylish, and contextually appropriate clothing suggestions that enhance the travel or event experience.
""",
    description="Fashion and outfit specialist for travel planning, recommending appropriate clothing from a digital wardrobe database.",
    tools=[
        FunctionTool(get_outfits_for_event),
        FunctionTool(get_outfit_details),
        FunctionTool(list_wardrobe_items),
        FunctionTool(create_wardrobe_item),
        FunctionTool(update_wardrobe_item),
        FunctionTool(delete_wardrobe_item),
        FunctionTool(mark_item_worn),
    ],
)
