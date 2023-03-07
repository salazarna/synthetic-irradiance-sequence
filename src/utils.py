import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =============================================================================
# Convierte una serie temporal a resolución horaria.
# =============================================================================
def cdf(data:np.array) -> np.array:
    # Sort data
    x = np.sort(data)

    # CDF values
    y = 1. * np.arange(len(data)) / (len(data) - 1)

    return np.array([x, y])

# =============================================================================
# Convierte una serie temporal a resolución horaria.
# =============================================================================
def analysis(df:pd.DataFrame, year:int, month:int, irradiance_column:str, plot:bool) -> dict:
    '''
    irrad_analysis function performs a statistical analysis in order
    to extract max. and min. values for each data point. Also, the
    function calculates the **median** clearness index per day and
    categorizes each day to one (of five) sky condition.

    Clearness index (k) analysis: mean daily values which are categorized
    as follows:
    - Sky Condition 1 (SC1): Totally covered, when k <= 0.2
    - Sky Condition 2 (SC2): Mostly covered, when 0.2 < k <= 0.4
    - Sky Condition 3 (SC3): Partly covered, when 0.4 < k <= 0.6
    - Sky Condition 4 (SC4): Mostly clear, when 0.6 < k <= 0.67
    - Sky Condition 5 (SC5): Totally clear, when k > 0.67
    '''
    # Array list to store daily irradiance values from irrad_range
    aux_irradiance = {'stochastic': {}, 'bootstrap': {}}

    # Constants
    TIMES = [f'{i}:0{j}' if j < 10 else f'{i}:{j}' for i in range(0, 24) for j in range(0, 60, 5)]

    MONTHS = {'1': 'Jan', '2': 'Feb', '3': 'Mar', '4': 'Apr', '5': 'May', '6': 'Jun',
              '7': 'Jul', '8': 'Aug', '9': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}

    # DataFrame filtered by date and between 6:00 to 18:00h range
    data = df.loc[(df.index.year == year) & (df.index.month == month)]

    # Median value of clear-sky index (kc)
    median_kc = data['kc'].loc[(data.index.hour >= 6) & (data.index.hour < 18)].resample(rule='1d').median()

    # Categorization according to clear-sky index (kc) value
    totally_covered = np.array(median_kc.loc[median_kc <= 0.2].index.day)
    mostly_covered = np.array(median_kc.loc[(0.2 < median_kc) & (median_kc <= 0.4)].index.day)
    partly_covered = np.array(median_kc.loc[(0.4 < median_kc) & (median_kc <= 0.6)].index.day)
    mostly_clear = np.array(median_kc.loc[(0.6 < median_kc) & (median_kc <= 0.67)].index.day)
    totally_clear = np.array(median_kc.loc[median_kc > 0.67].index.day)

    for i, j in enumerate([totally_covered, mostly_covered, partly_covered, mostly_clear, totally_clear]):
        aux_data = data.loc[data.index.day.isin(j)]

        # Stochastic method data
        aux_irradiance['stochastic'][f'sc{i+1}'] = aux_data.groupby([aux_data.index.hour, aux_data.index.minute])[irradiance_column].describe()

        # Bootstrap method data
        aux_irradiance['bootstrap'][f'sc{i+1}'] = pd.DataFrame(aux_data[irradiance_column].values.reshape(len(aux_data.index.day.unique()), len(TIMES)), index=list(aux_data.index.day.unique()), columns=TIMES)

    # Statistical analysis plot
    if plot == True:
        XTICKS = np.arange(start=0, stop=300, step=50)
        LABELS = [TIMES[i] for i in XTICKS]

        for i, j in enumerate([totally_covered, mostly_covered, partly_covered, mostly_clear, totally_clear]):
            aux_data = data[irradiance_column].loc[data.index.day.isin(j)]

            hor = 8
            ver = 5
            plt.figure(figsize=(hor,ver))

            if aux_data.empty == False:
                temp_aux_data = pd.DataFrame(aux_data.values.reshape(len(aux_data.index.day.unique()), len(TIMES)), columns=TIMES)

                plt.plot(temp_aux_data.T.values, color='black', alpha=0.1, linestyle='', marker='.', markersize=2, fillstyle='none')

                plt.plot(aux_irradiance['stochastic'][f'sc{i+1}']['max'].values, color='#1580E4', marker='.', markersize=4, linestyle='', label='Max')
                plt.plot(aux_irradiance['stochastic'][f'sc{i+1}']['mean'].values, color='#2DBD07', marker='.', markersize=4, linestyle='', label='Mean')
                plt.plot(aux_irradiance['stochastic'][f'sc{i+1}']['min'].values, color='coral', marker='.', markersize=4, linestyle='', label='Min')

                plt.fill_between(x=np.arange(len(aux_irradiance['stochastic'][f'sc{i+1}'])), y1=aux_irradiance['stochastic'][f'sc{i+1}']['max'], y2=aux_irradiance['stochastic'][f'sc{i+1}']['min'], color='whitesmoke', alpha=0.35, label='Stochastic Range')

                plt.title(f'Irradiance Behaviour for {MONTHS[str(month)]}-{year} (SC{i+1})')
                plt.ylabel('Irradiance, $W/m^2$')
                plt.xlabel('Time')

                plt.tick_params(which='major', direction='in', length=5, width=0.75, grid_alpha=0.3)
                plt.tick_params(which='minor', direction='in', length=2.5, width=0.5, grid_alpha=0.3)
                plt.xticks(rotation=0, ticks=XTICKS, labels=LABELS)
                plt.minorticks_on()
                plt.ylim(0, None)
                plt.xlim(0, len(aux_irradiance['stochastic'][f'sc{i+1}']))
                plt.grid(True)
                plt.grid(visible=True, which='major', color='grey', linestyle='-', linewidth=0.5)
                plt.grid(visible=True, which='minor', color='lightgrey', linestyle='-', linewidth=0.3, alpha=0.2)
                plt.tight_layout
                plt.legend(loc='best', fontsize=9) # bbox_to_anchor=(1,1)

    return aux_irradiance