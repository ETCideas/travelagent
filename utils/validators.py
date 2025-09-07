from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class TravelerInfo(BaseModel):
    adults: int = Field(1, ge=0)
    children: int = Field(0, ge=0)
    rooms: int = Field(1, ge=1)

class PreferenceInput(BaseModel):
    name: str
    email: Optional[str] = None
    origin: str
    destinations: List[str]
    start_date: str
    end_date: str
    likes: List[str] = []
    dislikes: List[str] = []
    cuisine_focus: Optional[str] = None
    traveler: TravelerInfo = TravelerInfo()

    @field_validator("destinations")
    @classmethod
    def non_empty_destinations(cls, v):
        if not v:
            raise ValueError("Please provide at least one destination city.")
        return v
