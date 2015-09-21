#!/usr/bin/python

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost", "ckgathi", "thabo321", "updatedb")

# prepare a cursor object using cursor() method
cursor = db.cursor()

try:
    r_file = open("household.txt", "r")
    r_line = r_file.readline()
    while r_line:
        r_line = r_line.split("|")
        identifier = r_line[0]
        lon = r_line[1]
        lat = r_line[2]
        print identifier
        print lon
        print lat
        print "*************"
        r_line = r_file.readline()
        # Execute the SQL command
        cursor.execute("""
       UPDATE mochudi_household
       SET lon=%s, lat=%s
       WHERE  identifier=%s
    """, (lon, lat, identifier))
    # Commit your changes in the database
    db.commit()
except:
    # Rollback in case there is any error
    db.rollback()
# disconnect from server
db.close()
r_file.close()
