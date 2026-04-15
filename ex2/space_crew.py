from enum import Enum
from pydantics import BaseModel, model_validator, Field, ValidationError
from datetime import datetime
from typing import List

class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"

class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(gt=18, lt=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(gt=0, lt=50)
    is_active: bool = True

class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(gt=1, lt=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(gt=1.0, lt=10000.0)

    @model_validator(mode='after')
    def check_requirements(self) -> 'SpaceMission':
        if self.mission_id[0] != "M":
            raise ValueError("Mission id must start with M")

        has_com_or_cap = False
        for member in self.crew:
            if member.is_active == False:
                raise ValueError("A member is inactive")
            if member.rank == Rank.CAPTAIN or member.rank == Rank.COMMANDER:
                has_com_or_cap = True
                break
        if not has_com_or_cap:
            raise ValueError("Mission has no commander or captain")
        if not self._get_percent_of_experienced():
            raise ValueError("Long missions need at least 50 percent experienced crew")

    def _get_percent_of_experienced(self) -> bool:
        experienced = 0
        total = 0
        for crew_member in self.crew:
            if crew_member.years_experience > 5:
                experienced += 1
            total += 1
        if (total * experienced) / 100 >= 0.5:
            return True
        return False



