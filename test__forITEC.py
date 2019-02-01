import numpy as np
from scipy.interpolate import interp1d
import json
import math
import pandas as pd
import csv

run_beginning = False

urban = pd.read_csv('epa_urban_conventional_tj.csv').dropna()
highway = pd.read_csv('epa_highway_conventional_tj.csv').dropna()

urban.apply(pd.to_numeric)
highway.apply(pd.to_numeric)

urban_dic = urban.to_dict('list')
highway = highway.to_dict('list')

urban_dic['ct300_delta_tj_ave_igbt'] = [float(x) for x in urban_dic['ct300_delta_tj_ave_igbt']]
urban_dic['ct300_delta_tj_max_igbt'] = [float(x) for x in urban_dic['ct300_delta_tj_max_igbt']]
urban_dic['ct300_delta_tj_ave_fwd'] = [float(x) for x in urban_dic['ct300_delta_tj_ave_fwd']]
urban_dic['ct300_delta_tj_max_fwd'] = [float(x) for x in urban_dic['ct300_delta_tj_max_fwd']]


highway['ct300_delta_tj_ave_igbt'] = [float(x) for x in highway['ct300_delta_tj_ave_igbt']]
highway['ct300_delta_tj_max_igbt'] = [float(x) for x in highway['ct300_delta_tj_max_igbt']]
highway['ct300_delta_tj_ave_fwd'] = [float(x) for x in highway['ct300_delta_tj_ave_fwd']]
highway['ct300_delta_tj_max_fwd'] = [float(x) for x in highway['ct300_delta_tj_max_fwd']]

with open('EPA_highway_out_convetional_tj__.json', 'w') as f:
    json.dump(highway, f)

with open('EPA_urban_out_conventional_tj__.json', 'w') as f:
    json.dump(urban_dic, f)

if run_beginning:
    with open('EPA_highway.json') as f:
        EPA_highway = json.load(f)

    with open('EPA_urban.json') as f:
        EPA_urban = json.load(f)

    with open('nissan_leaf.json') as f:
        nissan_leaf = json.load(f)

    bus_voltage = 375
    power_factor = 0.8

    kilowatts = [val / 1.341 * 1000 for val in nissan_leaf['powerKW']]

    peak_current = [power * 2 / math.cos(power_factor) / 3 / bus_voltage for power in kilowatts]

    current_interp = interp1d(nissan_leaf['speed'], peak_current)

    EPA_highway.update({
        "current":
            [current_interp(speed).item() for speed in EPA_highway['speed']]
    })

    EPA_urban.update({
        "current":
            [current_interp(speed).item() for speed in EPA_urban['speed']]
    })

    nissan_leaf.update({
        "speed_fo":
            [0, 95],
        'fo':
            [0, 700]
    })

    rpm_interp = interp1d(nissan_leaf['speed_fo'], nissan_leaf['fo'])

    EPA_highway.update({
        "freq_out":
            [rpm_interp(speed).item() for speed in EPA_highway['speed']],
        'delta_t':
            np.clip(np.diff(EPA_highway['time']), 0, 999).tolist()
    })

    EPA_urban.update({
        "freq_out":
            [rpm_interp(speed).item() for speed in EPA_urban['speed']],
        'delta_t':
            np.clip(np.diff(EPA_urban['time']), 0, 999).tolist()
    })

    del EPA_highway['freq_out'][-1]
    del EPA_urban['freq_out'][-1]

    EPA_highway.update({
        "cycles":
            np.multiply(EPA_highway['delta_t'], EPA_highway['freq_out']).tolist()
    })

    EPA_urban.update({
        "cycles":
            np.multiply(EPA_urban['delta_t'], EPA_urban['freq_out']).tolist()
    })

    with open('EPA_highway_out.json', 'w') as f:
        json.dump(EPA_highway, f)

    with open('EPA_urban_out.json', 'w') as f:
        json.dump(EPA_urban, f)

with open('EPA_urban_out_conventional_tj__.json') as f:
    EPA_urban_tj = json.load(f)

with open('EPA_highway_out_convetional_tj__.json') as f:
    EPA_highway_tj = json.load(f)

delta_t_tpm = [50, 150]
pc_tpm = [13625388, 35342]

delta_t_7th = [30, 100.78097]
pc_7th = [2.176771E7, 29355.777]


slope = np.log(pc_7th[0] / pc_7th[1]) / np.log(delta_t_7th[0] / delta_t_7th[1])
# out = pc[1]*(x/delta_t[1])^m

EPA_highway_tj.update({
    'ct300_delta_t_igbt_small': (2*np.clip(np.subtract( EPA_highway_tj['ct300_delta_tj_max_igbt'], EPA_highway_tj['ct300_delta_tj_ave_igbt']),0,10000)).tolist(),
    'ct300_delta_t_igbt_large': (np.clip(np.insert(np.diff(EPA_highway_tj['ct300_delta_tj_ave_igbt']),0,EPA_highway_tj['ct300_delta_tj_ave_igbt'][0]),0,10000)).tolist(),
    'ct300_delta_t_fwd_small':  (2*np.clip(np.subtract( EPA_highway_tj['ct300_delta_tj_max_fwd'], EPA_highway_tj['ct300_delta_tj_ave_fwd']),0,10000)).tolist(),
    'ct300_delta_t_fwd_large':  (np.clip(np.insert(np.diff(EPA_highway_tj['ct300_delta_tj_ave_fwd']),0,EPA_highway_tj['ct300_delta_tj_ave_fwd'][0]),0,10000)).tolist(),
    'ct600_delta_t_igbt_small': (2*np.clip(np.subtract( EPA_highway_tj['ct600_delta_tj_max_igbt'], EPA_highway_tj['ct600_delta_tj_ave_igbt']),0,10000)).tolist(),
    'ct600_delta_t_igbt_large': (np.clip(np.insert(np.diff(EPA_highway_tj['ct600_delta_tj_ave_igbt']),0,EPA_highway_tj['ct600_delta_tj_ave_igbt'][0]),0,10000)).tolist(),
    'ct600_delta_t_fwd_small':  (2*np.clip(np.subtract( EPA_highway_tj['ct600_delta_tj_max_fwd'], EPA_highway_tj['ct600_delta_tj_ave_fwd']),0,10000)).tolist(),
    'ct600_delta_t_fwd_large':  (np.clip(np.insert(np.diff(EPA_highway_tj['ct600_delta_tj_ave_fwd']),0,EPA_highway_tj['ct600_delta_tj_ave_fwd'][0]),0,10000)).tolist()
})

EPA_highway_tj.update({
    'ct300_delta_tj_igbt_small__cycles': (pc_tpm[1] * np.power(np.divide(EPA_highway_tj['ct300_delta_t_igbt_small'], delta_t_7th[1]), slope)).tolist(),
    'ct300_delta_tj_igbt_large__cycles': (pc_tpm[1] * np.power(np.divide(EPA_highway_tj['ct300_delta_t_igbt_large'], delta_t_7th[1]), slope)).tolist(),
    'ct300_delta_tj_fwd_small__cycles':  (pc_tpm[1] * np.power(np.divide(EPA_highway_tj['ct300_delta_t_fwd_small'], delta_t_7th[1]), slope)).tolist(),
    'ct300_delta_tj_fwd_large__cycles':  (pc_tpm[1] * np.power(np.divide(EPA_highway_tj['ct300_delta_t_fwd_large'], delta_t_7th[1]), slope)).tolist(),
    'ct600_delta_tj_igbt_small__cycles': (pc_tpm[1] * np.power(np.divide(EPA_highway_tj['ct600_delta_t_igbt_small'], delta_t_7th[1]), slope)).tolist(),
    'ct600_delta_tj_igbt_large__cycles': (pc_tpm[1] * np.power(np.divide(EPA_highway_tj['ct600_delta_t_igbt_large'], delta_t_7th[1]), slope)).tolist(),
    'ct600_delta_tj_fwd_small__cycles':  (pc_tpm[1] * np.power(np.divide(EPA_highway_tj['ct600_delta_t_fwd_small'], delta_t_7th[1]), slope)).tolist(),
    'ct600_delta_tj_fwd_large__cycles':  (pc_tpm[1] * np.power(np.divide(EPA_highway_tj['ct600_delta_t_fwd_large'], delta_t_7th[1]), slope)).tolist()
})


EPA_highway_tj.update({
    'ct300_delta_tj_igbt_small__lifetime_percent': np.divide(EPA_highway_tj['cycles'], EPA_highway_tj['ct300_delta_tj_igbt_small__cycles']).tolist(),
    'ct300_delta_tj_igbt_large__lifetime_percent': np.divide(EPA_highway_tj['cycles'], EPA_highway_tj['ct300_delta_tj_igbt_large__cycles']).tolist(),
    'ct300_delta_tj_fwd_small__lifetime_percent':  np.divide(EPA_highway_tj['cycles'], EPA_highway_tj['ct300_delta_tj_fwd_small__cycles']).tolist(),
    'ct300_delta_tj_fwd_large__lifetime_percent':  np.divide(EPA_highway_tj['cycles'], EPA_highway_tj['ct300_delta_tj_fwd_large__cycles']).tolist(),
    'ct600_delta_tj_igbt_small__lifetime_percent': np.divide(EPA_highway_tj['cycles'], EPA_highway_tj['ct600_delta_tj_igbt_small__cycles']).tolist(),
    'ct600_delta_tj_igbt_large__lifetime_percent': np.divide(EPA_highway_tj['cycles'], EPA_highway_tj['ct600_delta_tj_igbt_large__cycles']).tolist(),
    'ct600_delta_tj_fwd_small__lifetime_percent':  np.divide(EPA_highway_tj['cycles'], EPA_highway_tj['ct600_delta_tj_fwd_small__cycles']).tolist(),
    'ct600_delta_tj_fwd_large__lifetime_percent':  np.divide(EPA_highway_tj['cycles'], EPA_highway_tj['ct600_delta_tj_fwd_large__cycles']).tolist()
})

EPA_highway_tj.update({
    'ct300_delta_tj_igbt_small__lifetime_sum': np.sum(EPA_highway_tj['ct300_delta_tj_igbt_small__lifetime_percent']).item(),
    'ct300_delta_tj_igbt_large__lifetime_sum': np.sum(EPA_highway_tj['ct300_delta_tj_igbt_large__lifetime_percent']).item(),
    'ct300_delta_tj_fwd_small__lifetime_sum':  np.sum(EPA_highway_tj['ct300_delta_tj_fwd_small__lifetime_percent']).item(),
    'ct300_delta_tj_fwd_large__lifetime_sum':  np.sum(EPA_highway_tj['ct300_delta_tj_fwd_large__lifetime_percent']).item(),
    'ct600_delta_tj_igbt_small__lifetime_sum': np.sum(EPA_highway_tj['ct600_delta_tj_igbt_small__lifetime_percent']).item(),
    'ct600_delta_tj_igbt_large__lifetime_sum': np.sum(EPA_highway_tj['ct600_delta_tj_igbt_large__lifetime_percent']).item(),
    'ct600_delta_tj_fwd_small__lifetime_sum':  np.sum(EPA_highway_tj['ct600_delta_tj_fwd_small__lifetime_percent']).item(),
    'ct600_delta_tj_fwd_large__lifetime_sum':  np.sum(EPA_highway_tj['ct600_delta_tj_fwd_large__lifetime_percent']).item()
})

EPA_highway_tj.update({
    'ct300_delta_tj_igbt__lifetime_sum': EPA_highway_tj['ct300_delta_tj_igbt_small__lifetime_sum'] + EPA_highway_tj['ct300_delta_tj_igbt_large__lifetime_sum'],
    'ct300_delta_tj_fwd__lifetime_sum':  EPA_highway_tj['ct300_delta_tj_fwd_small__lifetime_sum'] + EPA_highway_tj['ct300_delta_tj_fwd_large__lifetime_sum'],
    'ct600_delta_tj_igbt__lifetime_sum': EPA_highway_tj['ct600_delta_tj_igbt_small__lifetime_sum'] +EPA_highway_tj['ct600_delta_tj_igbt_large__lifetime_sum'],
    'ct600_delta_tj_fwd__lifetime_sum':  EPA_highway_tj['ct600_delta_tj_fwd_small__lifetime_sum'] + EPA_highway_tj['ct600_delta_tj_fwd_large__lifetime_sum']
})

EPA_highway_tj.update({
    'ct300_delta_tj_module__lifetime_sum': EPA_highway_tj['ct300_delta_tj_igbt__lifetime_sum'] + EPA_highway_tj['ct300_delta_tj_fwd__lifetime_sum'],
    'ct600_delta_tj_module__lifetime_sum': EPA_highway_tj['ct600_delta_tj_igbt__lifetime_sum'] +EPA_highway_tj['ct300_delta_tj_fwd__lifetime_sum']
})

EPA_highway_tj.update({
    'ct300_delta_tj_module__lifetime_estimate': np.reciprocal(EPA_highway_tj['ct300_delta_tj_module__lifetime_sum']).item(),
    'ct600_delta_tj_module__lifetime_estimate': np.reciprocal(EPA_highway_tj['ct600_delta_tj_module__lifetime_sum']).item()
})

EPA_urban_tj.update({
    'ct300_delta_t_igbt_small': (2*np.clip(np.subtract( EPA_urban_tj['ct300_delta_tj_max_igbt'], EPA_urban_tj['ct300_delta_tj_ave_igbt']),0,10000)).tolist(),
    'ct300_delta_t_igbt_large': (np.clip(np.insert(np.diff(EPA_urban_tj['ct300_delta_tj_ave_igbt']),0,EPA_urban_tj['ct300_delta_tj_ave_igbt'][0]),0,10000)).tolist(),
    'ct300_delta_t_fwd_small':  (2*np.clip(np.subtract( EPA_urban_tj['ct300_delta_tj_max_fwd'], EPA_urban_tj['ct300_delta_tj_ave_fwd']),0,10000)).tolist(),
    'ct300_delta_t_fwd_large':  (np.clip(np.insert(np.diff(EPA_urban_tj['ct300_delta_tj_ave_fwd']),0,EPA_urban_tj['ct300_delta_tj_ave_fwd'][0]),0,10000)).tolist(),
    'ct600_delta_t_igbt_small': (2*np.clip(np.subtract( EPA_urban_tj['ct600_delta_tj_max_igbt'], EPA_urban_tj['ct600_delta_tj_ave_igbt']),0,10000)).tolist(),
    'ct600_delta_t_igbt_large': (np.clip(np.insert(np.diff(EPA_urban_tj['ct600_delta_tj_ave_igbt']),0,EPA_urban_tj['ct600_delta_tj_ave_igbt'][0]),0,10000)).tolist(),
    'ct600_delta_t_fwd_small':  (2*np.clip(np.subtract( EPA_urban_tj['ct600_delta_tj_max_fwd'], EPA_urban_tj['ct600_delta_tj_ave_fwd']),0,10000)).tolist(),
    'ct600_delta_t_fwd_large':  (np.clip(np.insert(np.diff(EPA_urban_tj['ct600_delta_tj_ave_fwd']),0,EPA_urban_tj['ct600_delta_tj_ave_fwd'][0]),0,10000)).tolist()
})

EPA_urban_tj.update({
    'ct300_delta_tj_igbt_small__cycles': (pc_tpm[1] * np.power(np.divide(EPA_urban_tj['ct300_delta_t_igbt_small'], delta_t_7th[1]), slope)).tolist(),
    'ct300_delta_tj_igbt_large__cycles': (pc_tpm[1] * np.power(np.divide(EPA_urban_tj['ct300_delta_t_igbt_large'], delta_t_7th[1]), slope)).tolist(),
    'ct300_delta_tj_fwd_small__cycles':  (pc_tpm[1] * np.power(np.divide(EPA_urban_tj['ct300_delta_t_fwd_small'], delta_t_7th[1]), slope)).tolist(),
    'ct300_delta_tj_fwd_large__cycles':  (pc_tpm[1] * np.power(np.divide(EPA_urban_tj['ct300_delta_t_fwd_large'], delta_t_7th[1]), slope)).tolist(),
    'ct600_delta_tj_igbt_small__cycles': (pc_tpm[1] * np.power(np.divide(EPA_urban_tj['ct600_delta_t_igbt_small'], delta_t_7th[1]), slope)).tolist(),
    'ct600_delta_tj_igbt_large__cycles': (pc_tpm[1] * np.power(np.divide(EPA_urban_tj['ct600_delta_t_igbt_large'], delta_t_7th[1]), slope)).tolist(),
    'ct600_delta_tj_fwd_small__cycles':  (pc_tpm[1] * np.power(np.divide(EPA_urban_tj['ct600_delta_t_fwd_small'], delta_t_7th[1]), slope)).tolist(),
    'ct600_delta_tj_fwd_large__cycles':  (pc_tpm[1] * np.power(np.divide(EPA_urban_tj['ct600_delta_t_fwd_large'], delta_t_7th[1]), slope)).tolist()
})


EPA_urban_tj.update({
    'ct300_delta_tj_igbt_small__lifetime_percent': np.divide(EPA_urban_tj['cycles'], EPA_urban_tj['ct300_delta_tj_igbt_small__cycles']).tolist(),
    'ct300_delta_tj_igbt_large__lifetime_percent': np.divide(EPA_urban_tj['cycles'], EPA_urban_tj['ct300_delta_tj_igbt_large__cycles']).tolist(),
    'ct300_delta_tj_fwd_small__lifetime_percent':  np.divide(EPA_urban_tj['cycles'], EPA_urban_tj['ct300_delta_tj_fwd_small__cycles']).tolist(),
    'ct300_delta_tj_fwd_large__lifetime_percent':  np.divide(EPA_urban_tj['cycles'], EPA_urban_tj['ct300_delta_tj_fwd_large__cycles']).tolist(),
    'ct600_delta_tj_igbt_small__lifetime_percent': np.divide(EPA_urban_tj['cycles'], EPA_urban_tj['ct600_delta_tj_igbt_small__cycles']).tolist(),
    'ct600_delta_tj_igbt_large__lifetime_percent': np.divide(EPA_urban_tj['cycles'], EPA_urban_tj['ct600_delta_tj_igbt_large__cycles']).tolist(),
    'ct600_delta_tj_fwd_small__lifetime_percent':  np.divide(EPA_urban_tj['cycles'], EPA_urban_tj['ct600_delta_tj_fwd_small__cycles']).tolist(),
    'ct600_delta_tj_fwd_large__lifetime_percent':  np.divide(EPA_urban_tj['cycles'], EPA_urban_tj['ct600_delta_tj_fwd_large__cycles']).tolist()
})

EPA_urban_tj.update({
    'ct300_delta_tj_igbt_small__lifetime_sum': np.sum(EPA_urban_tj['ct300_delta_tj_igbt_small__lifetime_percent']).item(),
    'ct300_delta_tj_igbt_large__lifetime_sum': np.sum(EPA_urban_tj['ct300_delta_tj_igbt_large__lifetime_percent']).item(),
    'ct300_delta_tj_fwd_small__lifetime_sum':  np.sum(EPA_urban_tj['ct300_delta_tj_fwd_small__lifetime_percent']).item(),
    'ct300_delta_tj_fwd_large__lifetime_sum':  np.sum(EPA_urban_tj['ct300_delta_tj_fwd_large__lifetime_percent']).item(),
    'ct600_delta_tj_igbt_small__lifetime_sum': np.sum(EPA_urban_tj['ct600_delta_tj_igbt_small__lifetime_percent']).item(),
    'ct600_delta_tj_igbt_large__lifetime_sum': np.sum(EPA_urban_tj['ct600_delta_tj_igbt_large__lifetime_percent']).item(),
    'ct600_delta_tj_fwd_small__lifetime_sum':  np.sum(EPA_urban_tj['ct600_delta_tj_fwd_small__lifetime_percent']).item(),
    'ct600_delta_tj_fwd_large__lifetime_sum':  np.sum(EPA_urban_tj['ct600_delta_tj_fwd_large__lifetime_percent']).item()
})

EPA_urban_tj.update({
    'ct300_delta_tj_igbt__lifetime_sum': EPA_urban_tj['ct300_delta_tj_igbt_small__lifetime_sum'] + EPA_urban_tj['ct300_delta_tj_igbt_large__lifetime_sum'],
    'ct300_delta_tj_fwd__lifetime_sum':  EPA_urban_tj['ct300_delta_tj_fwd_small__lifetime_sum'] + EPA_urban_tj['ct300_delta_tj_fwd_large__lifetime_sum'],
    'ct600_delta_tj_igbt__lifetime_sum': EPA_urban_tj['ct600_delta_tj_igbt_small__lifetime_sum'] +EPA_urban_tj['ct600_delta_tj_igbt_large__lifetime_sum'],
    'ct600_delta_tj_fwd__lifetime_sum':  EPA_urban_tj['ct600_delta_tj_fwd_small__lifetime_sum'] + EPA_urban_tj['ct600_delta_tj_fwd_large__lifetime_sum']
})

EPA_urban_tj.update({
    'ct300_delta_tj_module__lifetime_sum': EPA_urban_tj['ct300_delta_tj_igbt__lifetime_sum'] + EPA_urban_tj['ct300_delta_tj_fwd__lifetime_sum'],
    'ct600_delta_tj_module__lifetime_sum': EPA_urban_tj['ct600_delta_tj_igbt__lifetime_sum'] +EPA_urban_tj['ct300_delta_tj_fwd__lifetime_sum']
})

EPA_urban_tj.update({
    'ct300_delta_tj_module__lifetime_estimate': np.reciprocal(EPA_urban_tj['ct300_delta_tj_module__lifetime_sum']).item(),
    'ct600_delta_tj_module__lifetime_estimate': np.reciprocal(EPA_urban_tj['ct600_delta_tj_module__lifetime_sum']).item()
})

with open('epa_highway_convetional_calcs.json', 'w') as f:
    json.dump(EPA_highway_tj, f)

cow = list(EPA_highway_tj.keys())

for key in cow:
    EPA_highway_tj[key+"_urb_conventional"] = EPA_highway_tj.pop(key)

with open('epa_urban_convetional_calcs.json', 'w') as f:
    json.dump(EPA_urban_tj, f)

cow = list(EPA_urban_tj.keys())

for key in cow:
    EPA_urban_tj[key+"_hwy_conventional"] = EPA_urban_tj.pop(key)

with open('epa_highway_tpm_calcs.json') as f:
    highway_tpm = json.load(f)

for key in cow:
    highway_tpm[key+"_hwy_tpm"] = highway_tpm.pop(key)

with open('epa_urban_tpm_calcs.json') as f:
    urban_tpm = json.load(f)


for key in cow:
    urban_tpm[key+"_urb_tpm"] = urban_tpm.pop(key)

master = {}
for k, v in EPA_highway_tj.items():
    master.update({k:v})
for k, v in EPA_urban_tj.items():
    master.update({k:v})
for k, v in urban_tpm.items():
    master.update({k:v})
for k, v in highway_tpm.items():
    master.update({k:v})

with open('dict.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    for k,v in master.items():
        writer.writerow([k,v])
