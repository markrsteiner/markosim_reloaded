import math

import numpy as np
from scipy.interpolate import interp1d


class Module:
    def __init__(self, module_file):

        self.nameplate_vcc = module_file['Nameplate VCC']
        if module_file['vcc_ratio'] > 0:
            self.vcc_ratio = module_file['vcc_ratio']
        else:
            self.vcc_ratio = 0
        self.transistor = Transistor(module_file)
        self.diode = Diode(module_file)
        self.name = self.get__module_name(module_file)
        self.rth_dc__module = module_file['Module RTH DC']
        self.module_loss_total = None
        self.delta_tcase_ave = None
        self.thermal_interp_is_four_degree = self.check__thermal_interp()
        self.switches_per_degree = None
        self.input_output_freq = None
        self.time_division = None
        self.input_t_sink = None
        self.step_size = None
        self.step_range = None
        self.sec_per_cycle_degree = None
        self.duty_p = None
        self.time_list = None
        self.rad_list = None
        self.tj_max__time_value = None

    def check__thermal_interp(self):  # todo could this be cleaned?
        if self.transistor.trans_t_values__igbt[2] == 0:
            temp_trans_t = []
            temp_fwd_t = []
            temp_trans_r = []
            temp_fwd_r = []
            temp_trans_t.append(self.transistor.trans_r_values__igbt[1])
            temp_trans_t.append(self.transistor.trans_r_values__igbt[2])
            temp_trans_t.append(self.transistor.trans_t_values__igbt[0])
            temp_trans_t.append(self.transistor.trans_t_values__igbt[1])
            temp_trans_r.append(self.transistor.trans_r_values__igbt[0])
            temp_trans_r.append(self.transistor.trans_r_values__igbt[3])
            temp_fwd_t.append(self.diode.trans_r_values__fwd[1])
            temp_fwd_t.append(self.diode.trans_r_values__fwd[2])
            temp_fwd_t.append(self.diode.trans_t_values__fwd[0])
            temp_fwd_t.append(self.diode.trans_t_values__fwd[1])
            temp_fwd_r.append(self.diode.trans_r_values__fwd[0])
            temp_fwd_r.append(self.diode.trans_r_values__fwd[3])
            self.transistor.trans_r_values__igbt = temp_trans_r
            self.transistor.trans_t_values__igbt = temp_trans_t
            self.diode.trans_r_values__fwd = temp_fwd_r
            self.diode.trans_t_values__fwd = temp_fwd_t
            self.create_thermal_resistance_dict()
            return False
        else:
            self.create_thermal_resistance_dict()
            return True

    def get__max_current(self):
        return max(self.diode.nominal_tj_max__fwd, self.transistor.nominal_tj_max__igbt)

    def set__vcc_ratio_and_get_values(self, is_three_level, system):  # todo call this something different, and break it out for 3-level
        if self.vcc_ratio == 0:
            if is_three_level:
                if self.nameplate_vcc == 6500:
                    self.vcc_ratio = system.get__input_bus_voltage() / 3600
                else:
                    self.vcc_ratio = system.get__input_bus_voltage() / 2.0 / self.get__vcc_value(self.nameplate_vcc)  # fix this at some point, it's not exactly accurate
            else:
                self.vcc_ratio = system.get__input_bus_voltage() / self.get__vcc_value(self.nameplate_vcc)  # fix this at some point, it's not exactly accurate
        else:
            self.vcc_ratio = system.get__input_bus_voltage() / self.vcc_ratio
        self.switches_per_degree = system.get__switches_per_degree()
        self.input_output_freq = system.get__input_output_freq()
        self.time_division = system.get__time_division()
        self.input_t_sink = system.get__input_t_sink()
        self.step_size = system.step_size
        self.step_range = int(360 / self.step_size)
        self.sec_per_cycle_degree = 1.0 / self.input_output_freq / 360.0 * self.step_size
        self.duty_p = system.get__duty_p()

    def set__rg(self, input_instance, system_instance, module_location=None): #todo, fix all of this
        rg_suppress = input_instance.rg_suppress_flag #todo don't do this
        if not rg_suppress:
            system_instance.rg_output_flag = True #todo don't do this
            if module_location is None:
                rg_on = system_instance.input_rg_on
                rg_off = system_instance.input_rg_off
            elif module_location is "inside":
                rg_on = system_instance.input_rg_on_inside
                rg_off = system_instance.input_rg_off_inside
            elif module_location is "outside":
                rg_on = system_instance.input_rg_on_outside
                rg_off = system_instance.input_rg_off_outside
            else:
                rg_suppress = True
                rg_on = None
                rg_off = None
        else:
            system_instance.rg_output_flag = False
            rg_on = None
            rg_off = None
        self.transistor.set__rg(rg_on, rg_off, suppress_flag=rg_suppress)
        self.diode.set__rg(rg_on, rg_off, suppress_flag=rg_suppress)

    def set__current_igbt(self, current):
        self.transistor.set__current(current)

    def set__current_fwd(self, current):
        self.diode.set__current(current)

    def create_thermal_resistance_dict(self):  # todo could this be cleaned
        igbt_dc_rth = self.transistor.get_igbt_rth_from_time(10.0)
        fwd_dc_rth = self.diode.get_fwd_rth_from_time(10.0)
        time_value = self.sec_per_cycle_degree / 2.0
        time_step = 0.0

        rth_fwd_int = []
        rth_igbt_int = []

        if self.thermal_interp_is_four_degree:
            degree_count = -self.step_range
            while time_value <= 10.0:
                degree_count += 360
                time_step += self.sec_per_cycle_degree / self.step_size * 360
                igbt_trans_rth = self.transistor.get_igbt_rth_from_time(time_step)
                fwd_trans_rth = self.diode.get_fwd_rth_from_time(time_step)
                if igbt_trans_rth / igbt_dc_rth >= 0.99 and fwd_trans_rth / fwd_dc_rth >= 0.99:
                    break

            time_value = time_step + self.sec_per_cycle_degree / 2
            for i in range(self.step_range):
                rth_fwd_int.append(self.diode.integrate_rth_fwd(self.step_size, self.sec_per_cycle_degree, degree_count, i))
                rth_igbt_int.append(self.transistor.integrate_rth_igbt(self.step_size, self.sec_per_cycle_degree, degree_count, i))
        else:
            degree_count = 0
            for deg in range(self.step_range):
                rth_fwd_int.append(0)
                rth_igbt_int.append(0)
            while time_value <= 10.0:
                degree_count += 1
                for deg in range(self.step_range):
                    time_step = (deg) * self.sec_per_cycle_degree + time_value
                    rth_fwd_int[deg] += self.diode.get_fwd_rth_from_time(time_step)
                    rth_igbt_int[deg] += self.transistor.get_igbt_rth_from_time(time_step)
                time_value += self.sec_per_cycle_degree / self.step_size * 360
                if self.transistor.get_igbt_rth_from_time(time_value) / igbt_dc_rth >= 0.99 and self.diode.get_fwd_rth_from_time(time_value) / fwd_dc_rth >= 0.99:
                    break

        self.transistor.tj_max__igbt_thermo = rth_igbt_int
        self.diode.tj_max__fwd_thermo = rth_fwd_int
        self.tj_max__time_value = time_value


    def rotate(self, l, n):
        return l[-n:] + l[:-n]

    def rth_integral_four(self, step, spcd, index, scalar, growth, time):  # todo does everything need to be passed in?
        denom = math.exp(-360 / step * spcd / growth) - 1
        num1 = -math.exp(-spcd * (720 / step * time + 2 * index + 720 / step + 1) / (2 * growth))
        num2 = -time
        num3 = time * math.exp(-360 / step * spcd / growth)
        num4 = math.exp(-spcd * (1 + 2 * index) / (2 * growth))
        num5 = -1
        num6 = math.exp(-360 / step * spcd / growth)
        out = scalar / denom * (num1 + num2 + num3 + num4 + num5 + num6)
        return out

    def get__corrected_esw(self, checkee):  # todo could this be simplified?
        found = False
        for x in range(len(checkee)):
            if checkee[x] == 0:
                found = True
        if not found:
            checkee = np.insert(checkee, 0, 0.0)
        return checkee

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
            return "Unknown Module - Please add name to module file."
        else:
            return module_file['Module Name']

    def calculate__energy_power(self):
        self.transistor.calculate__energy_power()
        self.diode.calculate__energy_power()
        self.module_loss_total = self.transistor.device_loss_total__igbt + self.diode.device_loss_total__fwd


class Transistor:
    def __init__(self, module_file):
        temp_ic, temp_vce = self.get__corrected_vce(module_file["IC - IC VCE"], module_file["VCE - IC VCE"])
        self.ic_vce = interp1d(temp_ic, temp_vce, fill_value='extrapolate')
        self.ic_esw_on = interp1d(self.get__corrected_esw(module_file["IC - IC ESWON"]), self.get__corrected_esw(module_file["ESWON - IC ESWON"]), fill_value='extrapolate')
        self.ic_esw_off = interp1d(self.get__corrected_esw(module_file["IC - IC ESWOFF"]), self.get__corrected_esw(module_file["ESWOFF - IC ESWOFF"]), fill_value='extrapolate')
        self.rg_on_esw_on = interp1d(module_file["RGON - ESWON RGON"], module_file["ESWON - ESWON RGON"], fill_value='extrapolate')
        self.rg_off_esw_off = interp1d(module_file["RGOFF - ESWOFF RGOFF"], module_file["ESWOFF - ESWOFF RGOFF"], fill_value='extrapolate')
        self.current = []
        self.conduction_loss = []
        self.esw_on_loss = []
        self.esw_off_loss = []
        self.esw_loss__igbt = []
        self.energy__igbt = []
        self.instantaneous_power__igbt = []
        self.rth_dc__igbt = module_file['IGBT RTH DC']
        self.trans_r_values__igbt = module_file["IGBT R Values"]
        self.trans_t_values__igbt = module_file["IGBT T Values"]
        self.conduction_loss_total = None
        self.esw_on_loss_total = None
        self.esw_off_loss_total = None
        self.esw_loss_total = None
        self.device_loss_total__igbt = None
        self.delta_tj_ave__igbt = None
        self.nominal_tj_ave__igbt = None
        self.delta_tj_max__igbt = None
        self.nominal_tj_max__igbt = None
        self.tj_max_igbt_list = []
        self.tj_igbt_list = None
        self.tj_max__igbt_thermo = None
        self.rg_scalar_esw_on = None
        self.rg_scalar_esw_off = None

    def calculate__conduction_loss(self, duty):
        self.conduction_loss = [curr * duty * self.ic_vce(curr) * self.step_size / 360.0 if curr > 0.0 else 0.0 for curr, duty in zip(self.current, duty)]
        self.conduction_loss_total = sum(self.conduction_loss)

    def calculate__esw_on_loss(self, duty=None):
        if duty is None:
            duty = self.duty_p

        self.esw_on_loss = [self.switches_per_degree * self.ic_esw_on(curr) * self.rg_scalar_esw_on * self.vcc_ratio * self.input_output_freq if curr > 0.0 and 0.0 < duty < 1.0 else 0.0 for curr, duty in zip(self.current, duty)]
        self.esw_on_loss_total = sum(self.esw_on_loss)

    def calculate__esw_off_loss(self, duty=None):
        if duty is None:
            duty = self.duty_p
        self.esw_off_loss = [self.switches_per_degree * self.ic_esw_off(curr) * self.rg_scalar_esw_off * self.vcc_ratio * self.input_output_freq if curr > 0.0 and 0.0 < duty < 1.0 else 0.0 for curr, duty in zip(self.current, duty)]
        self.esw_off_loss_total = sum(self.esw_off_loss)

    def calculate__max_temp(self):  # maybe split into igbt and fwd separately?
        tj_igbt_list = []

        next_array_igbt = self.instantaneous_power__igbt
        next_array_igbt = self.rotate(next_array_igbt, -1)
        delta_p_igbt = [next_el - last_el for next_el, last_el in zip(next_array_igbt, self.instantaneous_power__igbt)]
        last_power_igbt = self.instantaneous_power__igbt[-1] - self.device_loss_total__igbt
        first_power_igbt = self.instantaneous_power__igbt[0] - self.device_loss_total__igbt
        rth_dict_igbt_added = [self.get_igbt_rth_from_time(i * self.sec_per_cycle_degree + self.tj_max__time_value) for i in range(self.step_range)]
        rth_dict_igbt_added = [old + new for old, new in zip(self.tj_max__igbt_thermo, rth_dict_igbt_added)]
        tj_igbt_inst_init = [self.input_t_sink + self.delta_tj_ave__igbt + self.delta_tcase_ave - last_power_igbt * self.tj_max__igbt_thermo[i] + first_power_igbt * rth_dict_igbt_added[i] for i in range(self.step_range)]

        for index in range(self.step_range):
            rth_dict_igbt_fix = [rth_dict_igbt_added[i] if i <= index else self.tj_max__igbt_thermo[i] for i in range(self.step_range)]
            # rth_dict_igbt_fix_orig = [val for val in rth_dict_igbt_fix]
            rth_dict_igbt_fix.reverse()

            new_rth_igbt = self.rotate(rth_dict_igbt_fix, index)
            new_rth_igbt = new_rth_igbt[:359]
            temp_add_vals_igbt = [delta_p * rth for delta_p, rth in zip(delta_p_igbt, new_rth_igbt)]
            sum_temp_add_vals_igbt = sum(temp_add_vals_igbt)
            tj_igbt_list.append(sum_temp_add_vals_igbt)

        tj_igbt_list = [tj + diff for tj, diff in zip(tj_igbt_inst_init, tj_igbt_list)]
        tj_ave_igbt = self.nominal_tj_ave__igbt - np.average(tj_igbt_list)
        self.tj_igbt_list = [tj + tj_ave_igbt for tj in tj_igbt_list]

        self.time_list = [i * self.sec_per_cycle_degree + self.tj_max__time_value for i in range(self.step_range)]
        self.rad_list = [i * self.step_size for i in range(self.step_range)]

        self.nominal_tj_max__igbt = max(tj_igbt_list)
        self.delta_tj_max__igbt = max(self.tj_igbt_list) - self.input_t_sink
        self.tj_max_igbt_list = tj_igbt_list

    def get_igbt_rth_from_time(self, time):
        num = 0
        if self.thermal_interp_is_four_degree:
            for i in range(0, 4):
                num += self.trans_r_values__igbt[i] * (1.0 - math.exp(-1.0 * time / self.trans_t_values__igbt[i]))
        else:
            for i in range(0, 2):
                num += self.trans_r_values__igbt[i] * (1.0 - math.exp(-1.0 * pow(time, self.trans_t_values__igbt[2 * i]) / self.trans_t_values__igbt[2 * i + 1]))

        return num * self.rth_dc__igbt

    def integrate_rth_igbt(self, step, spcd, start_time, index):  # todo could this be folded into below
        start_time = math.floor(start_time / 360)
        num = 0
        for i in range(4):
            num += self.rth_integral_four(step, spcd, index, self.trans_r_values__igbt[i], self.trans_t_values__igbt[i], start_time)
        return num * self.rth_dc__igbt

    def calculate__energy_power(self):
        self.esw_loss__igbt = [eswon + eswoff for eswon, eswoff in zip(self.esw_on_loss, self.esw_off_loss)]
        self.energy__igbt = [conduction + esw_loss for conduction, esw_loss in zip(self.conduction_loss, self.esw_loss__igbt)]
        self.instantaneous_power__igbt = [energy / self.input_output_freq / self.time_division for energy in self.energy__igbt]
        self.device_loss_total__igbt = self.conduction_loss_total + self.esw_loss_total

    def calculate__temperatures(self):
        self.delta_tj_ave__igbt = self.device_loss_total__igbt * self.rth_dc__igbt
        self.nominal_tj_ave__igbt = self.input_t_sink + self.delta_tj_ave__igbt + self.delta_tcase_ave
        self.calculate__max_temp()

    def set__rg(self, rg_on=0.0, rg_off=0.0, suppress_flag=0.0):
        if suppress_flag:
            self.rg_scalar_esw_on = 1
            self.rg_scalar_esw_off = 1
        else:
            self.rg_scalar_esw_on = self.rg_on_esw_on(rg_on)
            self.rg_scalar_esw_off = self.rg_off_esw_off(rg_off)

    def set__current(self, current):
        self.current = current


class Diode:
    def __init__(self, module_file):
        temp_if, temp_vf = self.get__corrected_vce(module_file["IF - IF VF"], module_file["VF - IF VF"])
        self.ic_err = interp1d(self.get__corrected_esw(module_file["IC - IC ERR"]), self.get__corrected_esw(module_file["ERR - IC ERR"]), fill_value='extrapolate')
        self.if_vf = interp1d(temp_if, temp_vf, fill_value='extrapolate')
        self.rg_on_err = interp1d(module_file["RGON - ERR RGON"], module_file["ERR - ERR RGON"], fill_value='extrapolate')
        self.current = []
        self.conduction_loss__fwd = []
        self.err_loss = []
        self.energy__fwd = []
        self.instantaneous_power__fwd = []
        self.rg_scalar_err = None
        self.rth_dc__fwd = module_file['FWD RTH DC']
        self.trans_r_values__fwd = module_file["FWD R Values"]
        self.trans_t_values__fwd = module_file["FWD T Values"]
        self.conduction_loss_total__fwd = None
        self.err_loss_total = None
        self.device_loss_total__fwd = None
        self.delta_tj_ave__fwd = None
        self.nominal_tj_ave__fwd = None
        self.delta_tj_max__fwd = None
        self.nominal_tj_max__fwd = None
        self.tj_max_fwd_list = []
        self.tj_fwd_list = None
        self.tj_max__fwd_thermo = None

    def calculate__conduction_loss(self, duty):
        self.conduction_loss__fwd = [curr * duty * self.if_vf(curr) * self.step_size / 360.0 if curr > 0.0 else 0.0 for curr, duty in zip(self.current, duty)]
        self.conduction_loss_total__fwd = sum(self.conduction_loss__fwd)

    def calculate__err_loss(self, duty=None):
        if duty is None:
            duty = self.duty_p

        self.err_loss = [self.switches_per_degree * self.ic_err(curr) * self.rg_scalar_err * self.vcc_ratio * self.input_output_freq if curr > 0.0 and 0.0 < duty < 1.0 else 0.0 for curr, duty in zip(self.current, duty)]
        self.err_loss_total = sum(self.err_loss)

    def calculate__max_temp(self):  # maybe split into igbt and fwd separately?
        tj_fwd_list = []

        delta_tj_fwd = self.device_loss_total__fwd * self.rth_dc__fwd
        next_array_fwd = self.instantaneous_power__fwd
        next_array_fwd = self.rotate(next_array_fwd, -1)
        delta_p_fwd = [next_el - last_el for next_el, last_el in zip(next_array_fwd, self.instantaneous_power__fwd)]
        last_power_fwd = self.instantaneous_power__fwd[-1] - self.device_loss_total__fwd
        first_power_fwd = self.instantaneous_power__fwd[0] - self.device_loss_total__fwd
        rth_dict_fwd_added = [self.get_fwd_rth_from_time(i * self.sec_per_cycle_degree + self.tj_max__time_value) for i in range(self.step_range)]
        rth_dict_fwd_added = [old + new for old, new in zip(self.tj_max__fwd_thermo, rth_dict_fwd_added)]
        tj_fwd_inst_init = [self.input_t_sink + delta_tj_fwd + self.delta_tcase_ave - last_power_fwd * self.tj_max__fwd_thermo[i] + first_power_fwd * rth_dict_fwd_added[i] for i in range(self.step_range)]

        for index in range(self.step_range):
            rth_dict_fwd_fix = [rth_dict_fwd_added[i] if i <= index else self.tj_max__fwd_thermo[i] for i in range(self.step_range)]
            # rth_dict_fwd_fix_orig = [val for val in rth_dict_fwd_fix]
            rth_dict_fwd_fix.reverse()

            new_rth_fwd = self.rotate(rth_dict_fwd_fix, index)
            new_rth_fwd = new_rth_fwd[:359]
            temp_add_vals_fwd = [delta_p * rth for delta_p, rth in zip(delta_p_fwd, new_rth_fwd)]
            sum_temp_add_vals_fwd = sum(temp_add_vals_fwd)
            tj_fwd_list.append(sum_temp_add_vals_fwd)

        tj_fwd_list = [tj + diff for tj, diff in zip(tj_fwd_inst_init, tj_fwd_list)]
        tj_ave_fwd = self.nominal_tj_ave__fwd - np.average(tj_fwd_list)
        self.tj_fwd_list = [tj + tj_ave_fwd for tj in tj_fwd_list]

        self.time_list = [i * self.sec_per_cycle_degree + self.tj_max__time_value for i in range(self.step_range)]
        self.rad_list = [i * self.step_size for i in range(self.step_range)]

        self.nominal_tj_max__fwd = max(tj_fwd_list)
        self.delta_tj_max__fwd = max(self.tj_fwd_list) - self.input_t_sink
        self.tj_max_fwd_list = tj_fwd_list

    def get_fwd_rth_from_time(self, time):  # todo could this be folded into below
        num = 0
        if self.thermal_interp_is_four_degree:
            for i in range(0, 4):
                num += self.trans_r_values__fwd[i] * (1.0 - math.exp(-1.0 * time / self.trans_t_values__fwd[i]))
        else:
            for i in range(0, 2):
                num += self.trans_r_values__fwd[i] * (1.0 - math.exp(-1.0 * pow(time, self.trans_t_values__fwd[2 * i]) / self.trans_t_values__fwd[2 * i + 1]))
        return num * self.rth_dc__fwd

    def integrate_rth_fwd(self, step, spcd, start_time, index):  # todo remove interp check
        start_time = math.floor(start_time / 360)
        num = 0
        for i in range(4):
            num += self.rth_integral_four(step, spcd, index, self.trans_r_values__fwd[i], self.trans_t_values__fwd[i], start_time)
        return num * self.rth_dc__fwd

    def calculate__energy_power(self):
        self.energy__fwd = [conduction + err for conduction, err in zip(self.conduction_loss__fwd, self.err_loss)]
        self.instantaneous_power__fwd = [energy / self.input_output_freq / self.time_division for energy in self.energy__fwd]
        self.device_loss_total__fwd = self.conduction_loss_total__fwd + self.err_loss_total

    def calculate__temperatures(self):
        self.delta_tj_ave__fwd = self.device_loss_total__fwd * self.rth_dc__fwd
        self.nominal_tj_ave__fwd = self.input_t_sink + self.delta_tj_ave__fwd + self.delta_tcase_ave
        self.calculate__max_temp()

    def set__rg(self, rg_on=0.0, rg_off=0.0, suppress_flag=False):
        if suppress_flag:
            self.rg_scalar_err = 1
        else:
            self.rg_scalar_err = self.rg_on_err(rg_on)

    def set__current(self, current):
        self.current = current
