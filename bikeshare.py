import time
import pandas as pd
import numpy as np

#Creating a dictionary containing the data sources for the three cities
CITY_DATA = { 'chicago': 'data/chicago.csv','New york city': 'data/new_york_city.csv',
               'washington': 'data/washington.csv', }

#Function to figure out the filtering requirements of the user
def get_filter():
    """
    Asks user to specify a city, month, and day to analyze.
    Args:
        None.
    Returns:
        str (city): name of the city to analyze
        str (month): name of the month to filter by, or "all" to apply no month filter
        str (day): name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    #an empty city variable to store entry from user
    city = ''
    
    while city not in CITY_DATA.keys():
        print("\nWelcome to this program. Please select a city to get started: ")
        print("\n1. Chicago 2. New York City 3. Washington")
        print("\nLower and upper case entry accepted.")
        
        city = input().lower()

        if city not in CITY_DATA.keys():
            print("\nIt seems you entered a wrong entry. Please check your entry and try again.")
            print("\nRestarting...")

    print(f"\nYou have chosen {city.title()} as your city.")

    
    
    #this dictionary to store all the months including the 'all' option. If a user enters 'all', it pulls out all data for every months
    MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    month = ''
    while month not in MONTH_DATA.keys():
        print("\nPlease enter any month (between January and June) of your choice to show the data:")
        print("\nAccepted input:\nFull month name; not case sensitive (e.g. january or JANUARY).\nFull month name in title case (e.g. April).")
        print("\n(You may also opt to view data for all months, please type 'all' or 'All' or 'ALL' for that.)")
        month = input().lower()

        if month not in MONTH_DATA.keys():
            print("\nInvalid input. Please check your entry and try again.")
            print("\nRestarting...")

    print(f"\nYou have chosen {month.title()} as your month.")

     
    DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ''
    while day not in DAY_LIST:
        print("\nPlease enter a day in the week to see data:")
        print("\nUpper or lowcase entry excepted.(Ex. 'Sunday or SUNDAY').")
        print("\n(To see all data for the week, enter 'all' or 'All'.)")
        day = input().lower()

        if day not in DAY_LIST:
            print("\nInvalid input. Please check your entry and try again.")
            print("\nRestarting...")

    print(f"\nYou have chosen {day.title()} as your day.")
    print(f"\nYou have chosen to view data for city: {city.upper()}, month/s: {month.upper()} and day/s: {day.upper()}.")
    print('-'*80)
    #Returning the city, month and day selections
    return city, month, day


#Function to load data from .csv files
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        param1 (str): name of the city to analyze
        param2 (str): name of the month to filter by, or "all" to apply no month filter
        param3 (str): name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df: Pandas DataFrame containing city data filtered by month and day
    """
    #Load data for city
    print("\nLoading data...")
    df = pd.read_csv(CITY_DATA[city])

    #Converting the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    
    df['day_of_week'] = df['Start Time'].dt.day_name()

    #Filter by month if applicable
    if month != 'all':
        #Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #Filter by month to create the new dataframe
        df = df[df['month'] == month]

    #Filter by day of week if applicable
    if day != 'all':
        #Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    #Returns the selected file as a dataframe (df) with relevant columns
    return df

#Function to calculate all the time-related statistics for the chosen data
def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Uses mode method to find the most popular month
    popular_month = df['month'].mode()[0]

    print(f"Most Popular Month (1 = January,...,6 = June): {popular_month}")

    #Uses mode method to find the most popular day
    popular_day = df['day_of_week'].mode()[0]

    print(f"\nMost Popular Day: {popular_day}")

    #Extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    #Uses mode method to find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print(f"\nMost Popular Start Hour: {popular_hour}")

    #Prints the time taken to perform the calculation
    #You will find this in all the functions involving any calculation
    #throughout this program
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

#Function to calculate station related statistics
def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Uses mode method to find the most common start station
    common_start_station = df['Start Station'].mode()[0]

    print(f"The most commonly used start station: {common_start_station}")

    #Uses mode method to find the most common end station
    common_end_station = df['End Station'].mode()[0]

    print(f"\nThe most commonly used end station: {common_end_station}")

    
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    combo = df['Start To End'].mode()[0]

    print(f"\nThe most frequent combination of trips are from {combo}.")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

#Function for trip duration related statistics
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Uses sum method to calculate the total trip duration
    total_duration = df['Trip Duration'].sum()
    #Finds out the duration in minutes and seconds format
    minute, second = divmod(total_duration, 60)
    #Finds out the duration in hour and minutes format
    hour, minute = divmod(minute, 60)
    print(f"The total trip duration is {hour} hours, {minute} minutes and {second} seconds.")

    #Calculating the average trip duration using mean method
    average_duration = round(df['Trip Duration'].mean())
    #Finds the average duration in minutes and seconds format
    mins, sec = divmod(average_duration, 60)
    #This filter prints the time in hours, mins, sec format if the mins exceed 60
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(f"\nThe average trip duration is {hrs} hours, {mins} minutes and {sec} seconds.")
    else:
        print(f"\nThe average trip duration is {mins} minutes and {sec} seconds.")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

#Function to calculate user statistics
def user_stats(df):
    """Displays statistics on bikeshare users.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

 
    user_type = df['User Type'].value_counts()

    print(f"The types of users by number are given below:\n\n{user_type}")
    try:
        gender = df['Gender'].value_counts()
        print(f"\nThe types of users by gender are given below:\n\n{gender}")
    except:
        print("\nThere is no 'Gender' column in this file.")

    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest year of birth: {earliest}\n\nThe most recent year of birth: {recent}\n\nThe most common year of birth: {common_year}")
    except:
        print("There are no birth year details in this file.")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)

#Function to display the data frame itself as per user request
def display_data(df):
    """Displays 5 rows of data from the csv file for the selected city.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """
    USER_RESPONSE = ['yes', 'no']
    raw_data = ''
    counter = 0
    while raw_data not in USER_RESPONSE:

        print("\nDo you wish to view the raw data?")
        print("\nAccepted responses:\nYes or yes\nNo or no")
        raw_data = input().lower()
        if raw_data == "yes":
    
            print(df.head())
        elif raw_data not in USER_RESPONSE:
    
            print("\nPlease check your input.")
            print("Input does not seem to match any of the accepted responses.")
            print("\nRestarting...\n")

    while raw_data == 'yes':

        print("Do you wish to view more raw data?")
        counter = counter + 5
        raw_data = input().lower()

        #If user opts for it, this displays next 5 rows of data
        if raw_data == "yes":
    
             print(df[counter:counter+5])
        elif raw_data != "yes":
    
             break

    print('-'*80)

#Main function to call all the previous functions
def main():
    while True:
        city, month, day = get_filter()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()