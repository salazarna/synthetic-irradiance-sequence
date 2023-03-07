import src
import pvlib
import scipy
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

# =============================================================================
# Standard deviation of increments (SDI)
# =============================================================================
def standard_deviation_increments(data:np.array) -> float:
    '''
    pp. 167
    '''
    delta = np.array([0 if i == 0 else abs(data[i] - data[i-1]) for i in range(len(data))])
    return  np.sqrt(np.sum((delta - np.mean(delta))**2) / (len(delta) - 1))

# =============================================================================
# Stability index (SI)
# =============================================================================
def stability_index(data:np.array, threshold:float=500) -> float:
    '''
    pp. 168
    '''
    delta = np.array([0 if i == 0 else abs(data[i] - data[i-1]) for i in range(len(data))])

    delta[delta > threshold] = 1
    delta[delta <= threshold] = 0

    return np.sum(delta)

# =============================================================================
# Integrated complementary cumulative distribution function (ICCDF)
# =============================================================================
def iccdf(data:np.array) -> float:
    '''
    pp. 170
    '''
    x, y = src.utils.cdf(data=data)

    return scipy.integrate.simpson(x=x, y=1-y)

# =============================================================================
# Variability index (VI)
# =============================================================================
def variability_index(timestamps:np.array, ghi:np.array, hcs:np.array) -> pd.Series:
    dt = int(pd.Series(timestamps).diff().median().total_seconds()/60)

    delta_ghi = np.array([0 if i == 0 else np.sqrt(((ghi[i] - ghi[i-1])**2) + dt**2) for i in range(len(ghi))])
    delta_hcs = np.array([0 if i == 0 else np.sqrt(((hcs[i] - hcs[i-1])**2) + dt**2) for i in range(len(hcs))])

    vi = delta_ghi / delta_hcs
    vi[np.isnan(vi)] = 1

    return pd.Series(vi, index=timestamps)

# =============================================================================
# Kolmogorov-Smirnov Test (KS)
# =============================================================================
def kolmogorov_smirnov(sample1:np.array, sample2:np.array) -> dict():
    '''
    The null hypothesis is that the two distributions are identical, i.e.,
    F(x) = G(x) for all x. The alternative is that they are not identical.

    If the KS statistic is large, then the p-value will be small,
    and this may be taken as evidence against the null hypothesis
    in favor of the alternative.

    If the p-value is lower than our threshold of 0.05, so we reject the
    null hypothesis in favor of the default “two-sided” alternative: the
    data were not drawn from the same distribution.
    '''
    ks = scipy.stats.ks_2samp(data1=sample1, data2=sample2)
    '''
    if ks.pvalue <= 0.05:
        return 1
    else:
        return 0
    '''
    return ks.pvalue

# =============================================================================
# Kullback-Leibler Divergence (KLD)
# =============================================================================
def kullback_leibler_divergence(sample1:np.array, sample2:np.array) -> float:
    '''
    The KLD helps to estimate the average amount of information between measured
    and true distributions.

    To use the estimated distribution from data rather
    than the true distribution in applications, the value of the KLD has to be
    minimal and therefore the information conveyed by the two distributions is
    not significantly different.

    If the KLD value is 0 then the estimated distribution fits perfectly the
    true underlying distribution of data.
    '''
    kld = scipy.stats.entropy(pk=sample1, qk=sample2)

    if kld == np.inf:
        return 1
    else:
        return kld

# =============================================================================
# Overlapping coefficient (OVC)
# =============================================================================
def overlapping_coefficient(sample1:np.array, sample2:np.array, number_bins:int=100) -> float:
    '''
    https://stats.stackexchange.com/questions/267432/coefficient-of-overlapping-ovl-for-two-distributions

    A value of 1 corresponds to a perfect fit between f(x) and g(x)
    and 0 valuecorresponds to totally disjointed densities.
    '''
    # Determine the range over which the integration will occur
    min_value = np.min((sample1.min(), sample2.min()))
    max_value = np.min((sample1.max(), sample2.max()))

    # Determine the bin width
    bin_width = (max_value-min_value)/number_bins

    #For each bin, find min frequency
    lower_bound = min_value #Lower bound of the first bin is the min_value of both arrays
    min_arr = np.empty(number_bins) #Array that will collect the min frequency in each bin

    for b in range(number_bins):
        higher_bound = lower_bound + bin_width #Set the higher bound for the bin

        #Determine the share of samples in the interval
        freq_sample1 = np.ma.masked_where((sample1<lower_bound)|(sample1>=higher_bound), sample1).count()/len(sample1)
        freq_sample2 = np.ma.masked_where((sample2<lower_bound)|(sample2>=higher_bound), sample2).count()/len(sample2)

        #Conserve the lower frequency
        min_arr[b] = np.min((freq_sample1, freq_sample2))
        lower_bound = higher_bound #To move to the next range

    return min_arr.sum()

# =============================================================================
# Root mean squared error (RMSE)
# =============================================================================
def root_mean_squared_error(target:np.array, predicted:np.array, percentage:bool=False):
    rmse = mean_squared_error(y_true=target, y_pred=predicted, squared=False)

    if percentage == True:
        rmse = (rmse / np.max(target)) * 100

    return rmse

# =============================================================================
# Percentage error
# =============================================================================
def percentage_error(target:np.array, predicted:np.array) -> float:
    return (np.abs(np.array(target) - np.array(predicted)) / np.array(target)) * 100

# =============================================================================
# Wrapper percentage error
# =============================================================================
def wrapper_percentage_error(data:np.array):
    return percentage_error(target=data[0], predicted=data[1])

# =============================================================================
# Mean absolute percentage error (MAPE)
# =============================================================================
def mean_absolute_percentage_error(target:np.array, predicted:np.array) -> float:
    return np.mean(percentage_error(target=target, predicted=predicted))

# =============================================================================
# Median absolute percentage error (MeAPE)
# =============================================================================
def median_absolute_percentage_error(target:np.array, predicted:np.array) -> float:
    return np.median(percentage_error(target=target, predicted=predicted))

# =============================================================================
# Energy production
# =============================================================================
def energy(irradiance:np.array, tmod:np.array, resolution:int, inverter:dict, module:dict, mps:int, spi:int, loss:float) -> float:
    # STEP 1. DC production (I-V curve)
    IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_cec(effective_irradiance=irradiance,
                                                            temp_cell=tmod,
                                                            alpha_sc=module['alpha_sc'],
                                                            a_ref=module['a_ref'],
                                                            I_L_ref=module['I_L_ref'],
                                                            I_o_ref=module['I_o_ref'],
                                                            R_sh_ref=module['R_sh_ref'],
                                                            R_s=module['R_s'],
                                                            Adjust=module['Adjust'],
                                                            EgRef=1.121,
                                                            dEgdT=-0.0002677)

    single_diode = pvlib.pvsystem.singlediode(photocurrent=IL,
                                              saturation_current=I0,
                                              resistance_series=Rs,
                                              resistance_shunt=Rsh,
                                              nNsVth=nNsVth,
                                              ivcurve_pnts=100,
                                              method='lambertw')

    iv_curve = pd.DataFrame({'i_sc': single_diode['i_sc'],
                             'v_oc': single_diode['v_oc'],
                             'i_mp': single_diode['i_mp'],
                             'v_mp': single_diode['v_mp'],
                             'p_mp': single_diode['p_mp'],
                             'i_x': single_diode['i_x'],
                             'i_xx': single_diode['i_xx']})

    # STEP 2. Scaling DC production
    dc = pd.DataFrame({'i_mp': iv_curve['i_mp'] * spi,
                       'v_mp': iv_curve['v_mp'] * mps,
                       'p_mp': iv_curve['p_mp'] * spi * mps})

    # STEP 3. DC losses
    losses = loss / 100

    dc['i_mp'] = dc['i_mp'] - dc['i_mp']*losses
    dc['p_mp'] = dc['p_mp'] - dc['p_mp']*losses

    # STEP 4. AC production
    ac = pvlib.inverter.sandia(v_dc=dc['v_mp'], p_dc=dc['p_mp'], inverter=inverter)
    ac[ac < 0] = 0

    # STEP 5. Acumulated energy
    min_to_hour = resolution/60

    return np.sum(ac * min_to_hour)