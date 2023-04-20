"""
Anoushka Bhatia, Xi Chen, Jai Gollapudi, Jingyi Gong, Krishi Patel, Shreya Thalvayapati
DS3500 Final Project: Fitbit Insights Dashboard
4/19/2023
data.py: reading in data from files
Github repo: https://github.com/jingyig16/healthdashboard
"""

# Importing libraries
import pandas as pd
import os


def read_data():
    """ Reads csv files into dataframes, changes column names for consistency in data,
        and makes a nested dictionary with smaller dict containing variable as key and
        df as value; Larger dict containing key as time period and small dict as value.

    :return: Nested dictionary
    """

    # Getting absolute path of the directory that contains the data.py file,
    # and then use joining that path with the relative path of each data file.
    base_path = os.path.abspath(os.path.dirname(__file__))

    daily_activity_file = os.path.join(base_path, "data/dailyActivity_merged.csv")
    daily_sleep_file = os.path.join(base_path, "data/sleepDay_merged.csv")
    daily_weight_file = os.path.join(base_path, "data/weightLogInfo_merged.csv")
    hourly_calories_file = os.path.join(base_path, "data/hourlyCalories_merged.csv")
    hourly_intensities_file = os.path.join(base_path, "data/hourlyIntensities_merged.csv")
    hourly_steps_file = os.path.join(base_path, "data/hourlySteps_merged.csv")
    minute_calories_narrow_file = os.path.join(base_path, "data/minuteCaloriesNarrow_merged.csv")
    minute_intensities_narrow_file = os.path.join(base_path, "data/minuteIntensitiesNarrow_merged.csv")
    minute_steps_narrow_file = os.path.join(base_path, "data/minuteStepsNarrow_merged.csv")
    minute_sleep_file = os.path.join(base_path, "data/minuteSleep_merged.csv")
    second_heartrate_file = os.path.join(base_path, "data/heartrate_seconds_merged.csv")

    # Reading files into dataframes
    daily_activity = pd.read_csv(daily_activity_file)
    daily_sleep = pd.read_csv(daily_sleep_file)
    daily_weight = pd.read_csv(daily_weight_file)
    hourly_calories = pd.read_csv(hourly_calories_file)
    hourly_intensities = pd.read_csv(hourly_intensities_file)
    hourly_steps = pd.read_csv(hourly_steps_file)
    minute_calories_narrow = pd.read_csv(minute_calories_narrow_file)
    minute_intensities_narrow = pd.read_csv(minute_intensities_narrow_file)
    minute_steps_narrow = pd.read_csv(minute_steps_narrow_file)
    minute_sleep = pd.read_csv(minute_sleep_file)
    second_heartrate = pd.read_csv(second_heartrate_file)

    # Data cleaning
    # Renaming column names for consistency over dataframes
    daily_activity = daily_activity.rename(columns={'ActivityDate': 'ActivityDay'})
    daily_sleep = daily_sleep.rename(columns={'SleepDay': 'ActivityDay'})
    daily_weight = daily_weight.rename(columns={'Date': 'ActivityDay'})
    minute_sleep = minute_sleep.rename(columns={'date': 'ActivityMinute',
                                                'value': 'TotalSleepRecords'})
    second_heartrate = second_heartrate.rename(columns={'Time': 'ActivitySecond',
                                                        'Value': 'Heartbeat'})

    # Converting column to datetime format
    daily_sleep['ActivityDay'] = pd.to_datetime(daily_sleep['ActivityDay'])

    # Defining the variables and the dataframe it needs to be extracted from
    data = {
        "D": {
            "TotalSteps": daily_activity,
            "TotalDistance": daily_activity,
            "TrackerDistance": daily_activity,
            "LoggedActivitiesDistance": daily_activity,
            "VeryActiveDistance": daily_activity,
            "ModeratelyActiveDistance": daily_activity,
            "LightActiveDistance": daily_activity,
            "SedentaryActiveDistance": daily_activity,
            "VeryActiveMinutes": daily_activity,
            "FairlyActiveMinutes": daily_activity,
            "LightlyActiveMinutes": daily_activity,
            "SedentaryMinutes": daily_activity,
            "Calories": daily_activity,
            "TotalMinutesAsleep": daily_sleep,
            "TotalSleepRecords": daily_sleep,
            "TotalTimeInBed": daily_sleep,
            "WeightKg": daily_weight,
            "WeightPounds": daily_weight,
            "BMI": daily_weight
        },
        "H": {
            "Calories": hourly_calories,
            "TotalIntensity": hourly_intensities,
            "StepTotal": hourly_steps
        },
        "M": {
            "Steps": minute_steps_narrow,
            "Calories": minute_calories_narrow,
            "Intensity": minute_intensities_narrow,
            "TotalSleepRecords": minute_sleep
        },
        "S": {
            "Heartbeat": second_heartrate
        }
    }

    return data


# Defining valid variables that user can choose from for time series and correlation
valid_variables = {
    'D': ['TotalSteps', 'TotalDistance', 'TrackerDistance', 'LoggedActivitiesDistance',
          'VeryActiveDistance', 'ModeratelyActiveDistance', 'LightActiveDistance',
          'SedentaryActiveDistance', 'VeryActiveMinutes', 'FairlyActiveMinutes',
          'LightlyActiveMinutes', 'SedentaryMinutes', 'Calories', 'TotalMinutesAsleep',
          'TotalSleepRecords', 'TotalTimeInBed', 'WeightKg', 'WeightPounds', 'BMI',
          ],
    'H': ['Calories', 'TotalIntensity', 'StepTotal'],
    'M': ['Calories', 'Intensity', 'Steps', 'TotalSleepRecords'],
    'S': ['Heartbeat']
}

