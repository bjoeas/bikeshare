import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

AVAILABLE_MONTH = ('january', 'february', 'march', 'april', 'may', 'june')

DAYS = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')


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
    while True:
        city_str = ', '.join(CITY_DATA).title()
        city = input('Which city should be analyzed ({})? '.format(city_str)).lower()
        if city not in CITY_DATA:
            print('This is not a valid city! Please take a specified city.')
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month_str = ', '.join(AVAILABLE_MONTH).title()
        month = input('Should filtering be done according to a certain month ({} or all)?) '.format(month_str)).lower()
        if month not in AVAILABLE_MONTH + ('all',):
            print('This is not a valid month! Please take a specified month or all.')
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_str = ', '.join(DAYS).title()
        day = input('Should filtering be done according to a certain day ({} or all)?) '.format(day_str)).lower()
        if day not in DAYS + ('all',):
            print('This is not a valid day! Please take a specified day or all.')
            continue
        else:
            break

    print('-' * 40)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # remove unused columns
    df.drop('Unnamed: 0', axis=1, inplace=True)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()  # new syntax
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].value_counts()
    print('Most common month: {} with {} times in the data selection'.format(common_month.idxmax(), common_month[0]))

    # display the most common day of week
    common_day = df['day_of_week'].value_counts()
    print('Most common day: {} with {} times in the data selection'.format(common_day.idxmax(), common_day[0]))

    # display the most common start hour
    common_hour = df['hour'].value_counts()
    print('Most common hour: {} with {} times in the data selection'.format(common_hour.idxmax(),
                                                                            common_hour[common_hour.idxmax()]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station:', start_station)

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('Most commonly used end station:', end_station)

    # display most frequent combination of start station and end station trip
    combination_of_stations = df.groupby(['Start Station', 'End Station'])['Start Station'].count().idxmax()
    print('Most commonly used combination of start station and end station trip:', combination_of_stations[0],
          '=>', combination_of_stations[1])

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = np.sum(df['Trip Duration'])
    print('Total travel time:', display_time(int(total_travel_time), 5))

    # display mean travel time
    mean_travel_time = np.mean(df['Trip Duration'])
    print('Mean travel time:', display_time(int(mean_travel_time), 5))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:\n{}'.format(user_types))

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print('\nGender Types:\n{}'.format(gender))
    except KeyError:
        print('\nNo gender-specific data are available for {}.'.format(city.title()))

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = df['Birth Year'].min()
        print('\nEarliest year of birth:', int(earliest_year))
        most_recent_year = df['Birth Year'].max()
        print('Most recent year of birth:', int(most_recent_year))
        most_common_year = df['Birth Year'].value_counts().idxmax()
        print('Most common year of birth:', int(most_common_year))
    except KeyError:
        print('\nNo birth year data is available for {}.'.format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def diplay_raw_data(df):
    """Display raw data upon users request"""

    df_length = len(df.index)
    count_row = 0
    while True:
        print(df.iloc[(0 + count_row):(5 + count_row)])
        count_row += 5

        if count_row > df_length:
            print('\nAll selected raw data were displayed.\n')
            break

        next_lines = input('\nWould you like to see the next 5 lines of raw data? Enter yes or no. ')
        if next_lines.lower() != 'yes':
            break

    print('-' * 40)


def display_time(seconds, granularity=2):
    """Converts seconds to weeks, days, hours, minutes and the remaining seconds and returns a dynamic string"""
    # https://stackoverflow.com/questions/4048651/python-function-to-convert-seconds-into-minutes-hours-and-days

    intervals = (
        ('weeks', 604800),  # 60 * 60 * 24 * 7
        ('days', 86400),  # 60 * 60 * 24
        ('hours', 3600),  # 60 * 60
        ('minutes', 60),
        ('seconds', 1),
    )
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        raw_data = input('\nWould you like to see the first 5 lines of raw data? Enter yes or no. ')
        if raw_data.lower() == 'yes':
            diplay_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no. ')
        if restart.lower() != 'yes':
            break


if __name__ == '__main__':
    main()
