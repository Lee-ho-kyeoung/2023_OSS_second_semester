import pynecone as pc
from typing import Optional
from sqlmodel import Field


class Regions(pc.Model, table=True):
    """A table of Regions"""

    region_id: int
    name: str
    continent_id: int

class Region_Areas(pc.Model, table=True):
    """A table of Regions"""

    region_name: str
    region_area: float

class Continents(pc.Model, table=True):
    """A table of Continents"""

    continent_id: int
    name: str

class Languages(pc.Model, table=True):
    """A table of Languages"""

    language_id: int
    language: str

class Countries(pc.Model, table=True):
    """A table of Countries."""

    country_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    area: float
    national_day: str
    country_code2 : str
    country_code3: str
    region_id: int

class Country_Languages(pc.Model, table=True):
    """A table of Country Language"""

    country_id: int = Field(default=None, foreign_key="Countries.country_id")
    language_id:int
    official: int

class Country_Stats(pc.Model, table=True):
    """A table of Country Stats"""

    country_id: int
    year: int
    population: int
    gdp: float
