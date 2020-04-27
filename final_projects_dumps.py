import json
import sqlite3

def main():
    conn = sqlite3.connect('Project.db') 
    c = conn.cursor() 
if __name__ == '__main__':
    main()