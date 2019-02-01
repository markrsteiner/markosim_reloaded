import math
import time

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

import calculate__three_level
import calculate__two_level
import format__output


class InputOperation:
    def __init__(self, module_file_dict, rg_suppress_flag, modulation_type, three_level_flag=False, tj_hold_flag=False, module_max_temp=None, nerd_output_flag=False, step_size = 1):
        self.index__user_input = -1
        self.index__module = 0
        self.module_file_dict = module_file_dict
        self.rg_suppress_flag = rg_suppress_flag
        self.nerd_output_flag = nerd_output_flag
        self.step_size = step_size
        self.user_inputs = []
        self.user_input_length = 0
        self.modulation_type = modulation_type
        self.module_max_temp = module_max_temp
        self.tj_hold_flag = tj_hold_flag
        self.three_level_flag = three_level_flag
        self.module_filename_list = []
        self.inner_module_filename_list = []
        self.outer_module_filename_list = []
        self.diode_module_filename_list = []
        self.simulation_keys = []
        self.simulation_values = []
        self.current_user_input = None
        self.current_module_file = None
        self.current_module_files_three_level = None
        self.module_list_length = 0
        self.total_sim_length = 0
        self.final_simulation_output = None
        self.output_file_location = ""
        self.module_file_changed = True
        self.nerd_output_module = {}
        self.nerd_output_inner_module = {}  # for three level, need the others, too

    def reset_all(self):
        self.index__user_input = 0
        self.index__module = 0
        self.rg_suppress_flag = False
        self.nerd_output_flag = False

    def get__step_size(self):
        return self.step_size

    def get__total_simulation_length(self):
        self.total_sim_length = self.module_list_length * self.user_input_length
        return self.total_sim_length

    def get__modulation_type(self):
        return self.modulation_type

    def get__tj_hold_flag(self):
        return self.tj_hold_flag

    def get__module_max_temp(self):
        return self.module_max_temp

    def get__input_rg_flag(self):
        return self.rg_suppress_flag

    def load_user_inputs(self, user_inputs_filename):
        self.user_inputs = self.input_file_reader(user_inputs_filename)
        self.user_input_length = len(self.user_inputs['Vcc [V]'])

    def load__module_filename_list(self, input__inner_module_filename_list, input__outer_module_filename_list=None, input__diode_module_filename_list=None):
        if self.three_level_flag:
            self.inner_module_filename_list = input__inner_module_filename_list
            self.outer_module_filename_list = input__outer_module_filename_list
            self.diode_module_filename_list = input__diode_module_filename_list
            self.module_list_length = min(len(self.inner_module_filename_list), len(self.outer_module_filename_list), len(self.diode_module_filename_list))
        else:
            self.module_filename_list = input__inner_module_filename_list
            self.module_list_length = len(self.module_filename_list)
        return self.module_list_length

    def get_next_user_input(self):
        output = {}
        for key in self.user_inputs.keys():
            if type(self.user_inputs[key]) is np.ndarray:
                output.update({key: self.user_inputs[key][self.index__user_input]})
            else:
                output.update({key: self.user_inputs[key]})
        output.update({'rg_suppress_flag': self.rg_suppress_flag, 'nerd_output_flag': self.nerd_output_flag})
        return output

    def get_next_module_file(self):
        if self.three_level_flag:
            if self.module_file_changed:
                inner_module_list = self.module_file_reader(self.inner_module_filename_list[self.index__module])
                inner_module_list = self.file_value_checker(inner_module_list)
                outer_module_list = self.module_file_reader(self.outer_module_filename_list[self.index__module])
                outer_module_list = self.file_value_checker(outer_module_list)
                diode_module_list = self.module_file_reader(self.diode_module_filename_list[self.index__module])
                diode_module_list = self.file_value_checker(diode_module_list)
                module_file_lists = {'inside_module': inner_module_list, 'outside_module': outer_module_list, 'diode_module': diode_module_list}
                self.module_file_changed = False
            else:
                module_file_lists = self.current_module_files_three_level
            return module_file_lists
        else:
            if self.module_file_changed:
                module_file_list = self.module_file_reader(self.module_filename_list[self.index__module])
                module_file_list = self.file_value_checker(module_file_list)
                self.module_file_changed = False
            else:
                module_file_list = self.current_module_file
            return module_file_list

    def module_file_reader(self, module_file):
        row_list = format__output.build__module_file_header()
        find_gen = self.gen_dict_extract(module_file, self.module_file_dict)
        module = next(find_gen)

        # todo probably get rid of this soon
        value_dict = {
            "Module Name": module_file,
            "IC - IC VCE": module['ic_vce']['ic__ic_vce'],
            "VCE - IC VCE": module['ic_vce']['vce__ic_vce'],
            "IF - IF VF": module['if_vf']['if__if_vf'],
            "VF - IF VF": module['if_vf']['vf__if_vf'],
            "IC - IC ESWON": module['ic_esw_on']['ic__ic_esw_on'],
            "ESWON - IC ESWON": module['ic_esw_on']['esw_on__ic_esw_on'],
            "IC - IC ESWOFF": module['ic_esw_off']['ic__ic_esw_off'],
            "ESWOFF - IC ESWOFF": module['ic_esw_off']['esw_off__ic_esw_off'],
            "IC - IC ERR": module['ic_err']['ic__ic_err'],
            "ERR - IC ERR": module['ic_err']['err__ic_err'],
            "ESWON - ESWON RGON": module['rg_on_esw_on']['esw_on__rg_on_esw_on'],
            "RGON - ESWON RGON": module['rg_on_esw_on']['rg_on__rg_on_esw_on'],
            "ESWOFF - ESWOFF RGOFF": module['rg_off_esw_off']['esw_off__rg_off_esw_off'],
            "RGOFF - ESWOFF RGOFF": module['rg_off_esw_off']['rg_off__rg_off_esw_off'],
            "ERR - ERR RGON": module['rg_on_err']['err__rg_on_err'],
            "RGON - ERR RGON": module['rg_on_err']['rg_on__rg_on_err'],
            "IGBT R Values": module['IGBT R Values'],
            "IGBT T Values": module['IGBT T Values'],
            "FWD R Values": module['FWD R Values'],
            "FWD T Values": module['FWD T Values'],
            "IGBT RTH DC": module['IGBT RTH DC'],
            "FWD RTH DC": module['FWD RTH DC'],
            "vcc_ratio": module['vcc_value'],
            "Module RTH DC": module['Module RTH DC'],
            "Nameplate VCC": module['vcc_value'],
            "Nameplate Current": module['Nameplate Current']
        }

        for key in value_dict:
            if type(value_dict[key]) is list:
                for val in range(len(value_dict[key])):
                    value_dict[key][val] = float(value_dict[key][val])
            if key != 'Module Name':
                if type(value_dict[key]) is str:
                    value_dict[key] = float(value_dict[key])

        return value_dict

    # def build__module_file_header(self):
    #     return ["Module Name",
    #             "IC - IC VCE",
    #             "VCE - IC VCE",
    #             "IF - IF VF",
    #             "VF - IF VF",
    #             "IC - IC ESWON",
    #             "ESWON - IC ESWON",
    #             "IC - IC ESWOFF",
    #             "ESWOFF - IC ESWOFF",
    #             "IC - IC ERR",
    #             "ERR - IC ERR",
    #             "ESWON - ESWON RGON",
    #             "RGON - ESWON RGON",
    #             "ESWOFF - ESWOFF RGOFF",
    #             "RGOFF - ESWOFF RGOFF",
    #             "ERR - ERR RGON",
    #             "RGON - ERR RGON",
    #             "IGBT R Values",
    #             "IGBT T Values",
    #             "FWD R Values",
    #             "FWD T Values",
    #             "IGBT RTH DC",
    #             "FWD RTH DC",
    #             "Module RTH DC",
    #             "Nameplate VCC",
    #             "Nameplate Current"
    #             ]
    #
    #     # value_dict = {}
    #     #
    #     # for x in range(len(row_list)):
    #     #     value_dict[row_list[x]] = self.pull_data_from_column(module_string, row_list[x], None)
    #     # for x in range(np.size(row_list)):
    #     #     if np.size(value_dict[row_list[x]]) == 1:
    #     #         value_dict[row_list[x]] = value_dict[row_list[x]][0]
    #     return value_dict

    def pull_data_from_column(self, module_file, column_string, indexcol):  # seems unnecessary
        df = pd.read_excel(module_file, index_col=indexcol)
        x = df[column_string].values
        x = x[~pd.isnull(x)]
        return x

    def gen_dict_extract(self, key, var):
        if hasattr(var, 'items'):
            for k, v in var.items():
                if k == key:
                    yield v
                if isinstance(v, dict):
                    for result in self.gen_dict_extract(key, v):
                        yield result

    def input_file_reader(self, input_file):
        row_list = ['Vcc [V]',
                    'Io [Apk]',
                    'PF [cos(\u03D5)]',
                    'Mod. Depth',
                    'fc [kHz]',
                    'fo [Hz]',
                    'rg on [\u03A9]',
                    'rg off [\u03A9]',
                    'Ts [\u00B0C]'
                    ]
        value_dict = {}
        for x in range(len(row_list)):
            value_dict[row_list[x]] = self.pull_data_from_column(input_file, row_list[x], None)
        for x in range(len(row_list)):
            if len(value_dict[row_list[x]]) == 1:
                value_dict[row_list[x]] = value_dict[row_list[x]][0]
        return value_dict

    def file_value_checker(self, file_values):
        threshold = 10
        current_value = file_values["Nameplate Current"]

        file_values["IC - IC VCE"], file_values["VCE - IC VCE"] = self.array_flipper(file_values["IC - IC VCE"], file_values["VCE - IC VCE"])
        file_values["IF - IF VF"], file_values["VF - IF VF"] = self.array_flipper(file_values["IF - IF VF"], file_values["VF - IF VF"])
        file_values["IC - IC ESWON"], file_values["ESWON - IC ESWON"] = self.array_flipper(file_values["IC - IC ESWON"], file_values["ESWON - IC ESWON"])
        file_values["IC - IC ESWOFF"], file_values["ESWOFF - IC ESWOFF"] = self.array_flipper(file_values["IC - IC ESWOFF"], file_values["ESWOFF - IC ESWOFF"])
        file_values["IC - IC ERR"], file_values["ERR - IC ERR"] = self.array_flipper(file_values["IC - IC ERR"], file_values["ERR - IC ERR"])
        file_values["RGON - ESWON RGON"], file_values["ESWON - ESWON RGON"] = self.array_flipper(file_values["RGON - ESWON RGON"], file_values["ESWON - ESWON RGON"])
        file_values["RGOFF - ESWOFF RGOFF"], file_values["ESWOFF - ESWOFF RGOFF"] = self.array_flipper(file_values["RGOFF - ESWOFF RGOFF"], file_values["ESWOFF - ESWOFF RGOFF"])
        file_values["RGON - ERR RGON"], file_values["ERR - ERR RGON"] = self.array_flipper(file_values["RGON - ERR RGON"], file_values["ERR - ERR RGON"])

        file_values["ESWON - ESWON RGON"] = self.check__rg_esw(file_values["ESWON - ESWON RGON"], file_values["ESWON - IC ESWON"], file_values["IC - IC ESWON"], current_value, threshold)
        file_values["ESWOFF - ESWOFF RGOFF"] = self.check__rg_esw(file_values["ESWOFF - ESWOFF RGOFF"], file_values["ESWOFF - IC ESWOFF"], file_values["IC - IC ESWOFF"], current_value, threshold)
        file_values["ERR - ERR RGON"] = self.check__rg_esw(file_values["ERR - ERR RGON"], file_values["ERR - IC ERR"], file_values["IC - IC ERR"], current_value, threshold)

        return file_values

    def strictly_increasing(self, values): #todo seems unecessary
        return all(x < y for x, y in zip(values, values[1:]))

    def array_flipper(self, dependent_array, independent_array): #todo seems unecessasary
        if not self.strictly_increasing(dependent_array):
            dependent_array = np.flipud(dependent_array)
            independent_array = np.flipud(independent_array)
        return [dependent_array, independent_array]

    def check__rg_esw(self, e_sw_rg, e_sw_ic, ic_e_sw, current_value, threshold):
        if e_sw_rg[0] > threshold:
            e_sw_rg = self.esw_rg_fixer(e_sw_ic, ic_e_sw, e_sw_rg, current_value)
        return e_sw_rg

    def esw_rg_fixer(self, esw_ic_esw, ic_ic_esw, esw_rg_esw, ic): #todo fold into function above?
        baseline = interp1d(ic_ic_esw, esw_ic_esw, fill_value='extrapolate')
        baseline_energy = float(baseline(ic))
        for x in range(0, len(esw_rg_esw)):
            esw_rg_esw[x] = esw_rg_esw[x] / float(baseline_energy)
        return esw_rg_esw

    def get__present_simulation_files_two_level(self): #todo seems unecessary
        if self.three_level_flag:
            return self.current_module_files_three_level, self.current_user_input
        else:
            return self.current_module_file, self.current_user_input

    def set__next_simulation_file_set(self): #todo seems dangerous
        if self.index__user_input < self.user_input_length - 1:
            self.index__user_input += 1
        else:
            if self.index__module < self.module_list_length - 1:
                self.index__module += 1
                self.index__user_input = 0
                self.module_file_changed = True
            else:
                return False
        self.current_user_input = self.get_next_user_input()
        if self.three_level_flag:
            self.current_module_files_three_level = self.get_next_module_file()
        else:
            self.current_module_file = self.get_next_module_file()
        return True

    def run__straight_simulation(self, progress_bar):  #todo messy, clean up
        if self.user_input_length > 1:
            progress_bar.setValue(1 / self.get__total_simulation_length() * 100)
            while self.set__next_simulation_file_set():
                prog_val = np.clip(progress_bar.value() + 1.0 / (self.get__total_simulation_length()) * 100, 0, 100)
                progress_bar.setValue(prog_val)
                if self.three_level_flag:
                    single_simulation_results = calculate__three_level.calculate_3_level(self)
                else:
                    single_simulation_results = calculate__two_level.simulation__two_level(self)

                single_simulation_results_fixed_precision_values = [math.floor(y * 100) / 100 if type(y) is not str else y for y in single_simulation_results.values()]  # limits output values to 2 decimal places
                self.simulation_values.append(single_simulation_results_fixed_precision_values)
            self.simulation_keys = [y for y in single_simulation_results.keys()]
            self.simulation_values = np.transpose(self.simulation_values)
            dict_where_keys_and_values_are_attached = {self.simulation_keys[x]: self.simulation_values[x] for x in range(len(self.simulation_keys))}
            self.final_simulation_output = {**dict_where_keys_and_values_are_attached}
        else:
            progress_bar.setValue(100)
            single_simulation_results = calculate__two_level.simulation__two_level(self)
            single_simulation_results_fixed_precision_values = [math.floor(y * 100) / 100 if type(y) is not str else y for y in single_simulation_results.values()]  # limits output values to 2 decimal places
            self.simulation_values = np.transpose(self.simulation_values)
            dict_where_keys_and_values_are_attached = {self.simulation_keys[x]: self.simulation_values[x] for x in range(len(self.simulation_keys))}
            self.final_simulation_output = {**dict_where_keys_and_values_are_attached}
            self.final_simulation_output = single_simulation_results_fixed_precision_values

    def set_output_file_location(self, input__output_file_location):
        self.output_file_location = input__output_file_location

    def save__output_file(self):  # todo can this be cleaned?
        columns = format__output.build__output_file_header(self.three_level_flag)
        output_file_name = self.output_file_location + '/output' + time.strftime("__%b_%d__%H_%M_%S") + '.xlsx'
        df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in self.final_simulation_output.items()]), columns=columns).T
        df.reset_index(level=0, inplace=True)
        xl_writer = pd.ExcelWriter(output_file_name, engine='xlsxwriter', options={'strings_to_numbers': True})
        workbook = xl_writer.book
        df.to_excel(xl_writer, index=False, header=False)
        worksheet = xl_writer.sheets['Sheet1']
        # worksheet, workbook = format__output.output_worksheet_formatter(df, workbook, worksheet)
        xl_writer.save()
        self.reset_all()

        if self.nerd_output_flag:
            nerd_file_name = self.output_file_location + '/nerd_output' + time.strftime("__%b_%d__%H_%M_%S") + '.xlsx'
            df_nerd = pd.DataFrame({
                "Current IGBT": self.nerd_output_module.current__igbt,
                "Current FWD": self.nerd_output_module.current__fwd,
                "Conduction Loss IGBT": self.nerd_output_module.conduction_loss__igbt,
                "ESW On Loss IGBT": self.nerd_output_module.esw_on_loss,
                "ESW Off Loss IGBT": self.nerd_output_module.esw_off_loss,
                "ESW Loss IGBT": self.nerd_output_module.esw_loss__igbt,
                "Energy IGBT": self.nerd_output_module.energy__igbt,
                "Inst power IGBT": self.nerd_output_module.instantaneous_power__igbt,
                "Tj list IGBT": self.nerd_output_module.tj_max_igbt_list[-120:],
                "Conduction Loss FWD": self.nerd_output_module.conduction_loss__fwd,
                "Err Loss FWD": self.nerd_output_module.err_loss,
                "Energy FWD": self.nerd_output_module.energy__fwd,
                "Inst Power FWD": self.nerd_output_module.instantaneous_power__fwd,
                "Tj list FWD": self.nerd_output_module.tj_max_fwd_list[-120:]
            })
            df_nerd.reset_index(level=0, inplace=True)
            xl_writer = pd.ExcelWriter(nerd_file_name, engine='xlsxwriter', options={'strings_to_numbers': True})
            workbook = xl_writer.book
            df_nerd.to_excel(xl_writer)
            xl_writer.save()

    def get__three_level_flag(self):
        return self.three_level_flag