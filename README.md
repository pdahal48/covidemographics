# COVID-API
This site provides a one stop access to county demographics and covid cases. Data used on this project are extracted from covidactnow.org and US Census Bureau API

Here is the tentative schema model. county_code will be used as a FOREIGN Key in all three of county demographics table. joint_code will be used to access covid information regarding a specific county. 
____
Table to store general location information for API accessibility

|id|county|state|__county_code__|state_code|__joint_code__
|--|------|-----|-----------|----------|----------
|1|Butler|OH|017|39|39017
___
___
 Although this information will not be saved in our database because of the file size, here is what I will be grabbing from the COVIDACTNOW API
 
  |id|__joint_code__|cases|deaths|date|
  |--|------|-----|-----------|----
  |1|39017|34548|452|02-18-2021

  For states comparision. I will also be extracting covid information in state level such as cases, deaths, case density, and risk level. 
 ____
 ____
 Three separate tables will be used to county demographics.
 1. Number of people with at least a bachelors degree
 
  |id|__county_code__|__state_code__|education(%)
  |--|-----------|-----------|--------
  |1|017|39|150000
  
 2. Population and Population density (ppl/sq mi)

  |id|**county_code**|__state_code__|pop|pop_den
  |--|-----------|---|-------|------
  |1|017|39|383134|815

3. Poverty: measures the % of people living under the poverty threshold

  |id|**county_code**|**state_code**|pov|
  |--|-----------|---|--------
  |1|017|39|11
 ____
