from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from .prompt import WARDROBE_PROMPT
from .tools.query_tools import (
    get_outfits_for_event,
    get_outfit_details,
    list_wardrobe_items,
)
from .tools.crud_tools import (
    create_wardrobe_item,
    update_wardrobe_item,
    delete_wardrobe_item,
    mark_item_worn,
)
from ...shared_libraries.model_config import get_model_type


wardrobe_agent = Agent(
    name="wardrobe_agent",
    model=get_model_type("sub_agent"),
    instruction=WARDROBE_PROMPT,
    description="Fashion and outfit specialist for travel planning, recommending appropriate clothing from a digital wardrobe database with helpful alternatives when items are missing.",
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
