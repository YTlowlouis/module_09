from pydantic import BaseModel, Field, ValidationError
from typing import Optional
from datetime import datetime

class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(gt=1, lt=20)
    power_level: float = Field(gt=0.0, lt=100.0)
    oxygen_level: float = Field(gt=0.0, lt=100.0)
    last_maintenance: datetime = None
    is_operational: bool = True
    notes: Optional[str] = None

def main():
    space_station = SpaceStation(station_id="89498498", name="lunar_station", crew_size=5, power_level=50.0, oxygen_level=50.0, last_maintenance="2023-10-25T14:30:00", is_operational=True)
    print("Valid Station created:")
    print(space_station.model_dump_json(indent=2))
    try:
        space_station2 = SpaceStation(station_id="498498", name="lunar_station2", crew_size=50, power_level=50.0, oxygen_level=50.0, last_maintenance="2023-10-25T14:30:00", is_operational=True)
    except ValidationError as e:
        print(f"\nValidationError: {e}")


if __name__ == "__main__":
    main()
