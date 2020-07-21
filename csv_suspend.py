#!/usr/bin/python3

import csv, datetime, getopt, os, sys

def logo():
    print('''
##############################################################
##############################################################
#
# PYTHON 3
# BATCH USER SUSPENSION SCRIPT v0.2
#
# Created by: Andrew Sturm
# Created on: 2020-07-20
#
##############################################################
##############################################################

This script will go through the process of suspending an account from a batch file.

The CSV is generated by the command: 'gam print users lastlogintime suspended todrive'.

From there, File > Download > CSV and point this program to that path.
''')

def main(argv):
    # Variables
    choice = ""
    emails = []
    gam = "/root/bin/gam/gam"
    today = datetime.datetime.now()

    # Check for the correct arguments
    try:
        opts, args = getopt.getopt(argv,"d:hi:vy",["days","help","input","version","yes"])
    except getopt.GetoptError:
        print("Invalid argument.\n\nUsage: csv_suspend.py -d days -i file")
        exit()

    # Get opt cases
    for opt, arg in opts:
        if opt in ("-h","--help"):
            print("Usage: csv_suspend.py -d days -i file")
            print("The CSV is generated by the command: 'gam print users lastlogintime suspended todrive'.")
            print("From there, File > Download > CSV and point this program to that path.")
            exit()
        elif opt in ("-d","--days"):
            days = arg
        elif opt in ("-i","--input"):
                try:
                    with open(arg, newline='') as csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            email = row['primaryEmail']
                            lastLogin = row['lastLoginTime']
                            suspended = row['suspended']

                            # Today minus the 'days' variable
                            if lastLogin != "Never":
                                if suspended == "FALSE":
                                    # Properly format both dates for comparison
                                    dateLogin = datetime.datetime.strptime(lastLogin, '%Y-%m-%dT%H:%M:%S.%fZ')
                                    dateToday = today - datetime.timedelta(days=int(days))

                                    if dateToday >= dateLogin:
                                        emails.append(email)
                                    elif today < dateLogin:
                                        print(str(today)+" is less than "+str(dateLogin)+". Something may be wrong...")

                except KeyboardInterrupt:
                    print("Keyboard interrupt signal detected.\nExiting...")
                    exit()
        elif opt in ("-v","--version"):
            logo()
            exit()
        elif opt in ("-y","--yes"):
            choice = 'y'

    # Check with user before suspending
    if choice == '':
        print(emails)
        choice = input("The above accounts will all be suspended. Do you wish to continue? [y/N]")
        if choice.lower() == "y":
            for row in emails:
                cmd = (gam+" update user "+row+" suspended on")
                os.system(cmd)
        else:
            exit()

# Start the main loop
if __name__ == "__main__":
    main(sys.argv[1:])
