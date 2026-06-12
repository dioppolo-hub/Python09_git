try:
    from pydantic import BaseModel, Field, ValidationError, model_validator
    from datetime import datetime
    from enum import Enum
    from typing import Optional
except ModuleNotFoundError as e:
    print(f"Error: {e}")
    print("\n=== INSTRUCTION ===")
    print("Build a Venv VE:")
    print("(Python3 -m venv venv) -> (source venv/bin/activate)")
    print("(pip install pydantic) -> (python3 space_station.py)")
    exit()


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_tipe: ContactType
    signal_streght: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = False


    @model_validator(mode='after')
    def validate_complex_error(self) -> 'AlienContact':
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")
        if self.contact_tipe.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        if self.contact_tipe == self.contact_tipe.TELEPATHIC and self.witness_count < 3:
            raise ValueError("Telepathic contact requires at least 3 witnesses")
        if self.signal_streght > 7.0 and not self.message_received:
            raise ValueError("Strong signals (> 7.0) should include received messages")
        return self


def main():
    print("Alien Contact Log Validation")
    print("=" * 40)
    try:
        valid_report = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.now(),
            location="Area 51, Nevada",
            contact_tipe=ContactType.RADIO,
            signal_streght=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
            is_verified=True
        )
        print("Valid contact report:")
        print(f"ID: {valid_report.contact_id}")
        print(f"Type: {valid_report.contact_tipe.value}")
        print(f"Location: {valid_report.location}")
        print(f"Signal: {valid_report.signal_streght}/10")
        print(f"Duration: {valid_report.duration_minutes} minutes")
        print(f"Witnesses: {valid_report.witness_count}")
        print(f"Message: {valid_report.message_received}")
    except ValidationError as e:
        print(f"Validation error: {e}")
    print("=" * 40)
    print("\nExpected validation error:")
    try:
        valid_report = AlienContact(
            contact_id="AC_2024_002(",
            timestamp=datetime.now(),
            location="London, UK",
            contact_tipe=ContactType.TELEPATHIC,
            signal_streght=4.0,
            duration_minutes=10,
            witness_count=1,
            message_received="Greetings from Zeta Reticuli"
        )
    except ValidationError as e:
        for error in e.errors():
            print(error['msg'])


if __name__ == "__main__":
    main()
