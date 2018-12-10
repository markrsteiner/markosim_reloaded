import math

import numpy as np
from scipy.interpolate import interp1d


class Module:
    def __init__(self, module_file):
        self.module = {}
        self.igbt = {}
        self.fwd = {}
        self.sim_info = {}

        self.fill__module_info(module_file)

    def fill__module_info(self, module_file):
        temp_ic, temp_vce = self.get__corrected_vce(module_file['IC - IC VCE'], module_file['VCE - IC VCE'])
        temp_if, temp_vf = self.get__corrected_vce(module_file['IF - IF VF'], module_file['VF - IF VF'])

        self.igbt.update({
            'info': {},
            'loss_totals': {},
            'temps': {}
        })
        self.fwd.update({
            'info': {},
            'loss_totals': {},
            'temps': {}
        })

        if module_file['vcc_ratio'] > 0:
            vcc_ratio = module_file['vcc_ratio']
        else:
            vcc_ratio = 0

        self.igbt['info'].update({
            'conduction': interp1d(temp_ic, temp_vce, fill_value='extrapolate'),
            'ic_esw_on': interp1d(self.get__corrected_esw(module_file['IC - IC ESWON']), self.get__corrected_esw(module_file['ESWON - IC ESWON']), fill_value='extrapolate'),
            'ic_esw_off': interp1d(self.get__corrected_esw(module_file['IC - IC ESWOFF']), self.get__corrected_esw(module_file['ESWOFF - IC ESWOFF']), fill_value='extrapolate'),
            'rg_on_esw_on': interp1d(module_file['RGON - ESWON RGON'], module_file['ESWON - ESWON RGON'], fill_value='extrapolate'),
            'rg_off_esw_off': interp1d(module_file['RGOFF - ESWOFF RGOFF'], module_file['ESWOFF - ESWOFF RGOFF'], fill_value='extrapolate'),
            'rth': module_file['IGBT RTH DC'],
            'trans_r': np.array(module_file['IGBT R Values']),
            'trans_t': np.array(module_file['IGBT T Values'])
        })

        self.fwd['info'].update({
            'ic_err': interp1d(self.get__corrected_esw(module_file['IC - IC ERR']), self.get__corrected_esw(module_file['ERR - IC ERR']), fill_value='extrapolate'),
            'conduction': interp1d(temp_if, temp_vf, fill_value='extrapolate'),
            'rg_on_err': interp1d(module_file['RGON - ERR RGON'], module_file['ERR - ERR RGON'], fill_value='extrapolate'),
            'rth': module_file['FWD RTH DC'],
            'trans_r': np.array(module_file['FWD R Values']),
            'trans_t': np.array(module_file['FWD T Values'])
        })

        self.module.update({
            'loss_totals': {},
            'temps': {},
            'tj_max': {},
            'vcc_ratio': vcc_ratio,
            'nameplate_vcc': module_file['Nameplate VCC'],
            'name': self.get__module_name(module_file),
            'rth': module_file['Module RTH DC'],
            'thermal_interp_is_four_degree': self.check__thermal_interp()
        })

    def check__thermal_interp(self):  # todo could this be cleaned?
        if self.igbt['info']['trans_t'][2] == 0.0:
            temp_trans_t = np.append(self.igbt['info']['trans_r'][1] / self.igbt['info']['trans_r'][2], self.igbt['info']['trans_t'][0] / self.igbt['info']['trans_t'][1])
            temp_trans_r = np.append(self.igbt['info']['trans_r'][0], self.igbt['info']['trans_r'][3])
            temp_fwd_t = np.append(self.fwd['info']['trans_r'][1] / self.fwd['info']['trans_r'][2], self.fwd['info']['trans_t'][0] / self.fwd['info']['trans_t'][1])
            temp_fwd_r = np.append(self.fwd['info']['trans_r'][0], self.fwd['info']['trans_r'][3])
            self.igbt['info']['trans_r'] = temp_trans_r
            self.igbt['info']['trans_t'] = temp_trans_t
            self.fwd['info']['trans_r'] = temp_fwd_r
            self.fwd['info']['trans_t'] = temp_fwd_t
            module_interp_is_four_deg = False
        else:
            module_interp_is_four_deg = True

        return module_interp_is_four_deg

    def get__max_current(self):
        return max(self.fwd['temps']['max_nom'], self.igbt['temps']['max_nom'])

    def set__vcc_ratio_and_get_values(self, is_three_level, system):  # todo call this something different, and break it out for 3-level
        vcc_ratio = self.module['vcc_ratio']
        if vcc_ratio == 0:
            if is_three_level:
                if self.module['nameplate_vcc'] == 6500:
                    vcc_ratio = system.get__input_bus_voltage() / 3600
                else:
                    vcc_ratio = system.get__input_bus_voltage() / 2.0 / self.get__vcc_value(self.module['nameplate_vcc'])  # fix this at some point, it's not exactly accurate
            else:
                vcc_ratio = system.get__input_bus_voltage() / self.get__vcc_value(self.module['nameplate_vcc'])  # fix this at some point, it's not exactly accurate
        else:
            vcc_ratio = system.get__input_bus_voltage() / vcc_ratio

        self.sim_info.update({
            'switching_scalar': system.get__switches_per_degree() * vcc_ratio * system.get__input_output_freq(),
            'input_output_freq': system.get__input_output_freq(),
            'time_division': system.get__time_division(),
            'input_t_sink': system.get__input_t_sink(),
            'step_size': system.step_size,
            'step_range': int(360 / system.step_size),
            'sec_per_cycle_degree': 1.0 / system.get__input_output_freq() / 360.0 * system.step_size,
            'duty_p': system.get__duty_cycle__p()
        })
        del self.module['vcc_ratio']

    def set__rg(self, input_instance, system_instance, module_location=None):  # todo set up getter setters
        if not input_instance.rg_suppress_flag:
            system_instance.rg_output_flag = True
            if module_location is None:
                rg_on = system_instance.input_rg_on
                rg_off = system_instance.input_rg_off
            elif module_location is 'inside':
                rg_on = system_instance.input_rg_on_inside
                rg_off = system_instance.input_rg_off_inside
            elif module_location is 'outside':
                rg_on = system_instance.input_rg_on_outside
                rg_off = system_instance.input_rg_off_outside
                self.fwd['info']['err_rg_scalar'] = self.fwd['info']['rg_on_err'](system_instance.input_rg_on_outside)
            else:
                self.igbt['info']['esw_on_rg_scalar'] = self.sim_info['switching_scalar']
                self.igbt['info']['esw_off_rg_scalar'] = self.sim_info['switching_scalar']
                self.fwd['info']['err_rg_scalar'] = self.sim_info['switching_scalar']
                return
            self.igbt['info']['esw_on_rg_scalar'] = self.igbt['info']['rg_on_esw_on'](rg_on) * self.sim_info['switching_scalar']
            self.igbt['info']['esw_off_rg_scalar'] = self.igbt['info']['rg_off_esw_off'](rg_off) * self.sim_info['switching_scalar']
            self.fwd['info']['err_rg_scalar'] = self.fwd['info']['rg_on_err'](rg_on) * self.sim_info['switching_scalar']
        else:
            system_instance.rg_output_flag = False
            self.igbt['info']['esw_on_rg_scalar'] = self.sim_info['switching_scalar']
            self.igbt['info']['esw_off_rg_scalar'] = self.sim_info['switching_scalar']
            self.fwd['info']['err_rg_scalar'] = self.sim_info['switching_scalar']

    def set__current_igbt(self, current):
        self.igbt['current'] = current

    def set__current_fwd(self, current):
        self.fwd['current'] = current

    def calculate__conduction_loss__igbt(self, duty):
        self.igbt = self.calculate__conduction_loss(self.igbt, duty)

    def calculate__conduction_loss__fwd(self, duty):
        self.fwd = self.calculate__conduction_loss(self.fwd, duty)

    def calculate__conduction_loss(self, part_dict, duty):
        part_dict['conduction_loss'] = [curr * duty_v * part_dict['info']['conduction'](curr) * self.sim_info.get('step_size') / 360.0 if curr > 0.0 else 0.0 for curr, duty_v in zip(part_dict.get('current'), duty)]
        part_dict['loss_totals']['conduction'] = np.sum(part_dict['conduction_loss'])
        return part_dict

    def calculate__switching_loss__igbt(self, duty=None):
        if duty is None:
            duty = self.sim_info['duty_p']

        self.igbt['esw_on_loss'] = [self.igbt['info'].get('ic_esw_on')(curr) * self.igbt['info']['esw_on_rg_scalar'] if curr > 0.0 and 0.0 < duty < 1.0 else 0.0 for curr, duty in zip(self.igbt['current'], duty)]
        self.igbt['loss_totals']['esw_on'] = np.sum(self.igbt['esw_on_loss'])

        self.igbt['esw_off_loss'] = [self.igbt['info']['ic_esw_off'](curr) * self.igbt['info']['esw_off_rg_scalar'] if curr > 0.0 and 0.0 < duty < 1.0 else 0.0 for curr, duty in zip(self.igbt['current'], duty)]
        self.igbt['loss_totals']['esw_off'] = np.sum(self.igbt['esw_off_loss'])

        self.igbt['esw_loss'] = np.add(self.igbt['esw_on_loss'], self.igbt['esw_off_loss'])
        self.igbt['loss_totals']['esw'] = np.sum(self.igbt['esw_loss'])

    def calculate__switching_loss__fwd(self, duty=None):
        if duty is None:
            duty = self.sim_info['duty_p']

        self.fwd['err_loss'] = [self.fwd['info']['ic_err'](curr) * self.fwd['info']['err_rg_scalar'] if curr > 0.0 and 0.0 < duty < 1.0 else 0.0 for curr, duty in zip(self.fwd['current'], duty)]
        self.fwd['loss_totals']['err'] = np.sum(self.fwd['err_loss'])

    def calculate__power_and_temps(self):
        self.igbt['energy'] = np.add(self.igbt['conduction_loss'], self.igbt['esw_loss'])
        self.igbt['power_inst'] = [energy / self.sim_info['input_output_freq'] / self.sim_info['time_division'] for energy in self.igbt['energy']]
        self.igbt['loss_totals']['device'] = self.igbt['loss_totals']['conduction'] + self.igbt['loss_totals']['esw']

        self.fwd['energy'] = np.add(self.fwd['conduction_loss'], self.fwd['err_loss'])
        self.fwd['power_inst'] = [energy / self.sim_info['input_output_freq'] / self.sim_info['time_division'] for energy in self.fwd['energy']]
        self.fwd['loss_totals']['device'] = self.fwd['loss_totals']['conduction'] + self.fwd['loss_totals']['err']

        self.module['loss_totals']['module'] = self.igbt['loss_totals']['device'] + self.fwd['loss_totals']['device']

        self.module['temps']['t_case'] = self.module['loss_totals']['module'] * self.module['rth']

        self.igbt['temps']['ave_delta'] = self.igbt['loss_totals']['device'] * self.igbt['info']['rth']
        self.igbt['temps']['ave_nom'] = self.sim_info['input_t_sink'] + self.igbt['temps']['ave_delta'] + self.module['temps']['t_case']

        self.fwd['temps']['ave_delta'] = self.fwd['loss_totals']['device'] * self.fwd['info']['rth']
        self.fwd['temps']['ave_nom'] = self.sim_info['input_t_sink'] + self.fwd['temps']['ave_delta'] + self.module['temps']['t_case']
        self.calculate__max_temp()

    def calculate__max_temp(self):  # maybe split into igbt and fwd separately?
        self.create_thermal_resistance_dict()
        tj_igbt_list = []
        tj_fwd_list = []

        delta_p_igbt = np.subtract(np.roll(self.igbt['power_inst'], -1), self.igbt['power_inst'])[:359]

        last_power_igbt = self.igbt['power_inst'][-1] - self.igbt['loss_totals']['device']
        first_power_igbt = self.igbt['power_inst'][0] - self.igbt['loss_totals']['device']

        rth_time = np.arange(self.sim_info['step_range']) * self.sim_info['sec_per_cycle_degree'] + self.module['tj_max']['time_value']
        rth_dict_igbt_added = np.add(self.calculate__rth_from_time(self.igbt, rth_time), self.igbt['info']['rth_dict'])

        tj_igbt_inst_init = rth_dict_igbt_added * first_power_igbt - last_power_igbt * self.igbt['info']['rth_dict'] + self.sim_info['input_t_sink'] + self.igbt['temps']['ave_delta'] + self.module['temps']['t_case']

        delta_p_fwd = np.subtract(np.roll(self.fwd['power_inst'], -1), self.fwd['power_inst'])[:359]
        last_power_fwd = self.fwd['power_inst'][-1] - self.fwd['loss_totals']['device']
        first_power_fwd = self.fwd['power_inst'][0] - self.fwd['loss_totals']['device']

        rth_dict_fwd_added = np.add(self.calculate__rth_from_time(self.fwd, rth_time), self.fwd['info']['rth_dict'])

        tj_fwd_inst_init = self.sim_info['input_t_sink'] + self.fwd['temps']['ave_delta'] + self.module['temps']['t_case'] - last_power_fwd * self.fwd['info']['rth_dict'] + first_power_fwd * rth_dict_fwd_added

        rth_dict_igbt__added_chunk = np.tile(rth_dict_igbt_added, (359, 1)).T  # todo need to get last 359 of array, not 1st value
        rth_dict_igbt__added_chunk[np.tril_indices(359, -1)] = 0
        rth_dict_igbt__added_chunk[359] = 0.0
        rth_dict_igbt__added_chunk.sort(axis=0)
        rth_dict_igbt__added_chunk = np.flipud(np.delete(rth_dict_igbt__added_chunk, 359, axis=0))

        rth_dict_igbt__old_chunk = np.tile(self.igbt['info']['rth_dict'], (359, 1)).T
        rth_dict_igbt__old_chunk[np.triu_indices(359)] = 0
        rth_dict_igbt__old_chunk.sort(axis=0)
        rth_dict_igbt__old_chunk = np.flipud(rth_dict_igbt__old_chunk)

        for i in range(self.sim_info['step_range'] - 1):
            rth_dict_igbt__old_chunk[:, i] = np.roll(rth_dict_igbt__old_chunk[:, i], i)

        rth_dict_igbt__old_chunk = np.delete(rth_dict_igbt__old_chunk, 359, axis=0)
        rth_dict_igbt_full = np.add(rth_dict_igbt__old_chunk, rth_dict_igbt__added_chunk)

        rth_dict_fwd__added_chunk = np.tile(rth_dict_fwd_added, (359, 1)).T  # todo need to get last 359 of array, not 1st value
        rth_dict_fwd__added_chunk[np.tril_indices(359, -1)] = 0
        rth_dict_fwd__added_chunk[359] = 0.0
        rth_dict_fwd__added_chunk.sort(axis=0)
        rth_dict_fwd__added_chunk = np.flipud(np.delete(rth_dict_fwd__added_chunk, 359, axis=0))

        rth_dict_fwd__old_chunk = np.tile(self.fwd['info']['rth_dict'], (359, 1)).T
        rth_dict_fwd__old_chunk[np.triu_indices(359)] = 0
        rth_dict_fwd__old_chunk.sort(axis=0)
        rth_dict_fwd__old_chunk = np.flipud(rth_dict_fwd__old_chunk)

        for i in range(self.sim_info['step_range'] - 1):
            rth_dict_fwd__old_chunk[:, i] = np.roll(rth_dict_fwd__old_chunk[:, i], i)

        rth_dict_fwd__old_chunk = np.delete(rth_dict_fwd__old_chunk, 359, axis=0)
        rth_dict_fwd_full = np.add(rth_dict_fwd__old_chunk, rth_dict_fwd__added_chunk)

        delta_p_tile__igbt = np.tile(delta_p_igbt, (359, 1)).T
        temp_delta__igbt = rth_dict_igbt_full * delta_p_tile__igbt
        tj_list__igbt = np.sum(temp_delta__igbt, axis=0)

        delta_p_tile__fwd = np.tile(delta_p_fwd, (359, 1)).T
        temp_delta__fwd = rth_dict_fwd_full * delta_p_tile__fwd
        tj_list__fwd = np.sum(temp_delta__fwd, axis=0)

        # for index in range(self.sim_info['step_range']):
        #     rth_dict_igbt_fix = [rth_dict_igbt_added[i] if i <= index else self.igbt['info']['rth_dict'][i] for i in range(self.sim_info['step_range'])]
        #     rth_dict_igbt_fix.reverse()
        #     rth_temp = np.roll(rth_dict_igbt_fix, index)[:359]
        #
        #     pre_temp = np.multiply(delta_p_igbt, rth_temp)
        #
        #     temp_add_vals_igbt = np.sum(pre_temp)
        #     tj_igbt_list.append(temp_add_vals_igbt)
        #
        #     rth_dict_fwd_fix = [rth_dict_fwd_added[i] if i <= index else self.fwd['info']['rth_dict'][i] for i in range(self.sim_info['step_range'])]
        #     rth_dict_fwd_fix.reverse()
        #
        #     temp_add_vals_fwd = np.sum(np.multiply(delta_p_fwd, np.roll(rth_dict_fwd_fix, index)[:359]))
        #     tj_fwd_list.append(temp_add_vals_fwd)

        tj_igbt_list = np.add(tj_igbt_inst_init, tj_igbt_list)
        tj_ave_igbt = self.igbt['temps']['ave_nom'] - np.average(tj_igbt_list)
        tj_igbt_list = np.add(tj_ave_igbt, tj_igbt_list)

        tj_fwd_list = np.add(tj_fwd_inst_init, tj_fwd_list)
        tj_ave_fwd = self.fwd['temps']['ave_nom'] - np.average(tj_fwd_list)
        tj_fwd_list = np.add(tj_fwd_list, tj_ave_fwd)

        self.module['tj_max']['time_list'] = [i * self.sim_info['sec_per_cycle_degree'] + self.module['tj_max']['time_value'] for i in range(self.sim_info['step_range'])]
        self.module['tj_max']['rad_list'] = [i * self.sim_info['step_size'] for i in range(self.sim_info['step_range'])]

        self.igbt['temps']['max_nom'] = max(tj_igbt_list)
        self.fwd['temps']['max_nom'] = max(tj_fwd_list)
        self.igbt['temps']['max_delta'] = max(tj_igbt_list) - self.sim_info['input_t_sink'] - self.module['temps']['t_case']
        self.fwd['temps']['max_delta'] = max(tj_fwd_list) - self.sim_info['input_t_sink'] - self.module['temps']['t_case']
        self.igbt['temps']['max_list'] = tj_igbt_list
        self.fwd['temps']['max_list'] = tj_fwd_list

    def advindexing_roll(self, A, r):
        rows, column_indices = np.ogrid[:A.shape[0], :A.shape[1]]
        r[r < 0] += A.shape[1]
        column_indices = column_indices - r[:, np.newaxis]
        return A[rows, column_indices]

    def calculate__rth_from_time(self, part_dict, time):
        if type(time) is np.ndarray:
            scalar = np.tile(part_dict['info']['trans_r'].T, (self.sim_info['step_range'], 1))
            growth = np.tile(part_dict['info']['trans_t'].T, (self.sim_info['step_range'], 1))
        else:
            scalar = part_dict['info']['trans_r']
            growth = part_dict['info']['trans_t']

        if self.module['thermal_interp_is_four_degree']:
            if type(time) is np.ndarray:
                time = np.tile(time, (4, 1)).T
                num = np.sum(np.multiply(scalar, np.subtract(1.0, np.exp(np.divide(-1.0 * time, growth)))), axis=1)
            else:
                num = np.sum(np.multiply(scalar, np.subtract(1.0, np.exp(-np.float_power(time, growth)))))

        else:
            if type(time) is np.ndarray:
                time = np.tile(time, (2, 1)).T
                num = np.sum(np.multiply(scalar, np.subtract(1.0, np.exp(-np.float_power(time, growth)))), axis=1)
            else:
                num = np.sum(np.multiply(scalar, np.subtract(1.0, np.exp(-np.float_power(time, growth)))))

        return num * part_dict['info']['rth']

    def calculate__rth_integration(self, part_dict, init__degree):  # todo could this be folded into rth_integral_four_copy
        init__degree = math.floor(init__degree / 360)
        index = np.arange(360)
        num = np.sum(self.rth_integral_four_copy(index, part_dict['info']['trans_r'], part_dict['info']['trans_t'], init__degree), axis=0)
        return num * self.igbt['info']['rth']

    def rth_integral_four_copy(self, degree_index, scalar, growth, start_degree):
        step_size = self.sim_info['step_size']
        switch_count = self.sim_info['sec_per_cycle_degree']
        degree_index = np.tile(degree_index, (4, 1))
        scalar = np.tile(scalar, (360, 1)).transpose()
        growth = np.tile(growth, (360, 1)).transpose()
        denom = np.subtract(np.exp(np.divide(-360 / step_size * switch_count, growth)), 1)
        num1 = np.negative(np.exp(np.divide(np.multiply(-switch_count * 0.5, np.add(720 / step_size * start_degree + 720 / step_size + 1, np.multiply(2, degree_index))), growth)))
        num3 = np.subtract(np.multiply(start_degree, np.exp(np.divide(-360 / step_size * switch_count, growth))), start_degree)
        num4 = np.exp(np.divide(np.multiply(-switch_count * 0.5, (np.add(1, np.multiply(2, degree_index)))), growth))
        num6 = np.subtract(np.exp(np.divide(-360 / step_size * switch_count, growth)), 1)
        numerator = np.multiply(scalar, np.add(np.add(num1, num3), np.add(num4, num6)))
        out = np.divide(numerator, denom)
        return out

    def create_thermal_resistance_dict(self):
        igbt_dc_rth = self.calculate__rth_from_time(self.igbt, 10.0)
        fwd_dc_rth = self.calculate__rth_from_time(self.fwd, 10.0)
        time_value = self.sim_info['sec_per_cycle_degree'] / 2.0
        looking_for_rth = True

        if self.module['thermal_interp_is_four_degree']:
            degree_count = -self.sim_info['step_range']
            attempt_count = 0
            transient_history = [0]
            degree = [-1, 0]
            while looking_for_rth and time_value <= 10.0:
                if attempt_count > 0:
                    guess_slope = (transient_history[-1] - transient_history[-2]) / (degree[-1] - degree[-2])
                    new_degree = round(abs(degree[-1] - (transient_history[-1] - 0.99) / guess_slope))
                    if new_degree == degree[-1]:
                        new_degree += 1
                    degree.append(new_degree)
                degree_count = degree[-1] * 360
                time_step = self.sim_info['sec_per_cycle_degree'] / self.sim_info['step_size'] * (720 + degree_count)
                igbt_trans_rth = self.calculate__rth_from_time(self.igbt, time_step)
                fwd_trans_rth = self.calculate__rth_from_time(self.fwd, time_step)
                check_val = min(igbt_trans_rth / igbt_dc_rth, fwd_trans_rth / fwd_dc_rth)
                transient_history.append(check_val)
                attempt_count += 1
                if check_val >= 0.99:
                    looking_for_rth = False

            time_value = time_step + self.sim_info['sec_per_cycle_degree'] / 2

            rth_fwd_int = self.calculate__rth_integration(self.fwd, degree_count)
            rth_igbt_int = self.calculate__rth_integration(self.igbt, degree_count)

        else:
            rth_fwd_int = np.zeros(self.sim_info['step_range'])
            rth_igbt_int = np.copy(rth_fwd_int)
            while looking_for_rth and time_value <= 10.0:
                time_step = np.arange(self.sim_info['step_range']) * self.sim_info['sec_per_cycle_degree'] + time_value
                rth_fwd_int += self.calculate__rth_from_time(self.fwd, time_step)
                rth_igbt_int += self.calculate__rth_from_time(self.igbt, time_step)
                time_value += self.sim_info['sec_per_cycle_degree'] / self.sim_info['step_size'] * 360
                if rth_igbt_int[-1] / igbt_dc_rth >= 0.99 and rth_fwd_int[-1] / fwd_dc_rth >= 0.99:
                    looking_for_rth = False

        self.igbt['info']['rth_dict'] = rth_igbt_int
        self.fwd['info']['rth_dict'] = rth_fwd_int
        self.module['tj_max']['time_value'] = time_value

    def get__corrected_esw(self, esw_array):
        if 0 not in esw_array:
            return np.insert(esw_array, 0, 0.0)

    def get__corrected_vce(self, checkee_ic, checkee_vce):  # todo is this necessary
        if 0 not in checkee_ic:
            checkee_ic = np.insert(checkee_ic, 0, 0)
            checkee_vce = np.insert(checkee_vce, 0, 0.9 * checkee_vce[0])
        return checkee_ic, checkee_vce

    def get__vcc_value(self, vcc_value):  # todo isn't there one of these already?
        if vcc_value == 650:
            return 300
        elif vcc_value == 1200:
            return 600
        else:
            return vcc_value / 2

    def get__module_name(self, module_file):  # todo shorten the output unknown line
        if type(module_file['Module Name']) is np.ndarray:  # checks to see if module file has module name entered. If not, requests user to add to file.
            return 'Unknown Module - Please add name to module file.'
        else:
            return module_file['Module Name']
