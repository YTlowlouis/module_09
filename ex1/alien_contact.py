from pydantic import BaseModel, Field, model_validator, ValidationError
from enum import Enum
from typing import Optional
from datetime import datetime

class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"

class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime = None
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(gt=0.0, lt=10.0)
    duration_minutes: int = Field(gt=1, lt=1440)
    witness_count: int = Field(gt=1, lt=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode='after')
    def check_logic(self) -> 'AlienContact':
        if self.contact_id[0] != "A" or self.contact_id[1] != "C":
            raise ValueError("Contact id does not start with AC")
        if self.contact_type == ContactType.PHYSICAL and self.is_verified == False:
            raise ValueError("Physical contact type must be verified")
        if self.contact_type == ContactType.TELEPATHIC and self.witness_count < 3:
            raise ValueError("Telepathic contact must have at least 3 witness")
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Signal strength of > 7 must have a message received")
        return self


def main():
    contact = AlienContact(contact_id="AC49889", timestamp="2023-10-25T14:30:00", location="moon", contact_type=ContactType.PHYSICAL, signal_strength=5.0, duration_minutes=50, witness_count=3, is_verified=True)
    print(contact.model_dump_json(indent=2))
    try:
        contact2 = AlienContact(contact_id="AC59489", timestamp="2023-10-25T14:30:00", location="moon", contact_type=ContactType.PHYSICAL, signal_strength=5.0, duration_minutes=50, witness_count=3, is_verified=False)
    except ValidationError as e:
        print(f"ValidationError: {e}")


if __name__ == "__main__":
    main()


