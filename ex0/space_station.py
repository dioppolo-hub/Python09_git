try:
    from pydantic import BaseModel, Field, ValidationError
    from datetime import datetime
    from typing import Optional
except ModuleNotFoundError as e:
    print(f"Error: {e}")
    print("\n=== INSTRUCTION ===\n")
    print("Build a Venv VE:")
    print("(Python3 -m venv venv) -> (source venv/bin/activate)")
    print("(pip install pydantic) -> (python3 space_station.py)")
    exit()


class SpaceStation(BaseModel):
    stattion_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=3, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=1.0, le=100.0)
    oxygen_level: float = Field(ge=1.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(default=None, max_length=200)


def main():
    print("Space Station Data Validation")
    print("=" * 40)
    try:
        valid_station = SpaceStation(
            stattion_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance="2026-06-12T12:00:00"
        )
        print("Valid Station Created:")
        print(f"ID: {valid_station.stattion_id}")
        print(f"Name: {valid_station.name}")
        print(f"Crew: {valid_station.crew_size} people")
        print(f"Power: {valid_station.power_level}%")
        print(f"Oxygen: {valid_station.oxygen_level}%")
        print(f"Last Manteinance: {valid_station.last_maintenance}")
        if valid_station.is_operational:
            status = "Operational"
        else:
            status = "Not Operational"
        print(f"Status: {status}")
    except ValidationError as e:
        print(f"Unexpected error: {e}")
    print("=" * 40)
    try:
        print("\nTrying invalid SpaceStation...\n")
        invalid_station = SpaceStation(
            stattion_id="BAD01",
            name="Broken Station",
            crew_size=25,
            power_level=50.0,
            oxygen_level=50.0,
            last_maintenance="2026-06-12T12:00:00"
        )
    except ValidationError as e:
        errors = e.errors()
        for error in errors:
            print(error['msg'])


if __name__ == "__main__":
    main()
