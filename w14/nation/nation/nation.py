"""Welcome to Pynecone! This file shows nations stats."""
import pynecone as pc
from pynecone import utils # logging

from .base_state import Countries, Languages, Country_Languages, Regions, Continents, Country_Stats
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


country_list = []
  
with pc.session() as session:
    countries = session.query(Countries.name, Countries.country_id).all()

country_dicts = {country[0]:country[1] for country in countries}
country_list = list(country_dicts.keys())


class NationState(pc.State):
    country: str = "South Korea"

    @pc.var
    def country_id(self) -> int:
        return country_dicts[self.country]

    @pc.var
    def language_dict(self) -> dict:
        with pc.session() as session:
            language_dict = session.query(Languages.language, Country_Languages.official)\
                .filter(Languages.language_id == Country_Languages.language_id)\
                .filter(Country_Languages.country_id == self.country_id)\
                .all()                
        
        language_dict = {language[0]:language[1] for language in language_dict}
        return language_dict

    @pc.var
    def languages(self) -> list:
        languages = list(self.language_dict.keys())
        return languages
    
    @pc.var
    def official_languages(self) -> list:
        official_languages = []
        for (k, v) in self.language_dict.items():
            if v:
                official_languages.append(k)
        return official_languages
    
    @pc.var
    def non_official_languages(self) -> list:
        non_official_languages = []
        for (k, v) in self.language_dict.items():
            if not v:
                non_official_languages.append(k)
        return non_official_languages

    @pc.var
    def region(self) -> str:

        with pc.session() as session:
            region = session.query(Regions.name)\
                .join(Countries, Countries.region_id == Regions.region_id)\
                .filter(Countries.country_id == self.country_id)\
                .first()
        return region[0]
           
    @pc.var
    def continent(self) -> str:

        with pc.session() as session:
            continent = session.query(Continents.name)\
                .join(Regions, Regions.continent_id == Continents.continent_id)\
                .outerjoin(Countries, Countries.region_id == Regions.region_id)\
                .filter(Countries.country_id == self.country_id)\
                .first()
        return continent[0]

    @pc.var
    def area(self) -> float:

        with pc.session() as session:
            area = session.query(Countries.area).where(Countries.country_id == self.country_id).first()
        return area[0]
    
    @pc.var
    def national_day(self) -> str:

        with pc.session() as session:
            national_day = session.query(Countries.national_day).where(Countries.country_id == self.country_id).first()
        if national_day[0]:
            return str(national_day[0])
        else:
            return "데이터없음"
        
    @pc.var
    def population(self) -> list:

        with pc.session() as session:
            population_list = session.query(Country_Stats.year, Country_Stats.population)\
                .where(Country_Stats.country_id == self.country_id)\
                .order_by(Country_Stats.year.asc())\
                .all()
            
        population_list = [{"Year":pop[0], "Population":pop[1]} for pop in population_list]
        if population_list:
            return population_list
        else:
            # utils.console.print(f'population_list is empty')
            return []

    @pc.var
    def population_line(self) -> go.Figure:
        """The line figure."""
 
        if not self.population:
            # utils.console.print(f'self.population is empty')
            return go.Figure()
        else:
            population_df = pd.DataFrame(self.population)
            population_df.columns = ["Year", "Population"]
            return px.line(
                population_df,
                x="Year",
                y="Population",          
                title="Population/Year plot",
            )

    @pc.var
    def last_population(self):
        if self.population:
            return str(self.population[-1])
        else:
            return "데이터 없음"

    @pc.var
    def gdp(self) -> list:
        with pc.session() as session:
            gdp_list = session.query(Country_Stats.year, Country_Stats.gdp)\
                .where(Country_Stats.country_id == self.country_id)\
                .order_by(Country_Stats.year.asc())\
                .all()
        gdp_list = [{"Year":gdp[0], "GDP":gdp[1]} for gdp in gdp_list]
        # utils.console.print(f'gdp_list : {gdp_list}')
        if gdp_list:
            return gdp_list
        else:
            # utils.console.print(f'gdp_list is empty')
            return []
        
    @pc.var
    def gdp_line(self) -> go.Figure:
        """The line figure."""
 
        if not self.gdp:
            # utils.console.print(f'self.gdp is empty')
            return go.Figure()
        else:
            # utils.console.print(f'self.gdp else : {self.gdp}')
            gdp_df = pd.DataFrame(self.gdp)
            return px.line(
                gdp_df,
                x="Year",
                y="GDP",           
                title="GDP/Year plot",
            )

    @pc.var
    def last_gdp(self):
        if self.gdp:
           return str(self.gdp[-1])
        else:
            return "데이터 없음"


def selection():
    return pc.vstack(
        pc.select(
            country_list,
            placeholder="Select a country.",
            on_change=NationState.set_country,
        ),
        align_items="left",
        width="100%",
        spacing="1em",
    )

def get_lang(lang):
    return pc.list_item(lang)

def index():
    "The main view."
    utils.console.print('index started -----')
    utils.console.print(f'index NationState languages : {NationState.language_dict}')
    return pc.center(
        pc.vstack(
            selection(),
            pc.divider(),            
            pc.heading(NationState.country),
            pc.divider(),
            pc.hstack(
                pc.vstack(
                    pc.heading('사용언어', size="md"),
                    pc.divider(),
                    pc.heading('공식언어', size="sm"),
                    pc.divider(),
                    pc.list(
                        pc.foreach(
                            NationState.official_languages,
                            lambda language: pc.list_item(language),
                        )
                    ),
                    pc.divider(),
                    pc.heading('비공식언어', size="sm"),
                    pc.divider(),
                    pc.list(
                        pc.foreach(
                            NationState.non_official_languages,
                            lambda language: pc.list_item(language),
                        )
                    ),
                    width="10%"
                ),
                pc.vstack(
                    pc.heading('주요정보', size="md"),
                    pc.divider(),
                    # 대륙, 리전, 면적, 국경일, 최근인구, 최근 gdp
                    pc.box(
                        "대륙 : ",
                        pc.span(NationState.continent, color="red"),
                    ),
                    pc.box(
                        "리전 : ",
                        pc.span(NationState.region, color="blue"),
                    ),
                    pc.box(
                        "면적 : ",
                        pc.span(NationState.area, color="green"),
                    ),
                    pc.box(
                        "국경일 : ",
                        pc.span(NationState.national_day, color="red"),
                    ),
                    pc.box(
                        "최근인구 : ",
                        pc.span(NationState.last_population),
                    ),
                    pc.box(
                        "최근GDP : ",
                        pc.span(NationState.last_gdp),
                    ),
                    align_items="left",
                    width="20%",
                ),
                pc.vstack(
                    pc.heading('인구그래프', size="md"),
                    pc.divider(),
                    pc.plotly(data=NationState.population_line, layout={"width": "500", "height": "400"}),
                ),
                pc.vstack(
                    pc.heading('GDP그래프', size="md"),
                    pc.divider(),
                    pc.plotly(data=NationState.gdp_line, layout={"width": "500", "height": "400"}),
                ),
                align_items="up",
                spacing="2em",
                width="100%",
            ),
            width="100%",
        ),
        padding_top="6em",
        width="100%",
    )

# Add state and page to the app.
app = pc.App(state=NationState)
app.add_page(index)
app.compile()