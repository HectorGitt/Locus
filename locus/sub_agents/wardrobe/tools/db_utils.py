import os
from typing import Dict, Optional
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, func
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
