import os
import httpx
from crewai.tools import BaseTool
from typing import Type, Optional, Any
from pydantic import BaseModel, Field


class PexelsSearchInput(BaseModel):
    """Input schema for Pexels search tool."""
    query: str = Field(..., description="The search query for finding stock photos (e.g., 'modern office', 'nature sunset')")
    per_page: int = Field(default=15, description="Number of results to return (max 80)")
    orientation: Optional[str] = Field(default=None, description="Photo orientation: 'landscape', 'portrait', or 'square'")


class PexelsSearchTool(BaseTool):
    name: str = "Search Stock Photos"
    description: str = (
        "Searches the Pexels API for high-quality stock photos based on a query. "
        "Returns relevant photos with URLs, photographer info, and metadata. "
        "Use this tool to find stock photos that match user requirements."
    )
    args_schema: Type[BaseModel] = PexelsSearchInput
    api_key: str = Field(default="")
    
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
    
    def _run(self, query: str, per_page: int = 15, orientation: Optional[str] = None) -> str:
        """
        Execute the Pexels API search.
        
        Args:
            query: Search query string
            per_page: Number of results (1-80)
            orientation: Optional orientation filter
            
        Returns:
            Formatted string with photo results
        """
        try:
            # Validate per_page
            per_page = min(max(1, per_page), 80)
            
            # Build request
            url = "https://api.pexels.com/v1/search"
            headers = {
                "Authorization": self.api_key
            }
            params = {
                "query": query,
                "per_page": per_page
            }
            
            if orientation:
                params["orientation"] = orientation
            
            # Make synchronous request
            with httpx.Client() as client:
                response = client.get(url, headers=headers, params=params, timeout=30.0)
                response.raise_for_status()
                data = response.json()
            
            # Check if photos were found
            if not data.get("photos"):
                return f"No photos found for query: '{query}'. Try different search terms."
            
            # Format results - concise format to reduce context size
            photos = data["photos"]
            total_results = data.get("total_results", 0)
            
            result = f"Found {total_results} photos for '{query}'. Showing top {len(photos)} results:\n\n"
            
            for i, photo in enumerate(photos, 1):
                # Include alt description for better selection decisions
                alt_text = photo.get('alt', 'No description available')
                # Concise format: Description, ID, photographer, dimensions, Pexels page, thumbnail URL, and Original URL
                result += f"{i}. Description: {alt_text} | "
                result += f"Photo ID: {photo['id']} | "
                result += f"Photographer: [{photo['photographer']}]({photo['photographer_url']}) | "
                result += f"{photo['width']}x{photo['height']} | "
                result += f"[Pexels]({photo['url']}) | "
                result += f"Thumbnail: {photo['src']['medium']} | "
                result += f"[Original]({photo['src']['original']})\n"
            
            return result
            
        except httpx.HTTPStatusError as e:
            return f"Error searching Pexels API: HTTP {e.response.status_code}. Check your API key and query."
        except httpx.TimeoutException:
            return "Request to Pexels API timed out. Please try again."
        except Exception as e:
            return f"Unexpected error searching Pexels: {str(e)}"
