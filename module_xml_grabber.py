import json
import copy
import xmltodict


def rename_section(file, module_value, old_string, new_string):
    file[module_value][new_string] = file[module_value][old_string]
    del file[module_value][old_string]
    return file


with open('FullModules.xml', errors='ignore') as f:
    files = xmltodict.parse(f.read())

clean_files_list = files['xml']['DataSheet']['Module']

clean_files = {}

print(clean_files_list[0]['Name'])

for x in range(len(clean_files_list)):
    clean_files[str(clean_files_list[x]['Name']) + " @ TJ=" + str(clean_files_list[x]['Tch'])] = clean_files_list[x]

for value in clean_files:
    if clean_files[value]['Division'] == 'DIP-CIB':
        clean_files[value]['Division'] = 'DIPIPM'

    if clean_files[value]['Division'] == 'HVIGBT_MOD':
        clean_files[value]['Division'] = 'HVIGBT'

    if clean_files[value]['Division'] == 'DIODE_MOD':
        clean_files[value]['Division'] = 'HVIGBT'

    if clean_files[value]['Division'] == 'IGBT_MOD':
        clean_files[value]['Division'] = 'Industrial IGBT'

    if clean_files[value]['Division'] == 'IPM':
        clean_files[value]['Division'] = 'Industrial IPM'

    if clean_files[value]['Division'] == 'MOS_MOD':
        clean_files[value]['Division'] = 'MOSFET Modules'
        # clean_files = rename_value(clean_files,value,'Division','Old')

    clean_files = rename_section(clean_files, value, 'Vcc', 'vcc_value')
    clean_files = rename_section(clean_files, value, 'ThermalContactResistance', 'Module RTH DC')
    clean_files = rename_section(clean_files, value, 'RatedVoltage', 'Nameplate Voltage')
    clean_files = rename_section(clean_files, value, 'RatedCurrent', 'Nameplate Current')
    clean_files = rename_section(clean_files, value, 'BaseData', 'base_data_unknown')
    clean_files = rename_section(clean_files, value, 'Deprecation', 'deprecation_unknown')
    clean_files = rename_section(clean_files, value, 'ElementNumber', 'number_of_switches')
    clean_files = rename_section(clean_files, value, 'InterpolationDegree', 'interp_degree')
    clean_files = rename_section(clean_files, value, 'Lower', 'lower_unknown')
    clean_files = rename_section(clean_files, value, 'ModDate', 'mod_date')
    clean_files = rename_section(clean_files, value, 'ModUser', 'mod_user')
    clean_files = rename_section(clean_files, value, 'PathEn', 'path_en')
    clean_files = rename_section(clean_files, value, 'PathJa', 'path_ja')
    # clean_files = rename_section(clean_files, value, 'Priority', 'priority_unknown')
    clean_files = rename_section(clean_files, value, 'RthCf', 'CF RTH DC')
    clean_files = rename_section(clean_files, value, 'RthDi', 'FWD RTH DC')
    clean_files = rename_section(clean_files, value, 'RthTr', 'IGBT RTH DC')
    clean_files = rename_section(clean_files, value, 'Segment', 'segment')
    clean_files = rename_section(clean_files, value, 'SwitchingElement', 'switching_element_unknown')
    clean_files[value]['melco_data_unused'] = {}
    clean_files[value]['min_base_and_max_vals'] = {}
    clean_files[value]['melco_data_unused'].update({'number_of_switches': clean_files[value]['number_of_switches']})

    clean_files[value]['melco_data_unused'].update({'interp_degree': clean_files[value]['interp_degree']})
    clean_files[value]['melco_data_unused'].update({'path_ja': clean_files[value]['path_ja']})
    clean_files[value]['melco_data_unused'].update({'path_en': clean_files[value]['path_en']})
    clean_files[value]['melco_data_unused'].update({'mod_user': clean_files[value]['mod_user']})
    clean_files[value]['melco_data_unused'].update({'mod_date': clean_files[value]['mod_date']})
    clean_files[value]['melco_data_unused'].update({'base_data_unknown': clean_files[value]['base_data_unknown']})
    # clean_files[value]['melco_data_unused'].update({'priority_unknown': clean_files[value]['priority_unknown']})
    clean_files[value]['melco_data_unused'].update({'deprecation_unknown': clean_files[value]['deprecation_unknown']})
    clean_files[value]['melco_data_unused'].update({'segment': clean_files[value]['segment'],
                                                    'switching_element_unknown': clean_files[value]['switching_element_unknown'],
                                                    'lower_unknown': clean_files[value]['lower_unknown']})
    clean_files[value]['min_base_and_max_vals'].update({
        'fsw_base': clean_files[value]['fswFc'],
        'tsink_base': clean_files[value]['Tf'],
        'rgon_base': clean_files[value]['RgOn'],
        'rgoff_base': clean_files[value]['RgOff'],
        'power_factor_base': clean_files[value]['PF'],
        'output_current_base': clean_files[value]['Icp'],
        'output_current_max': clean_files[value]['IcpMax'],
        'output_current_min': clean_files[value]['IcpMin'],
        'vcc_max': clean_files[value]['VccMax'],
        'vcc_min': clean_files[value]['VccMin'],
        'fsw_max': clean_files[value]['fswMax'],
        'fsw_min': clean_files[value]['fswMin'],
        'tsink_max': clean_files[value]['TfMax'],
        'tsink_min': clean_files[value]['TfMin'],
        'rg_on_max': clean_files[value]['RgOnMax'],
        'rg_on_min': clean_files[value]['RgOnMin'],
        'rg_off_max': clean_files[value]['RgOffMax'],
        'rg_off_min': clean_files[value]['RgOffMin'],
        'power_factor_max': clean_files[value]['PFMax'],
        'power_factor_min': clean_files[value]['PFMin'],
        'output_current_display_max': clean_files[value]['IcpDisplayMax'],
        'fsw_display_max': clean_files[value]['fcDisplayMax'],
        'fo_base': clean_files[value]['fo'],
        'fo_max': clean_files[value]['foMax'],
        'fo_min': clean_files[value]['foMin'],
        'junc_temp_max': clean_files[value]['Tj'],
        'junc_temp_tested': clean_files[value]['Tch'],
        'case_temp_max': clean_files[value]['TcMax']
    })
    del clean_files[value]['number_of_switches']
    del clean_files[value]['fswFc']
    del clean_files[value]['Tf']
    del clean_files[value]['RgOn']
    del clean_files[value]['RgOff']
    del clean_files[value]['Icp']
    del clean_files[value]['PF']
    del clean_files[value]['IcpMax']
    del clean_files[value]['IcpMin']
    del clean_files[value]['VccMax']
    del clean_files[value]['VccMin']
    del clean_files[value]['fswMax']
    del clean_files[value]['fswMin']
    del clean_files[value]['TfMax']
    del clean_files[value]['TfMin']
    del clean_files[value]['RgOnMax']
    del clean_files[value]['RgOnMin']
    del clean_files[value]['RgOffMax']
    del clean_files[value]['RgOffMin']
    del clean_files[value]['PFMax']
    del clean_files[value]['PFMin']
    del clean_files[value]['IcpDisplayMax']
    del clean_files[value]['fcDisplayMax']
    del clean_files[value]['fo']
    del clean_files[value]['foMax']
    del clean_files[value]['foMin']
    del clean_files[value]['Tj']
    del clean_files[value]['Tch']
    del clean_files[value]['TcMax']

    del clean_files[value]['segment']
    del clean_files[value]['lower_unknown']
    del clean_files[value]['switching_element_unknown']

    del clean_files[value]['interp_degree']
    del clean_files[value]['path_ja']
    del clean_files[value]['path_en']
    del clean_files[value]['mod_user']
    del clean_files[value]['mod_date']
    del clean_files[value]['base_data_unknown']
    # del clean_files[value]['priority_unknown']
    del clean_files[value]['deprecation_unknown']

    ic_temp__ic_vce = []
    vce_temp__ic_vce = []

    for ic_pair in range(len(clean_files[value]['IcVce'])):
        ic_temp__ic_vce.append(clean_files[value]['IcVce'][ic_pair]['Ic'])
        vce_temp__ic_vce.append(clean_files[value]['IcVce'][ic_pair]['Vce'])

    del clean_files[value]['IcVce']
    clean_files[value]['ic_vce'] = {}
    clean_files[value]['ic_vce']['ic__ic_vce'] = ic_temp__ic_vce
    clean_files[value]['ic_vce']['vce__ic_vce'] = vce_temp__ic_vce

    ####

    if_temp__if_vf = []
    vf_temp__if_vf = []

    for ic_pair in range(len(clean_files[value]['IcVf'])):
        if_temp__if_vf.append(clean_files[value]['IcVf'][ic_pair]['Ic'])
        vf_temp__if_vf.append(clean_files[value]['IcVf'][ic_pair]['Vf'])

    del clean_files[value]['IcVf']
    clean_files[value]['if_vf'] = {}
    clean_files[value]['if_vf']['if__if_vf'] = if_temp__if_vf
    clean_files[value]['if_vf']['vf__if_vf'] = vf_temp__if_vf

    ic__ic_esw_on__temp = []
    esw_on__ic_esw_on__temp = []
    for pair in range(len(clean_files[value]['IcEswOn'])):
        ic__ic_esw_on__temp.append(clean_files[value]['IcEswOn'][pair]['Ic'])
        esw_on__ic_esw_on__temp.append(clean_files[value]['IcEswOn'][pair]['EswOn'])
    del clean_files[value]['IcEswOn']
    clean_files[value]['ic_esw_on'] = {}
    clean_files[value]['ic_esw_on']['ic__ic_esw_on'] = ic__ic_esw_on__temp
    clean_files[value]['ic_esw_on']['esw_on__ic_esw_on'] = esw_on__ic_esw_on__temp

    ic__ic_esw_off__temp = []
    esw_off__ic_esw_off__temp = []
    for pair in range(len(clean_files[value]['IcEswOff'])):
        ic__ic_esw_off__temp.append(clean_files[value]['IcEswOff'][pair]['Ic'])
        esw_off__ic_esw_off__temp.append(clean_files[value]['IcEswOff'][pair]['EswOff'])
    del clean_files[value]['IcEswOff']
    clean_files[value]['ic_esw_off'] = {}
    clean_files[value]['ic_esw_off']['ic__ic_esw_off'] = ic__ic_esw_off__temp
    clean_files[value]['ic_esw_off']['esw_off__ic_esw_off'] = esw_off__ic_esw_off__temp

    ic__ic_err__temp = []
    err__ic_err__temp = []
    for pair in range(len(clean_files[value]['IcErr'])):
        ic__ic_err__temp.append(clean_files[value]['IcErr'][pair]['Ic'])
        err__ic_err__temp.append(clean_files[value]['IcErr'][pair]['Err'])
    del clean_files[value]['IcErr']
    clean_files[value]['ic_err'] = {}
    clean_files[value]['ic_err']['ic__ic_err'] = ic__ic_err__temp
    clean_files[value]['ic_err']['err__ic_err'] = err__ic_err__temp

    rg_on__rg_on_esw_on__temp = []
    esw_on__rg_on_esw_on__temp = []
    for pair in range(len(clean_files[value]['RgEswOn'])):
        rg_on__rg_on_esw_on__temp.append(clean_files[value]['RgEswOn'][pair]['Rg'])
        esw_on__rg_on_esw_on__temp.append(clean_files[value]['RgEswOn'][pair]['EswOn'])
    del clean_files[value]['RgEswOn']
    clean_files[value]['rg_on_esw_on'] = {}
    clean_files[value]['rg_on_esw_on']['rg_on__rg_on_esw_on'] = rg_on__rg_on_esw_on__temp
    clean_files[value]['rg_on_esw_on']['esw_on__rg_on_esw_on'] = esw_on__rg_on_esw_on__temp

    rg_off__rg_off_esw_off__temp = []
    esw_off__rg_off_esw_off__temp = []
    for pair in range(len(clean_files[value]['RgEswOff'])):
        rg_off__rg_off_esw_off__temp.append(clean_files[value]['RgEswOff'][pair]['Rg'])
        esw_off__rg_off_esw_off__temp.append(clean_files[value]['RgEswOff'][pair]['EswOff'])
    del clean_files[value]['RgEswOff']
    clean_files[value]['rg_off_esw_off'] = {}
    clean_files[value]['rg_off_esw_off']['rg_off__rg_off_esw_off'] = rg_off__rg_off_esw_off__temp
    clean_files[value]['rg_off_esw_off']['esw_off__rg_off_esw_off'] = esw_off__rg_off_esw_off__temp

    rg_on__rg_on_err__temp = []
    err__rg_on_err__temp = []
    for pair in range(len(clean_files[value]['RgErr'])):
        rg_on__rg_on_err__temp.append(clean_files[value]['RgErr'][pair]['Rg'])
        err__rg_on_err__temp.append(clean_files[value]['RgErr'][pair]['Err'])
    del clean_files[value]['RgErr']
    clean_files[value]['rg_on_err'] = {}
    clean_files[value]['rg_on_err']['rg_on__rg_on_err'] = rg_on__rg_on_err__temp
    clean_files[value]['rg_on_err']['err__rg_on_err'] = err__rg_on_err__temp

    vcc__vcc_esw_on__temp = []
    esw_on__vcc_esw_on__temp = []
    for pair in range(len(clean_files[value]['VccEswOn'])):
        vcc__vcc_esw_on__temp.append(clean_files[value]['VccEswOn'][pair]['Vcc'])
        esw_on__vcc_esw_on__temp.append(clean_files[value]['VccEswOn'][pair]['EswOn'])
    del clean_files[value]['VccEswOn']
    clean_files[value]['vcc_esw_on'] = {}
    clean_files[value]['vcc_esw_on']['vcc__vcc_esw_on'] = vcc__vcc_esw_on__temp
    clean_files[value]['vcc_esw_on']['esw_on__vcc_esw_on'] = esw_on__vcc_esw_on__temp

    vcc__vcc_esw_off__temp = []
    esw_off__vcc_esw_off__temp = []
    for pair in range(len(clean_files[value]['VccEswOff'])):
        vcc__vcc_esw_off__temp.append(clean_files[value]['VccEswOff'][pair]['Vcc'])
        esw_off__vcc_esw_off__temp.append(clean_files[value]['VccEswOff'][pair]['EswOff'])
    del clean_files[value]['VccEswOff']
    clean_files[value]['vcc_esw_off'] = {}
    clean_files[value]['vcc_esw_off']['vcc__vcc_esw_off'] = vcc__vcc_esw_off__temp
    clean_files[value]['vcc_esw_off']['esw_off__vcc_esw_off'] = esw_off__vcc_esw_off__temp

    vcc__vcc_err__temp = []
    err__vcc_err__temp = []
    for pair in range(len(clean_files[value]['VccErr'])):
        vcc__vcc_err__temp.append(clean_files[value]['VccErr'][pair]['Vcc'])
        err__vcc_err__temp.append(clean_files[value]['VccErr'][pair]['Err'])
    del clean_files[value]['VccErr']
    clean_files[value]['vcc_err'] = {}
    clean_files[value]['vcc_err']['vcc__vcc_err'] = vcc__vcc_err__temp
    clean_files[value]['vcc_err']['err__vcc_err'] = err__vcc_err__temp

    if 'IdVsdOn' in clean_files[value]:
        id__id_vsd_on__temp = []
        vsd_on__vsd_on_id_vsd_on__temp = []
        for pair in range(len(clean_files[value]['IdVsdOn'])):
            id__id_vsd_on__temp.append(clean_files[value]['IdVsdOn'][pair]['Id'])
            vsd_on__vsd_on_id_vsd_on__temp.append(clean_files[value]['IdVsdOn'][pair]['VsdOn'])
        del clean_files[value]['IdVsdOn']
        clean_files[value]['id_vsd_on'] = {}
        clean_files[value]['id_vsd_on']['id__id_vsd_on'] = id__id_vsd_on__temp
        clean_files[value]['id_vsd_on']['vsd_on__vsd_on_id_vsd_on'] = vsd_on__vsd_on_id_vsd_on__temp
    else:
        id__id_vsd_on__temp = [1, 10000]
        vsd_on__vsd_on_id_vsd_on__temp = [1, 1]

    clean_files[value]['IGBT R Values'] = []
    clean_files[value]['IGBT T Values'] = []
    clean_files[value]['FWD R Values'] = []
    clean_files[value]['FWD T Values'] = []

    for rth_val in range(0, 4):
        if rth_val == 0:
            igbt_r = clean_files[value]['R1TrPerR0']
            igbt_t = clean_files[value]['T1TrPerJ1']
            fwd_r = clean_files[value]['R1aDiPerRd0']
            fwd_t = clean_files[value]['T1aDiPerJd1']

        if rth_val == 1:
            igbt_r = clean_files[value]['R2TrPerJ0']
            igbt_t = clean_files[value]['T2TrPerT1']
            fwd_r = clean_files[value]['R2aDiPerJd0']
            fwd_t = clean_files[value]['T2aDiPerTd1']

        if rth_val == 2:
            igbt_r = clean_files[value]['R3TrPerT0']
            igbt_t = clean_files[value]['T3Tr']
            fwd_r = clean_files[value]['R3aDiPerTd0']
            fwd_t = clean_files[value]['T3aDi']

        if rth_val == 3:
            igbt_r = clean_files[value]['R4TrPerR1']
            igbt_t = clean_files[value]['T4Tr']
            fwd_r = clean_files[value]['R4aDiPerRd1']
            fwd_t = clean_files[value]['T4aDi']

        clean_files[value]['IGBT R Values'].append(igbt_r)
        clean_files[value]['IGBT T Values'].append(igbt_t)
        clean_files[value]['FWD R Values'].append(fwd_r)
        clean_files[value]['FWD T Values'].append(fwd_t)

    del clean_files[value]['R1TrPerR0']
    del clean_files[value]['T1TrPerJ1']
    del clean_files[value]['R1aDiPerRd0']
    del clean_files[value]['T1aDiPerJd1']

    del clean_files[value]['R2TrPerJ0']
    del clean_files[value]['T2TrPerT1']
    del clean_files[value]['R2aDiPerJd0']
    del clean_files[value]['T2aDiPerTd1']

    del clean_files[value]['R3TrPerT0']
    del clean_files[value]['T3Tr']
    del clean_files[value]['R3aDiPerTd0']
    del clean_files[value]['T3aDi']

    del clean_files[value]['R4TrPerR1']
    del clean_files[value]['T4Tr']
    del clean_files[value]['R4aDiPerRd1']
    del clean_files[value]['T4aDi']

clean_files_div = {}

for value in clean_files:
    if clean_files[value]['Division'] in clean_files_div.keys():
        clean_files_temp = clean_files[value]['Division']
        del clean_files[value]['Division']
        clean_files_div[clean_files_temp].update({value: clean_files[value]})
    else:
        clean_files_temp = clean_files[value]['Division']
        del clean_files[value]['Division']
        clean_files_div.update({clean_files_temp: {value: clean_files[value]}})

clean_files = clean_files_div

del clean_files_div
del clean_files_list
del clean_files_temp
del err__ic_err__temp
del err__rg_on_err__temp
del vcc__vcc_err__temp
del err__vcc_err__temp
del esw_off__ic_esw_off__temp
del esw_off__rg_off_esw_off__temp
del esw_off__vcc_esw_off__temp
del esw_on__ic_esw_on__temp
del esw_on__rg_on_esw_on__temp
del esw_on__vcc_esw_on__temp
del f
del files
del fwd_r
del fwd_t
del ic__ic_err__temp
del ic__ic_esw_off__temp
del ic__ic_esw_on__temp
del ic_pair
del ic_temp__ic_vce
del if_temp__if_vf
del igbt_r
del igbt_t
del pair
del rg_on__rg_on_esw_on__temp
del rg_off__rg_off_esw_off__temp
del rg_on__rg_on_err__temp
del rth_val
del value
del vcc__vcc_esw_off__temp
del vcc__vcc_esw_on__temp
del vce_temp__ic_vce
del vf_temp__if_vf
del x

blab = copy.deepcopy(clean_files)

for value in blab:
    for value2 in blab[value]:
        if clean_files[value][value2]['Nameplate Voltage'] in clean_files[value].keys():
            clean_files_temp = clean_files[value][value2]['Nameplate Voltage']
            del clean_files[value][value2]['Nameplate Voltage']
            clean_files[value][clean_files_temp].update({value2: clean_files[value][value2]})
        else:
            clean_files_temp = clean_files[value][value2]['Nameplate Voltage']
            del clean_files[value][value2]['Nameplate Voltage']
            clean_files[value].update({clean_files_temp: {}})
            clean_files[value][clean_files_temp].update({value2: clean_files[value][value2]})
        del clean_files[value][value2]

blab = copy.deepcopy(clean_files)

for value in blab:
    for value2 in blab[value]:
        for value3 in blab[value][value2]:
            if clean_files[value][value2][value3]['Series'] in clean_files[value][value2].keys():
                clean_files_temp = clean_files[value][value2][value3]['Series']
                del clean_files[value][value2][value3]['Series']
                clean_files[value][value2][clean_files_temp].update({value3: clean_files[value][value2][value3]})
            else:
                clean_files_temp = clean_files[value][value2][value3]['Series']
                del clean_files[value][value2][value3]['Series']
                clean_files[value][value2].update({clean_files_temp: {}})
                clean_files[value][value2][clean_files_temp].update({value3: clean_files[value][value2][value3]})
            del clean_files[value][value2][value3]

# clean_files['HVIGBT']['6500'] = clean_files['HVIGBT']['3600']
# del clean_files['HVIGBT']['3600']


clean_files = json.dumps(clean_files)
with open('standard_modules.json', 'w') as f:
    f.write(clean_files)
    f.close()
