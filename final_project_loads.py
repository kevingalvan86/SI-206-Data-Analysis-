# Final Project: COVID-19 Data
# name: Kevin Felipe Galvan
# email:kevgal@umich.edu
# name: Hiram Rodriguez
# email: hiramr@umich.edu
import requests
import json
import sqlite3
import csv
from pytrends.request import TrendReq
import pandas as pd

pytrends = TrendReq(hl='en-US', tz=360)

def get_covid_info():

    url = "https://api.covid19api.com/summary"
    payload = {}
    headers= {}
    response = requests.request("GET", url, headers=headers, data = payload)
    dic = json.loads(response.text)
    return dic

def get_global_info(field_names):
    url = r"https://restcountries.eu/rest/v2/all?fields="
    for name in field_names:
        url = url + name + ";"
    r = requests.request("GET", url[:-1])
    l = json.loads(r.text)
    return l

def get_google_trends():
    kw_list = ["COVID-19"]
    pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')

    df = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
    df = df.to_csv('google_info.csv')
    return df

def main():
    conn = sqlite3.connect('Project.db') 
    c = conn.cursor() 
    c.execute('''CREATE TABLE IF NOT EXISTS Region (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 
    "Name" TEXT UNIQUE
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS Country  (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 
	"Name" TEXT UNIQUE,
    "Population" INT,
	"Region" INT,
    FOREIGN KEY ("Region") REFERENCES Region("id")
	)''')
    c.execute('''create table if not exists Google (
    "ID" integer primary key AUTOINCREMENT not null UNIQUE,
    "Value" INT,
    "Country" INT,
    FOREIGN KEY ("Country") REFERENCES Country("id"))''')
    c.execute('''CREATE TABLE IF NOT EXISTS Covid (
    "ID" integer primary key AUTOINCREMENT not null UNIQUE,
    "Cases" INT,
    "Deaths" INT,
    "Country" INT,
    "Region" INT,
    FOREIGN KEY ("Country", "Region") REFERENCES Country("id", "Region"))''')
    conn.commit()
    count = 0
    region_list = get_global_info(["region"])
    country_list = get_global_info(["name", "population","region"])
    covid_dic = get_covid_info()
    for region in region_list:
        c.execute("select id from Region where name = ?", (region['region'], ))
        try:
            existing = c.fetchone()[0]
            print("Found in database ",existing)
            continue
        except: 
            pass
        c.execute('''INSERT OR IGNORE INTO Region (name) VALUES (?)''',(region['region'], ))
        conn.commit()
        count += 1
        if count == 20:
            print("20 items have been added to the Database")
            break
    if count == 20:
        pass
    else:
        for country in country_list:
            c.execute("SELECT id FROM Country WHERE Name = ?", (country["name"], ))
            try:
                existing = c.fetchone()[0]
                print("Found in database ",existing)
                continue
            except: 
                pass
            c.execute("SELECT id From Region WHERE Name = ?", (country['region'],))
            region_shared_key = c.fetchone()
            region_id = region_shared_key[0]
            c.execute('''INSERT OR IGNORE INTO Country (Name, Population, "Region") VALUES (?, ?, ?)''', (country['name'], country['population'], 
            region_id))
            conn.commit()
            count += 1
            if count == 20:
                print("20 items have been added to the Database")
                break
    if count == 20:
        pass
    else:
        for country in covid_dic["Countries"]:
            c.execute("SELECT id FROM Country WHERE Name = ?", (country['Country'], ))
            try:
                c_id = c.fetchone()[0]
                print("Name found in country table", c_id)
            except:
                continue
            c.execute("SELECT ID FROM Covid WHERE Country = ?", (c_id, ))
            try:
                exists = c.fetchone()[0]
                print("Country Already in Covid Table", exists)
                continue
            except:
                pass
            c.execute("SELECT Region FROM Country WHERE id = ?", (c_id, ))
            r_id = c.fetchone()[0]
            confirmed = country['TotalConfirmed']
            deaths = country['TotalDeaths']
            c.execute('''INSERT OR IGNORE INTO Covid (Cases, Deaths, Country, Region) Values (?,?,?,?)''', (confirmed, deaths, c_id, r_id))
            conn.commit()
            count += 1
            if count == 20:
                print("20 Items have been added to the Database Table Covid")
                break
    csv_file = get_google_trends()
    trends = open('google_info.csv', 'r')
    if count == 20:
        pass
    else:
        for row in trends:
            row = row.split(",")
            c.execute("SELECT id FROM Country WHERE Name = ?", (row[0], ))
            try:
                c_id = c.fetchone()[0]
                print("Name found in country table", c_id)
            except:
                continue
            c.execute("SELECT ID FROM Google WHERE Country = ?", (c_id, ))
            try:
                exists = c.fetchone()[0]
                print("Country Already in Google Table", exists)
                continue
            except:
                pass
            c.execute('''INSERT OR IGNORE INTO Google (Value, Country) Values (?, ?)''' ,(row[1],c_id ))
            conn.commit()

            count += 1
            if count == 20:
                print("20 items added to Database Table Google")
                break
    trends.close()

if __name__ == '__main__':
    main()
