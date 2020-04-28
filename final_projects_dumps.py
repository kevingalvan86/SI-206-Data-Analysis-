# Final Project: COVID-19 Data
# name: Kevin Felipe Galvan
# email:kevgal@umich.edu
# name: Hiram Rodriguez
# email: hiramr@umich.edu


import json
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
def main():
    conn = sqlite3.connect('Project.db') 
    c = conn.cursor() 
    c.execute('''SELECT Country.Name, Region.Name, Covid.Cases, Covid.Deaths, Country.Population,
    Google.Value FROM Covid JOIN Country JOIN Google JOIN Region ON
    (Covid.Country = Country.id AND 
    Google.Country = Covid.Country AND 
    Region.id = Covid.Region)''')
    data = c.fetchall()
    c.execute("SELECT Region.Name From Region")
    region_names = c.fetchall()
    data_dict = {}
    asia_pop = 0
    asia_cases = 0 
    asia_deaths = 0
    asia_trend = 0
    europe_pop = 0
    europe_cases = 0
    europe_deaths = 0
    europe_trend = 0
    africa_pop = 0
    africa_cases = 0
    africa_deaths = 0
    africa_trend = 0
    oceania_pop = 0
    oceania_cases = 0
    oceania_deaths = 0
    oceania_trend = 0 
    americas_pop = 0
    americas_cases = 0
    americas_deaths= 0
    americas_trend = 0
    polar_pop = 0
    polar_cases = 0
    polar_deaths=0
    polar_trend = 0
    for tup in region_names[:-1]:
        data_dict[tup[0]] = {}
    for region in data_dict:
        for tup in data:
            if tup[1] == region:
                data_dict[region][tup[0]] = {"Cases" : tup[2], "Deaths" : tup[3], "Population" : tup[4], "Google Trend" : tup[5]}
    calc_dict = {}
    for tup in data:
        if tup[1] == 'Asia':
            asia_pop += tup[4]
            asia_cases += tup[2]
            asia_deaths += tup[3]
            asia_trend += tup[5]
        if tup[1] == 'Americas':
            americas_pop += tup[4]
            americas_cases += tup[2]
            americas_deaths += tup[3]
            americas_trend += tup[5]
        if tup[1] == 'Oceania':
            oceania_pop += tup[4]
            oceania_cases += tup[2]
            oceania_deaths += tup[3]
            oceania_trend += tup[5]
        if tup[1] == 'Europe':
            europe_pop += tup[4]
            europe_cases += tup[2]
            europe_deaths += tup[3]
            europe_trend += tup[5]
        if tup[1] == 'Africa':
            africa_pop += tup[4]
            africa_cases += tup[2]
            africa_deaths += tup[3]
            africa_trend += tup[5]
        if tup[1] == 'Polar':
            polar_pop += tup[4]
            polar_cases += tup[2]
            polar_deaths += tup[3]
            polar_trend += tup[5]

    for tup in region_names[:-1]:
        if tup[0] == 'Asia':
            calc_dict[tup[0]] = {"Population": asia_pop, "COVID-19 Cases" : asia_cases, "COVID-19 Deaths" : asia_deaths, "Google Trend Total": asia_trend}
        if tup[0] == 'Americas':
            calc_dict[tup[0]] = {"Population": americas_pop, "COVID-19 Cases" : americas_cases, "COVID-19 Deaths" : americas_deaths, "Google Trend Total": americas_trend}
        if tup[0] == 'Oceania':
            calc_dict[tup[0]] = {"Population": oceania_pop, "COVID-19 Cases" : oceania_cases, "COVID-19 Deaths" : oceania_deaths, "Google Trend Total": oceania_trend}   
        if tup[0] == 'Europe':
            calc_dict[tup[0]] = {"Population": europe_pop, "COVID-19 Cases" : europe_cases, "COVID-19 Deaths" : europe_deaths, "Google Trend Total": europe_trend}
        if tup[0] == 'Africa':
            calc_dict[tup[0]] = {"Population": africa_pop, "COVID-19 Cases" : africa_cases, "COVID-19 Deaths" : africa_deaths, "Google Trend Total": africa_trend}
        if tup[0] == 'Polar':
            calc_dict[tup[0]] = {"Population": polar_pop, "COVID-19 Cases" : polar_cases, "COVID-19 Deaths" : polar_deaths, "Google Trend Total": polar_trend}

    json.dumps(calc_dict)
    json.dumps(data_dict)
    with open("Calculation_File", "w") as f:
        f.write("CALCULATIONS\n\n\n")
        json.dump(calc_dict, f, indent=3)
        f.write("\n\nData per Country\n\n")
        json.dump(data_dict, f, indent=3)
    names = []
    totals = []
    cases = []
    deaths = []
    for region in region_names[:-1]:
        print(calc_dict[region[0]])
        names.append(region[0])
        totals.append(calc_dict[region[0]]['Population'])
        cases.append(calc_dict[region[0]]['COVID-19 Cases'])
        deaths.append(calc_dict[region[0]]['COVID-19 Deaths'])
    ypos = np.arange(len(names))
    plt.bar(ypos, totals, align='center', alpha=0.5)
    plt.xticks(ypos, names)
    plt.ylabel('Population')
    plt.xlabel('Regions')
    plt.title('Population per Region')
    plt.savefig('Population.png')
    index = np.arange(len(names))
    fig, ax = plt.subplots()
    bar_width = 0.35
    opacity = 0.8

    plt.bar(index, cases, bar_width,
    alpha=opacity, color='b', label='Cases')

    plt.bar(index + bar_width, deaths, bar_width,
    alpha=opacity,color='g',label='Deaths')
    plt.xlabel('Region')
    plt.ylabel('Amount of People')
    plt.title('COVID-19 Data by Region')
    plt.xticks(index + bar_width, names)
    plt.legend()
    plt.tight_layout()
    plt.savefig('COVID.png')

    

    

if __name__ == '__main__':
    main()