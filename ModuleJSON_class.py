import numpy as np
import pandas as pd

import format__output


class ModuleForJSON:
    def __init__(self, module_filename):
        self.module_dict = self.module_file_reader(module_filename)
        self.output_dict = {}

    def module_file_reader(self, module_file):
        module_string = module_file

        row_list = format__output.build__module_file_header()

        value_dict = {}

        for x in range(len(row_list)):
            value_dict[row_list[x]] = self.pull_data_from_column(module_string, row_list[x], None)
        for x in range(np.size(row_list)):
            if np.size(value_dict[row_list[x]]) == 1:
                value_dict[row_list[x]] = value_dict[row_list[x]][0]
        return value_dict

    def pull_data_from_column(self, module_file, column_string, indexcol):  # seems unnecessary
        df = pd.read_excel(module_file, index_col=indexcol)
        x = df[column_string].values
        x = x[~pd.isnull(x)]
        return x

    def get_JSON_ready_dict(self):
        ic__ic_esw_on = self.module_dict["IC - IC ESWON"]
        esw_on__ic_esw_on = self.module_dict["ESWON - IC ESWON"]
        ic__ic_esw_off = self.module_dict["IC - IC ESWOFF"]
        esw_off__ic_esw_off = self.module_dict["ESWOFF - IC ESWOFF"]
        rg_on__esw_on_rg_on = self.module_dict["RGON - ESWON RGON"]
        esw_on__esw_on_rg_on = self.module_dict["ESWON - ESWON RGON"]
        rg_off__esw_off_rg_off = self.module_dict["RGOFF - ESWOFF RGOFF"]
        esw_off__esw_off_rg_off = self.module_dict["ESWOFF - ESWOFF RGOFF"]
        ic__ic_err = self.module_dict["IC - IC ERR"]
        err__ic_err = self.module_dict["ERR - IC ERR"]
        rg_on__err_rg_on = self.module_dict["RGON - ERR RGON"]
        err__err_rg_on = self.module_dict["ERR - ERR RGON"]
        nameplate_vcc = self.module_dict['Nameplate VCC']
        vcc_ratio = self.module_dict['vcc_ratio']
        module_name = self.module_dict['Module Name']
        ic__ic_vce = self.module_dict['IC - IC VCE']
        vce__ic_vce = self.module_dict['VCE - IC VCE']
        if__if_vf = self.module_dict['IF - IF VF']
        vf__if_vf = self.module_dict["VF - IF VF"]
        rth_dc__igbt = self.module_dict['IGBT RTH DC']
        rth_dc__fwd = self.module_dict['FWD RTH DC']
        rth_dc__module = self.module_dict['Module RTH DC']
        trans_r_values__igbt = self.module_dict["IGBT R Values"]
        trans_t_values__igbt = self.module_dict["IGBT T Values"]
        trans_r_values__fwd = self.module_dict["FWD R Values"]
        trans_t_values__fwd = self.module_dict["FWD T Values"]
        self.output_dict.update({module_name: {}})
        self.output_dict[module_name].update(
            {
                "Name": module_name,
                "Module RTH DC": rth_dc__module,
                "FWD RTH DC": rth_dc__fwd,
                "IGBT RTH DC": rth_dc__igbt,
                "IGBT R Values": trans_r_values__igbt,
                "IGBT T Values": trans_t_values__igbt,
                "FWD R Values": trans_r_values__fwd,
                "FWD T Values": trans_t_values__fwd
            })
        self.output_dict[module_name].update({
            "ic_vce": {
                "ic__ic_vce": ic__ic_vce,
                "vce__ic_vce": vce__ic_vce
            },
            "if_vf": {
                "if__if_vf": if__if_vf,
                "vf__if_vf": vf__if_vf
            },
            "ic_esw_on": {
                "ic__ic_esw_on": ic__ic_esw_on,
                "esw_on__ic_esw_on": esw_on__ic_esw_on
            },
            "ic_esw_off": {
                "ic__ic_esw_off": ic__ic_esw_off,
                "esw_off__ic_esw_off": esw_off__ic_esw_off
            },
            "ic_err": {
                "ic__ic_err": ic__ic_err,
                "err__ic_err": err__ic_err
            },
            "rg_on_esw_on": {
                "rg_on__rg_on_esw_on": rg_on__esw_on_rg_on,
                "esw_on__rg_on_esw_on": esw_on__esw_on_rg_on
            },
            "rg_off_esw_off": {
                "rg_off__rg_off_esw_off": rg_off__esw_off_rg_off,
                "esw_off__rg_off_esw_off": esw_off__esw_off_rg_off
            },
            "rg_on_err": {
                "rg_on__rg_on_err": rg_on__err_rg_on,
                "err__rg_on_err": err__err_rg_on
            }
        })
        return self.output_dict
