import warnings
import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Ask user to specify a city, month, and day to analyze.

    Return:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) raw - yes determines top 5 rows are shown
    """
    print("\nHello! Let's explore some US bikeshare data!\n\nWe have information on three cities: Chicago, New York City, and Washington.")
    # Get user input for city (chicago, new york city, washington).
    city = input("Type the name of the city that interests you: ").lower()
    while city not in CITY_DATA.keys():
        city = input("That doesn't look quite right... look above for the choices available, and please try again: ").lower()

    # Get user input for month (all, january, february, ... , june)
    month = input("\nType 'All', or the month for which you'd like to see information: ").lower()
    while month not in months and month !='all':
        month = input("That doesn't look quite right... try typing the full name of the month, or 'All': ").lower()

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("\nType 'All', or a specific day of the week for which you'd like to see information: ").lower()
    while day not in days and day !='all':
        day = input("That doesn't look quite right... try typing the full name of the day (e.g.: 'Wednesday'), or 'All': ").lower()

    # Ask user whether they wish to see top 5 rows
    raw = input("\nWould you like to see the top five rows of raw data?\nType 'yes' to display: ").lower()

    print('-'*40)
    return city, month, day, raw


def load_data(city, month, day, raw):
    """
    Load data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) raw - yes or other
    Return:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA.get(city))

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # Add and modify columns used in various stats function
    df['hour'] = df['Start Time'].dt.hour
    df['trip'] = 'is from ' + df['Start Station'].astype(str) + ', ends at ' + df['End Station'].astype(str)

    # Filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
        # Check that month requested is in range of dataframe
        if month > df['month'].max():
            print('Unfortunately, we only have information up to the month of {}. Changing selection to all months.'\
                    .format(months[df['month'].max() - 1].title()))
        # filter by month to create the new dataframe
        else:
            df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        # use the index of the days list to get the corresponding int
        day = days.index(day)
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]


    return df


def show_rows(df, raw):
    """Displays five rows of the dataframe, based on user input"""

    row = 0
    column_set1 = ['Start Time', 'month', 'day_of_week', 'Trip Duration',
        'Start Station', 'End Station', 'User Type', 'Gender', 'Birth Year']
    column_set2 = ['Start Time', 'month', 'day_of_week','Trip Duration',
        'Start Station', 'End Station', 'User Type']

    # Catch 'future warning' as an error, so only correct columns are displayed.
    warnings.filterwarnings("error")

    while raw == 'yes':
        try:
            print(df.loc[row:row + 4, column_set1])
        except:
            print(df.loc[row:row + 4, column_set2])
        row += 5
        raw = input("\nWould you like to see more? Enter 'yes' to see 5 more rows: ").lower()
    print('-'*40)

    return


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    month_mode = months[df['month'].mode().values[0] - 1]
    print("The most common month in your selection is {}.".format(month_mode.title()))

    # Display the most common day of week
    day_mode = days[df['day_of_week'].mode().values[0]]
    print("The most common day of the week in your selection is {}.".format(day_mode.title()))

    # Display the most common start hour
    hour_mode = df['hour'].mode().values[0]
    print("The most common starting hour in your selection is {} (24 hour clock).".format(hour_mode))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Display statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    start_station_mode = df['Start Station'].mode().values[0]
    print("Most popular station to start at: {}.".format(start_station_mode))

    # Display most commonly used end station
    end_station_mode = df['End Station'].mode().values[0]
    print("Most popular station to end at: {}.".format(end_station_mode))

    # Display most frequent combination of start station and end station trip
    trip_mode = df['trip'].mode().values[0]
    print("Most popular trip {}.".format(trip_mode))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time in minutes in hours
    total_travel = df['Trip Duration'].sum() / 60 / 60
    print('Total travel time was approximately {} hours.'.format(int(round(total_travel))))

    # Display mean travel time in minutes
    mean_travel = df['Trip Duration'].mean() / 60
    print('Average travel time was approximately {} minutes.'.format(round(mean_travel)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Display statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    types = df['User Type'].value_counts()
    print("The chart below shows the number of each user type.\n{}".format(types))

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print("\nThe chart below shows the number of users by gender.\n{}".format(gender))
    except:
        print("\nThere is no gender information in your selection.\n")

    # Display earliest, most recent, and most common year of birth
    try:
        print('\nThe oldest user was born in {}, the youngest user was born in {}, and the most common year of birth was {}.'\
            .format(int(df['Birth Year'].min()), \
                    int(df['Birth Year'].max()), \
                    int(df['Birth Year'].mode().values[0])))
    except:
        print('No information on year of birth is available in your selection.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day, raw = get_filters()
        df = load_data(city, month, day, raw)

        if raw == 'yes':
            show_rows(df, raw)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
