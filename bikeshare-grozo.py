#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#month-list to be used in the project
months=['all','january', 'february', 'march', 'april', 'may','june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs


    #If cities is not in the list of valid cities requires a new city
    city=""
    while city not in ['chicago','new york city', 'washington']:
        if city!="":
            print("Invalid city, please introduce one of the options provided.")
        city=input('Introduce the city you want to explore (chicago, new york city, washington):').lower()

    # TO DO: get user input for month (all, january, february, ... , june)

    month=""
    #If month is not in the list of valid months requires a new month
    while month not in months:
        if month!="":
            print("Invalid month, introduce one from the options provided.")
        month=input("Introduce the month you want to analyze ('all','january', 'february', 'march', 'april', 'may','june'):").lower()


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    #If day is not in the list of valid months requires a new day
    day=""
    while day.lower() not in ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday','sunday']:
        if day!="":
            print("\nInvalid day, introduce one from the options provided.\n")
        day=input("Introduce the day of the week you want to analyze ('all','monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday','sunday'):").lower()


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
    #from CITY DATA dictionary we get the filename
    filename=CITY_DATA[city]
    df=pd.read_csv(filename)

    #format Start Time as datetime

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month

    #On Python 3 day_name() and Python 2.7 or previous weekday_name
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months=['january','february','march','april','may','june']
        # filter by month to create the new dataframe
        month=months.index(month)+1
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month

    #Get the month number and then look for the name in the month list
    popular_month=months[df['month'].mode()[0]].title()
    print('The most popular month is: {}'.format(popular_month))

    # TO DO: display the most common day of week

    popular_dow=df['day_of_week'].mode()[0]

    print('The most popular day of week is: {}'.format(popular_dow))

    # TO DO: display the most common start hour
    df['hour']=df['Start Time'].dt.hour
    popular_hour=df['hour'].mode()[0]
    print('The most popular hour is: {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station

    popular_start_station=df['Start Station'].mode()[0]
    print('The most popular start station is: {}'.format(popular_start_station))

    # TO DO: display most commonly used end station

    popular_end_station=df['End Station'].mode()[0]
    print('The most popular end station is: {}'.format(popular_end_station))


    # TO DO: display most frequent combination of start station and end station trip

    #Create trip variable and then find the mode
    df['Trip']=df['Start Station']+' - '+df['End Station']
    popular_trip=df['Trip'].mode()[0]
    print('The most popular trip is: {}'.format(popular_trip))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time


    #Calculate the total travel time in minutes

    total_travel_time=np.round(df['Trip Duration'].sum()/60,2)
    print('The total travel time has been: {} minutes'.format(total_travel_time))

    # TO DO: display mean travel time
    #Calculate the mean travel time in minutes

    mean_travel_time=np.round(df['Trip Duration'].mean()/60,2)
    print('The average travel time has been: {} minutes'.format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("The number of travels per user type has been:\n{}".format(df['User Type'].value_counts()))
    print("\n")

    #Check if Gender it a variable in the dataframe, if it isn't we are in the washington database and we cannot
    #have results for gender and year of birth

    try:
        # TO DO: Display counts of gender

        valcounts=df['Gender'].value_counts()

        print("The number of travels per gender has been:\n{}".format(valcounts))
        print("\n")

    # TO DO: Display earliest, most recent, and most common year of birth
        earliest=int(df['Birth Year'].min())
        recent=int(df['Birth Year'].max())
        common=int(df['Birth Year'].mode()[0])

        print("The earliest year of birth is: {}".format(earliest))
        print("The most recent year of birth is: {}".format(recent))
        print("The most common year of birth is: {}".format(common))

    except:
        #When there is an exception respond that we cannot provide data for Gender and Year of birth for washington
        print("Gender and year of birth not provided for washington\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def IndividualData(df):

    #Given a data frame asks the user if he wants to see individual data in shunks of 5 for as long as the user requires

    start_loc = 0
    view_display = input("Would you like to see individual data? (Enter yes/no): ").lower()

    while (view_display not in ["yes", "no"]):
        view_display=input("Invalid answer. Would you like to continue seeing more data? Enter yes/no:").lower()


    while view_display=="yes":
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_display = input("Do you wish to continue seeing more data? (Enter yes/no): ").lower()
        while (view_display not in ["yes", "no"]):
            view_display=input("Invalid answer. Would you like to continue seeing more data? Enter yes/no:").lower()



def main():

    #The routine runs in the following order:
    #1. The user is asked for city, month and day inputs
    #2. The data required is loaded
    #3. All the stats are calculated from the data loaded
    #4. The user is asked if she wants to see individual data.

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        IndividualData(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
