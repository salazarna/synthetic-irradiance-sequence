import numpy as np
import pandas as pd
import pvlib
import scipy


# =============================================================================
# Stochastic
# =============================================================================
def stochastic(dictionary:dict, year:int, month:int, sky_condition:str, runs:int) -> dict:
    '''
    '''
    # Catching exception
    if sky_condition not in ['sc1', 'sc2', 'sc3', 'sc4', 'sc5']:
        raise ValueError(f"An invalid sky condition ({sky_condition}) was selected. Select one of ['sc1', 'sc2', 'sc3', 'sc4', 'sc5'].")

    # Dictionary
    synthetic_irradiance = {}

    # Constants
    MONTHS = {'1': 'Jan', '2': 'Feb', '3': 'Mar', '4': 'Apr', '5': 'May', '6': 'Jun',
              '7': 'Jul', '8': 'Aug', '9': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}

    #Calling the data from irrad_analysis dictionary previously created
    data = dictionary[sky_condition]

    if data.empty == True:
        print('There is no information related to the date {MONTHS[str(month)]}-{year} {sky_condition}.')

    else:
        # DataFrame to store all the synthetic irradiance before store at dictionary
        df = pd.DataFrame()

        for i in range(runs):
            # Generation of synthetic irradiance by a gaussian (normal) distribution
            synt = np.random.normal(loc=data['mean'], scale=data['std'])
            '''
            if synt < data['min'].values:
                synt = data['min'].values

            if synt > data['max'].values:
                synt = data['max'].values
            '''
            synt[synt < data['min']] = data['min'][synt < data['min']].values
            synt[synt > data['max']] = data['max'][synt > data['max']].values

            # Synthetic data storage in dataframe
            df[f'synt{i+1}'] = synt

            if i == runs-1:
                # Change numerical index to datetime index
                df.set_index(data.index, inplace=True)
                df.index.set_names(['hour', 'minute'], inplace=True)

                # Save the synthetic data in irradsyntm1_dict
                synthetic_irradiance[f'{MONTHS[str(month)]}{year}-{sky_condition}'] = df

    return synthetic_irradiance

# =============================================================================
# Bootstrap
# =============================================================================
def bootstrap(dictionary:dict, year:int, month:int, sky_condition:str, resolution:int, runs:int) -> dict:
    '''
    '''
    # Catching exception
    if sky_condition not in ['sc1', 'sc2', 'sc3', 'sc4', 'sc5']:
        raise ValueError(f"An invalid sky condition ({sky_condition}) was selected. Select one of ['sc1', 'sc2', 'sc3', 'sc4', 'sc5'].")

    # Dictionary
    synthetic_irradiance = {}

    # Constants
    MONTHS = {'1': 'Jan', '2': 'Feb', '3': 'Mar', '4': 'Apr', '5': 'May', '6': 'Jun',
              '7': 'Jul', '8': 'Aug', '9': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}

    MULTIINDEX = [(i,j) for i in range(0, 24) for j in range(0, 60, resolution)]

    #Calling the data from irrad_analysis dictionary previously created
    data = dictionary[sky_condition]

    if data.empty == True:
        print(f'There is no information related to the date {MONTHS[str(month)]}-{year} {sky_condition}.')

    else:
        # DataFrame to store all the synthetic irradiance before store at dictionary
        df = pd.DataFrame()

        aux_data = data.to_numpy()

        synt = aux_data[np.random.choice(aux_data.shape[0], runs, replace=True)]

        for i in range(runs):
            # Synthetic data storage in dataframe
            df[f'synt{i+1}'] = synt[i]

            if i == runs-1:
                # Change numerical index to datetime index
                df.index = pd.MultiIndex.from_tuples(MULTIINDEX, names=('hour', 'minute'))

                # Save the synthetic data in irradsyntm1_dict
                synthetic_irradiance[f'{MONTHS[str(month)]}{year}-{sky_condition}'] = df

    return synthetic_irradiance

# =============================================================================
# Clear sky index (kc)
# =============================================================================
def clear_sky_index(data:pd.DataFrame(), column:str, longitude:float, latitude:float, altitude:float, time_zone:str) -> pd.DataFrame():
    '''
    '''
    # Location
    location = pvlib.location.Location(latitude, longitude, time_zone, altitude)

    # Clear-sky irradiance (Hcs)
    RESOLUTION = int(pd.Series(data.index.values).diff().median().total_seconds()/60)

    # Clear-sky irradiance (Hcs)
    hcs = location.get_clearsky(times=pd.date_range(start=data.index[0],end=data.index[-1], freq=f'{RESOLUTION}min', tz=time_zone),
                                model='ineichen')

    # Append clear-sky irradiance to main dataframe
    data['ics_wm2'] = hcs['ghi'].values

    # Clear-sky index (kc) to main dataframe
    data['kc'] = data[column].values / data['ics_wm2'].values

    # NaN
    data['kc'] = data['kc'].fillna(1)

    # Replace kc > 1
    data.loc[data['kc'] > 1, 'kc'] = 1

    return data

# =============================================================================
# Sequential
# =============================================================================
def sequential(data:pd.DataFrame, irradiance_column:str, year:int, month:int, sky_condition:str,
               method:str, confidence_interval:float, runs:int) -> pd.DataFrame():
    '''
    '''
    # Catching exception
    if sky_condition not in ['sc1', 'sc2', 'sc3', 'sc4', 'sc5']:
        raise ValueError(f"An invalid sky condition ({sky_condition}) was selected. Select one of ['sc1', 'sc2', 'sc3', 'sc4', 'sc5'].")

    if method not in ['stochastic', 'bootstrap']:
        raise ValueError(f"An invalid method ({method}) for synthetic solar irradiance generation was selected. Select one of ['stochastic', 'bootstrap'].")

    # Constants
    RESOLUTION = int(pd.Series(data.index.values).diff().median().total_seconds()/60)
    TIMES = [f'{i}:0{j}' if j < 10 else f'{i}:{j}' for i in range(0, 24) for j in range(0, 60, RESOLUTION)]
    MULTIINDEX = [(i,j) for i in range(0, 24) for j in range(0, 60, RESOLUTION)]

    # DataFrame filtered by date and between 6:00 to 18:00h range
    data = data.loc[(data.index.year == year) & (data.index.month == month)]

    # Median value of clear-sky index (kc)
    median_kc = data['kc'].loc[(data.index.hour >= 6) & (data.index.hour < 18)].resample(rule='1d').median()

    # Categorization according to clear-sky index (kc) value
    if sky_condition == 'sc1':
        days = np.array(median_kc.loc[median_kc <= 0.2].index.day)

    elif sky_condition == 'sc2':
        days = np.array(median_kc.loc[(0.2 < median_kc) & (median_kc <= 0.4)].index.day)

    elif sky_condition == 'sc3':
        days = np.array(median_kc.loc[(0.4 < median_kc) & (median_kc <= 0.6)].index.day)

    elif sky_condition == 'sc4':
        days = np.array(median_kc.loc[(0.6 < median_kc) & (median_kc <= 0.67)].index.day)

    elif sky_condition == 'sc5':
        days = np.array(median_kc.loc[median_kc > 0.67].index.day)

    else:
        raise ValueError(f'An invalid sky condition {sky_condition} was requested.')

    if len(days) == 0:
        df = None

    else:
        aux_data = data[irradiance_column].loc[data.index.day.isin(days)]

        temp_aux_data = pd.DataFrame(aux_data.values.reshape(len(aux_data.index.day.unique()), len(TIMES)), index=list(aux_data.index.day.unique()), columns=TIMES)

        if temp_aux_data.empty != True:
            ALPHA = 1 - confidence_interval

            # DataFrame to store all the synthetic irradiance before store at dictionary
            df = pd.DataFrame()

            for r in range(runs):
                synt = []

                for i, j in enumerate(TIMES):
                    if i == 0:
                        # STEP 1. Select column from pd.DataFrame
                        temp = temp_aux_data[j]

                        # STEP 2. Generate a stochastic synthetic data
                        if method == 'stochastic':
                            synt.append(np.random.normal(loc=np.mean(temp), scale=np.std(temp)))

                        else:
                            synt.append(np.random.choice(temp.values))

                    else:
                        # STEP 1. Select column from pd.DataFrame
                        temp = temp_aux_data[[TIMES[i-1], TIMES[i]]]

                        # STEP 2. Confidence interval
                        N = len(temp)

                        z = scipy.stats.norm.ppf(confidence_interval+(ALPHA/2)) # Gaussian
                        std = np.std(temp[TIMES[i-1]], ddof=0) # Population

                        upper_bound = synt[i-1] + (z * std / np.sqrt(N))
                        lower_bound = synt[i-1] - (z * std / np.sqrt(N))

                        # STEP 3. Interval bounds
                        if upper_bound >= np.max(temp[TIMES[i-1]].values):
                            upper_bound = np.max(temp[TIMES[i-1]].values)

                        if lower_bound <= np.min(temp[TIMES[i-1]].values):
                            lower_bound = np.min(temp[TIMES[i-1]].values)

                        # STEP 3. Filter pd.DataFrame by confidence interval
                        temp = temp.loc[(lower_bound <= temp[TIMES[i-1]]) & (temp[TIMES[i-1]] <= upper_bound)]

                        # STEP 4. Generate a stochastic synthetic data
                        if len(temp[TIMES[i]]) == 0:
                            synt.append(synt[i-1])

                        else:
                            # Stochastic
                            if method == 'stochastic':
                                s = np.random.normal(loc=np.mean(temp[TIMES[i]]), scale=np.std(temp[TIMES[i]]))

                                if s >= np.max(temp[TIMES[i]].values):
                                    s = np.max(temp[TIMES[i]].values)

                                if s <= np.min(temp[TIMES[i]].values):
                                    s = np.min(temp[TIMES[i]].values)

                                synt.append(s)

                            # Bootstrap
                            else:
                                synt.append(np.random.choice(temp[TIMES[i]].values))

                # Synthetic data storage in dataframe
                df[f'synt{r+1}'] = synt

                if r == runs-1:
                    # Change numerical index to datetime index
                    df.index = pd.MultiIndex.from_tuples(MULTIINDEX, names=('hour', 'minute'))

    return df