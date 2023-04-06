import pandas as pd

def read_data():
    """ Reads csv files into dataframes, changes column names for consistency in data,
        and makes a nested dictionary with smaller dict containing variable as key and
        df as value; Larger dict containing key as time period and small dict as value.


    :return: Nested dictionary
    """
    daily_activity = pd.read_csv("/Users/jaigollapudi/Downloads/Fitabase Data 4.12.16-5.12.16/dailyActivity_merged.csv")
    daily_sleep = pd.read_csv("/Users/jaigollapudi/Downloads/Fitabase Data 4.12.16-5.12.16/sleepDay_merged.csv")
    daily_weight = pd.read_csv("/Users/jaigollapudi/Downloads/Fitabase Data 4.12.16-5.12.16/weightLogInfo_merged.csv")
    hourly_calories = pd.read_csv("/Users/jaigollapudi/Downloads/Fitabase Data 4.12.16-5.12.16/hourlyCalories_merged.csv")
    hourly_intensities = pd.read_csv("/Users/jaigollapudi/Downloads/Fitabase Data 4.12.16-5.12.16/hourlyIntensities_merged.csv")
    hourly_steps = pd.read_csv("/Users/jaigollapudi/Downloads/Fitabase Data 4.12.16-5.12.16/hourlySteps_merged.csv")
    minute_calories_narrow = pd.read_csv("/Users/jaigollapudi/Downloads/Fitabase Data 4.12.16-5.12.16/minuteCaloriesNarrow_merged.csv")
    minute_intensities_narrow = pd.read_csv("/Users/jaigollapudi/Downloads/Fitabase Data 4.12.16-5.12.16/minuteIntensitiesNarrow_merged.csv")
    minute_steps_narrow = pd.read_csv("/Users/jaigollapudi/Downloads/Fitabase Data 4.12.16-5.12.16/minuteStepsNarrow_merged.csv")
    minute_sleep = pd.read_csv("/Users/jaigollapudi/Downloads/Fitabase Data 4.12.16-5.12.16/minuteSleep_merged.csv")
    second_heartrate = pd.read_csv("/Users/jaigollapudi/Downloads/Fitabase Data 4.12.16-5.12.16/heartrate_seconds_merged.csv")

    # Renaming column names for consistency over dataframes
    daily_activity = daily_activity.rename(columns={'ActivityDate': 'ActivityDay'})
    daily_sleep = daily_sleep.rename(columns={'SleepDay': 'ActivityDay'})
    daily_weight = daily_weight.rename(columns={'Date': 'ActivityDay'})
    minute_sleep = minute_sleep.rename(columns={'date': 'ActivityMinute'})
    second_heartrate = second_heartrate.rename(columns={'Time': 'ActivitySecond'})

    daily_sleep['ActivityDay'] = pd.to_datetime(daily_sleep['ActivityDay'])

    # Defining the variables and the dataframe it needs to be pulled from
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
            "value": minute_sleep
        },
        "S": {
            "Value": second_heartrate
        }
    }

    return data


# Defining valid variables that user can choose from
valid_variables = {
    'D': ['TotalSteps', 'TotalDistance', 'TrackerDistance', 'LoggedActivitiesDistance',
          'VeryActiveDistance', 'ModeratelyActiveDistance', 'LightActiveDistance',
          'SedentaryActiveDistance', 'VeryActiveMinutes', 'FairlyActiveMinutes',
          'LightlyActiveMinutes', 'SedentaryMinutes', 'Calories', 'TotalMinutesAsleep',
          'TotalSleepRecords','TotalTimeInBed','WeightKg', 'WeightPounds', 'BMI',
          ],
    'H': ['Calories', 'TotalIntensity', 'StepTotal'],
    'M': ['Calories', 'Intensity', 'Steps','value'],
    'S': ['Value']
}
