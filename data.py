import pandas as pd


def read_data():
    """ Reads csv files into dataframes, changes column names for consistency in data,
        and makes a nested dictionary with smaller dict containing variable as key and
        df as value; Larger dict containing key as time period and small dict as value.


    :return: Nested dictionary
    """
    daily_activity = pd.read_csv("data/dailyActivity_merged.csv")
    daily_sleep = pd.read_csv("data/sleepDay_merged.csv")
    daily_weight = pd.read_csv("data/weightLogInfo_merged.csv")
    hourly_calories = pd.read_csv("data/hourlyCalories_merged.csv")
    hourly_intensities = pd.read_csv("data/hourlyIntensities_merged.csv")
    hourly_steps = pd.read_csv("data/hourlySteps_merged.csv")
    minute_calories_narrow = pd.read_csv("data/minuteCaloriesNarrow_merged.csv")
    minute_intensities_narrow = pd.read_csv("data/minuteIntensitiesNarrow_merged.csv")
    minute_steps_narrow = pd.read_csv("data/minuteStepsNarrow_merged.csv")
    minute_sleep = pd.read_csv("data/minuteSleep_merged.csv")
    second_heartrate = pd.read_csv("data/heartrate_seconds_merged.csv")

    # Data cleaning
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
          'TotalSleepRecords', 'TotalTimeInBed', 'WeightKg', 'WeightPounds', 'BMI',
          ],
    'H': ['Calories', 'TotalIntensity', 'StepTotal'],
    'M': ['Calories', 'Intensity', 'Steps', 'value'],
    'S': ['Value']
}

valid_users = {'fitbit': 'test',
               1503960366: 'NEU_1',
               1624580081: 'NEU_2',
               1644430081: 'NEU_3',
               1844505072: 'NEU_4',
               1927972279: 'NEU_5',
               2022484408: 'NEU_6',
               2026352035: 'NEU_7',
               2320127002: 'NEU_8',
               2347167796: 'NEU_9',
               2873212765: 'NEU_10',
               3372868164: 'NEU_11',
               3977333714: 'NEU_12',
               4020332650: 'NEU_13',
               4057192912: 'NEU_14',
               4319703577: 'NEU_15',
               4388161847: 'NEU_16',
               4445114986: 'NEU_17',
               4558609924: 'NEU_18',
               4702921684: 'NEU_19',
               5553957443: 'NEU_20',
               5577150313: 'NEU_21',
               6117666160: 'NEU_22',
               6290855005: 'NEU_23',
               6775888955: 'NEU_24',
               6962181067: 'NEU_25',
               7007744171: 'NEU_26',
               7086361926: 'NEU_27',
               8053475328: 'NEU_28',
               8253242879: 'NEU_29',
               8378563200: 'NEU_30',
               8583815059: 'NEU_31',
               8792009665: 'NEU_32',
               8877689391: 'NEU_33'}
