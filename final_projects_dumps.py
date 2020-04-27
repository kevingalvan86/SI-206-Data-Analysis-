import json
import sqlite3

def main():
    conn = sqlite3.connect('Project.db') 
    c = conn.cursor() 
    c.execute('''SELECT Country.Name, Region.Name, Covid.Cases, Covid.Deaths, Country.Population
    Google.Value FROM Covid JOIN Country JOIN Google JOIN Region ON
    (Covid.Country = Country.id AND 
    Google.Country = Covid.Country AND 
    Region.id =
     Covid.
     Region)''')
    print(c.fetchall())
if __name__ == '__main__':
    main()