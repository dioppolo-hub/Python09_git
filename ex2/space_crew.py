try:
    from pydantic import BaseModel, Field, ValidationError, model_validator
    from datetime import datetime
    from enum import Enum
except ModuleNotFoundError as e:
    print(f"Error: {e}")
    print("\n=== INSTRUCTION ===")
    print("Build a Venv VE:")
    print("(Python3 -m venv venv) -> (source venv/bin/activate)")
    print("(pip install pydantic) -> (python3 space_station.py)")
    exit()


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LITENANT = "liutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=500)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validate_error(self) -> 'SpaceMission':
        if not self.mission_id.startswith("M"):
            raise ValueError("Contact ID must start with 'M'")
        has_leader = False
        for member in self.crew:
            if (
                member.rank == "commander" or
                member.rank == "captain"
            ):
                has_leader = True
                break
        if not has_leader:
            raise ValueError(
                "The mission crew must include one Captain or one Commander"
                )
        return self


def main():
    liutenant = CrewMember(
        member_id="C001",
        name="Franko Rossi",
        rank=Rank.LITENANT,
        age=19,
        specialization="Navigation",
        years_experience=1
    )
    commander = CrewMember(
        member_id="C002",
        name="Bobby b. blue",
        rank=Rank.COMMANDER,
        age=29,
        specialization="Mission Command",
        years_experience=2
    )
    officer = CrewMember(
        member_id="C003",
        name="Danny d. doo",
        rank=Rank.OFFICER,
        age=35,
        specialization="Engineering",
        years_experience=5
    )
    print("Space Mission Crew Validation:")
    print("=" * 40)
    try:
        valid_mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            crew=[liutenant, commander, officer],
            mission_status="planned",
            budget_millions=2500.0,
        )
        print("Valid Mission created:")
        print(f"Mission: {valid_mission.mission_name}")
        print(f"ID: {valid_mission.mission_id}")
        print(f"Destination: {valid_mission.destination}")
        print(f"Budget: {valid_mission.budget_millions}M")
        print(f"Mission Status: {valid_mission.mission_status}")
        print(f"Launch_date: {valid_mission.launch_date}")
        print(f"Crew Size: {len(valid_mission.crew)}")
        for member in valid_mission.crew:
            print(f"- {member.name} ({member.rank}) - {member.specialization}")
    except ValidationError as e:
        print(f"Validation Error: {e}")
    print("=" * 40)
    try:
        print("\nTesting Invalid Mission...\n")
        invalid_mission = SpaceMission(
                mission_id="M2024_MARS",
                mission_name="Mars Colony Establishment",
                destination="Mars",
                launch_date=datetime.now(),
                duration_days=900,
                crew=[liutenant, officer],
                mission_status="planned",
                budget_millions=2500.0,
            )
        print("Invalid Mission created:")
        print(f"Mission: {invalid_mission.mission_name}")
        print(f"ID: {invalid_mission.mission_id}")
        print(f"Destination: {invalid_mission.destination}")
        print(f"Budget: {invalid_mission.budget_millions}M")
        print(f"Mission Status: {invalid_mission.mission_status}")
        print(f"Launch_date: {invalid_mission.launch_date}")
        print(f"Crew Size: {len(invalid_mission.crew)}")
    except ValidationError as e:
        for error in e.errors():
            print(error['msg'])


if __name__ == "__main__":
    main()
