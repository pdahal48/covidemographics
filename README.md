# CoviDemographics
Covidemographics site provides a one stop access to county demographics and covid cases. Data used on this project are extracted from COVIDACTNOW.ORG and US Census Bureau API
As I analyzed covid data, I always wonder about the factors that could be driving covid cases in one county vs the other. On this site, Users can not only see the covid cases and deaths but also view county demographics including population, population density, poverty (%), and % of people with at least a bachelor's degree.

## User-Flow
Site is default to Los Angeles County, California. User have an option to change the location using the Select Fields on the field. 
___
List of APIs
- ED_API = https://api.census.gov/data/2019/acs/acsse?get=NAME,K201501_007E&for=county:{county}&in=state:{state}&key=9459a79ef95b98b7009a83c5ba3d94c682f72e50
- POP_API = https://api.census.gov/data/2019/pep/population?get=DENSITY,POP&for=county:{county}&in=state:{state}&key=9459a79ef95b98b7009a83c5ba3d94c682f72e50
- POV_API = https://api.census.gov/data/timeseries/poverty/saipe?get=NAME,SAEPOVRTALL_PT&for=county:{county}&in=state:{state}&key=9459a79ef95b98b7009a83c5ba3d94c682f72e50
- COVID_API = https://api.covidactnow.org/v2/states.json?apiKey=b28cd827fcb9481db77660ed3eee9157

___
Here is the schema model. joint_code will be used to access covid information regarding a specific county. 
____
Table to store general location information for API accessibility.

|id|county|state|__county_code__|state_code|__joint_code__
|--|------|-----|-----------|----------|----------
|1|Butler|OH|017|39|39017
___

A table will also be stored in the DATABASE with state's fips code and state abbreviations for access to COVID API. 
|id|state|state_abb|
|--|------|-----|
|1|39|OH

___
 Although this information will not be saved in our database because of the file size, here is what I will be grabbing from the COVIDACTNOW API
 
  |id|__joint_code__|cases|deaths|date|
  |--|------|-----|-----------|----
  |1|39017|34548|452|02-18-2021

  For states comparision. I will also be extracting covid information in state level such as cases, deaths, case density, and risk level. 
 ____
 ____
 
  For county demographics information, site will be make a direct request to the API. 
