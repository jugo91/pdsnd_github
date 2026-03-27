#### Code for udactiy bike share project
## Author: Ingo Paschke

import time
from datetime import datetime
import pandas as pd
import numpy as np
import os

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    while city == "":
        city = input('Type a city you want to filter: chicago, new york city, washington.\n')
        city = str(city).lower()
        if city in ['chicago', 'new york city', 'washington']:
            print('Success. You chose '+city+".")
            if city == "new york city":
                city = "new_york_city"
        else:
            city = ""
            print("Please choose any of the given cities. The orthography must match.")


    # get user input for month (all, january, february, ... , june)
    month = ""

    while month == "":
        month = input('Type a month you want to filter: all, january, february, ... , june.\n')
        month = str(month).lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may' , 'june']:
            print('Success. You chose '+month+".")
        else:
            month = ""
            print("Please choose any of the given months. The orthography must match.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    while day == "":
        day = input('Type a day you want to filter: all, monday, tuesday, ... sunday.\n')

        day = str(day).lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday' ,'sunday']:
            print('Success. You chose '+day+".")
        else:
            month = ""
            day("Please choose any of the given days. The orthography must match.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day

    """
    #create dictonaries for mapping of month and day independent of locale


    file_path = './'+city+'.csv'

    if os.path.exists(file_path):
        print("The file exists.")
    else:
        print("The file "+file_path+" does not exist. Please check your directory.")
        


    df = pd.read_csv(file_path)

    #Display raw data if user whishes so


    raw = ""
    raw = input('Do you want to see the first 5 lines of raw data? Please answer with \'yes\' or \'no\'..\n')
    raw = str(raw).lower()
    if raw in ['yes', 'no']:
        print('Success. You chose '+raw+".")
    i=0
    while (raw == "yes") & (i< len(df.index)):
        print(df[i:min(i+5,len(df.index))])
        raw = input('Do you want to see five more lines of raw data? Please answer with \'yes\' or \'no\'..\n')
        raw = str(raw).lower()
        if raw in ['yes', 'no']:
            print('Success. You chose '+raw+".")
            if raw == "yes":
                i=i+5
        else:
            raw = "yes"
            day("Please choose yes or no.")

    #Date time transformations before filtering
    df['Start Time']= df['Start Time'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S" ))
    df['Start Hour'] = df['Start Time'].apply(lambda x: datetime.strftime(x,'%H'))
    df['Month'] = df['Start Time'].apply(lambda x: datetime.strftime(x,'%B').lower())
    df['Weekday'] = df['Start Time'].apply(lambda x: datetime.strftime(x,'%A').lower())
    df['Start and End Station'] = df['Start Station'].apply(lambda x: x+" and ")+ df["End Station"]

    #filter Month and Weekday, if not 'all' is demanded, respectively

    if month != 'all':
        df = df[df['Month']==month]


    if day != 'all':
        df = df[df['Weekday']==day]

    print(df.head())

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is: "+df['Month'].value_counts().index[0])



    # display the most common day of week
    print("The most common day of the week is: "+(df['Weekday'].value_counts().index[0]))


    # display the most common start hour
    print("The most common start hour is: "+df['Start Hour'].value_counts().index[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is: "+df['Start Station'].value_counts().index[0])


    # display most commonly used end station

    print("The most commonly used end station is: "+df['End Station'].value_counts().index[0])


    # display most frequent combination of start station and end station trip

    print("The most frequent combination of start station and end station trip is:  "+df['Start and End Station'].value_counts().index[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time: "+str(df["Trip Duration"].sum())+" seconds")


    # display mean travel time
    print("Mean travel time: "+str(df["Trip Duration"].mean())+" seconds")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    #,User Type,Gender,Birth Year

    # Display counts of user types    
    print('\nThe following user types in those frequencies exist:\n')    
    print(df['User Type'].value_counts())


    # Display counts of gender
    if "Gender" in df.columns:
        print('\nThe following genders in those frequencies exist:\n')    
        print(df['Gender'].value_counts())
    else: print("Gender not in data. Nothing to show here.")


    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        print("The most recent year of birth is: "+str(df['Birth Year'].dropna().sort_values().iloc[-1]))
        print("The earliest year of birth is: "+str(df['Birth Year'].dropna().sort_values().iloc[0]))
        print("The most common year of birth is: "+str(df['Birth Year'].dropna().value_counts().index[0]))
    else: print("Birth Year not in data. Nothing to show here.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
