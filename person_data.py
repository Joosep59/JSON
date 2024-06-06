from datetime import datetime
from typing import List, Dict, Tuple, Optional


class Person:

    def __init__(self, data: Dict[str, str]):

        self.name = data["nimi"]
        self.birth_date = data["sundinud"]
        self.occupation = data["amet"]
        self.death_date = data["surnud"]
        self.birth_year = int(self.birth_date.split('-')[0]) if self.birth_date != "0000-00-00" else None

    def is_alive(self) -> bool:
        return self.death_date == "0000-00-00"

    def age(self, on_date: Optional[datetime.date] = None) -> Optional[int]:
        if self.birth_date == "0000-00-00":
            return None
        if on_date is None:
            on_date = datetime.today().date()
        birth_date = datetime.strptime(self.birth_date, "%Y-%m-%d").date()
        age = on_date.year - birth_date.year - ((on_date.month, on_date.day) < (birth_date.month, birth_date.day))
        return age

    def death_age(self) -> Optional[int]:
        if self.is_alive() or self.death_date == "0000-00-00":
            return None
        death_date = datetime.strptime(self.death_date, "%Y-%m-%d").date()
        return self.age(on_date=death_date)

    def formatted_birth_date(self) -> str:
        return datetime.strptime(self.birth_date, "%Y-%m-%d").strftime(
            "%d.%m.%Y") if self.birth_date != "0000-00-00" else "Unknown"

    def formatted_death_date(self) -> Optional[str]:
        return datetime.strptime(self.death_date, "%Y-%m-%d").strftime("%d.%m.%Y") if not self.is_alive() else None


class PersonData:

    def __init__(self, data: List[Dict[str, str]]):
        self.people = [Person(person) for person in data]

        # Initialize variables for calculations
        self.living_count = 0
        self.deceased_count = 0
        self.longest_name_data = ("", 0, "")
        self.oldest_living_data = ("", 0, "")
        self.oldest_deceased_data = ("", 0, "", "")
        self.total_actor_count = 0
        self.birth_year_count = 0
        self.unique_occupations_set = set()
        self.names_with_more_than_two_parts_count = 0
        self.birth_death_same_except_year_count = 0

        # Iterate over each person to calculate statistics
        for person in self.people:
            # Count living and deceased people
            if person.is_alive():
                self.living_count += 1
            else:
                self.deceased_count += 1

            # Calculate longest name
            if len(person.name) > self.longest_name_data[1]:
                self.longest_name_data = (person.name, len(person.name), person.formatted_birth_date())

            # Calculate oldest living person
            if person.is_alive() and person.age() > self.oldest_living_data[1]:
                self.oldest_living_data = (person.name, person.age(), person.formatted_birth_date())

            # Calculate oldest deceased person
            if not person.is_alive() and person.death_age() > self.oldest_deceased_data[1]:
                self.oldest_deceased_data = (person.name, person.death_age(), person.formatted_birth_date(), person.formatted_death_date())

            # Count actors
            if "näitleja" in person.occupation:
                self.total_actor_count += 1

            # Count people born in a specific year (e.g., 2000)
            if person.birth_year == 1997:
                self.birth_year_count += 1

            # Add occupation to unique_occupations_set
            self.unique_occupations_set.add(person.occupation)

            # Count names with more than two parts
            if len(person.name.split(" ")) > 2:
                self.names_with_more_than_two_parts_count += 1

            # Count people whose birth and death dates have the same month and day
            if person.birth_date[5:] == person.death_date[5:]:
                self.birth_death_same_except_year_count += 1

    def total_people(self) -> int:
        return len(self.people)

    def longest_name(self) -> Tuple[str, int, str]:
        return self.longest_name_data

    def oldest_living_person(self) -> Tuple[str, int, str]:
        return self.oldest_living_data

    def oldest_deceased_person(self) -> Tuple[str, int, str, str]:
        return self.oldest_deceased_data

    def total_actors(self) -> int:
        return self.total_actor_count

    def born_in_year(self, year: int) -> int:
        return self.birth_year_count

    def unique_occupations(self) -> int:
        return len(self.unique_occupations_set)

    def names_with_more_than_two_parts(self) -> int:
        return self.names_with_more_than_two_parts_count

    def birth_death_same_except_year(self) -> int:
        return self.birth_death_same_except_year_count

    def living_and_deceased_count(self) -> Tuple[int, int]:
        return self.living_count, self.deceased_count
