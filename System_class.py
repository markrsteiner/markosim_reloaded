import math

import numpy as np

import format__output


class System:
    def __init__(self, user_input_file: dict) -> None:  # should take simulator instance or something
        self.input_bus_voltage = float(user_input_file['Vcc [V]'])
        self.input_ic_peak = float(user_input_file['Io [Apk]'])
        self.input_mod_depth = float(user_input_file['Mod. Depth'])
        self.input_output_freq = float(user_input_file['fo [Hz]'])
        self.input_t_sink = float(user_input_file['Ts [\u00B0C]'])
        self.input_modulation_type = ""
        self.input_rg_on = float(user_input_file['rg on [\u03A9]'])
        self.input_rg_off = float(user_input_file['rg off [\u03A9]'])
        self.input_rg_on_inside = 0
        self.input_rg_off_inside = 0
        self.input_rg_on_outside = 0
        self.input_rg_off_outside = 0
        self.is_three_level = False
        self.rg_output_flag = True
        self.step_size = int(1) #todo fix later
        self.time_division = 1 / self.input_output_freq / 360.0 * self.step_size
        self.power_factor_phase_shift = math.acos(float(user_input_file['PF [cos(\u03D5)]'])) * 180 / math.pi
        self.switches_per_degree = float(user_input_file['fc [kHz]']) * self.time_division
        self.output_current = []
        self.output_voltage = []
        self.system_output_view = {}

        # may delete, checking
        self.cycle_angle__radian = []
        self.cycle_angle__degree = []
        self.system_output_voltage = []
        self.output_current_full = []
        self.duty_cycle__p = []
        self.duty_cycle__n = []

    def set__three_level(self, is_three_level):
        self.is_three_level = is_three_level
        self.input_bus_voltage /= 2

    def set__modulation(self, input__modulation_type):
        self.input_modulation_type = input__modulation_type

    def set__input_current(self, input_current):
        self.input_ic_peak = input_current

    def get__input_current(self):
        return self.input_ic_peak

    def get__input_bus_voltage(self):
        return self.input_bus_voltage

    def get__switches_per_degree(self):
        return self.switches_per_degree

    def get__input_output_freq(self):
        return self.input_output_freq

    def get__duty_cycle__p(self):
        return self.duty_cycle__p

    def get__step_size(self):
        return self.step_size

    def get__time_division(self):
        return self.time_division

    def get__input_t_sink(self):
        return self.input_t_sink

    def get__system_output_current(self):
        return self.output_current_full

    def get__system_output_voltage(self):
        return self.system_output_voltage

    def get__system_output_view(self):
        return self.system_output_view

    def calculate__system_output(self):
        self.cycle_angle__radian = [i * self.step_size + self.step_size / 2 for i in range(int(360 / self.step_size))]
        self.cycle_angle__degree = [val * math.pi / 180 for val in self.cycle_angle__radian]

        if self.input_modulation_type == "Sinusoidal":
            self.calculate__system_outputs()
            # if self.input_modulation_type == "SVPWM":  #add later maybe
            #     self.set_next_current__SVPWM()
            # if self.input_modulation_type == 'Two Phase I':
            #     self.set_next_current__2phase_i()
        if self.is_three_level:
            self.duty_cycle__p = [np.clip(voltage / self.input_bus_voltage, 0, 1) for voltage in self.system_output_voltage]
            self.duty_cycle__n = [np.clip(-voltage / self.input_bus_voltage, 0, 1) for voltage in self.system_output_voltage]
        else:
            self.duty_cycle__p = [np.clip(voltage / self.input_bus_voltage, 0, 1) for voltage in self.system_output_voltage]
            self.duty_cycle__n = [np.clip(-voltage / self.input_bus_voltage, 0, 1) for voltage in self.system_output_voltage]

    def create__output_view(self, inside_module, outside_module=None, diode_module=None):
        is_three_level = outside_module is not None and diode_module is not None
        if is_three_level:
            self.system_output_view = format__output.build__output_view_dict(self, inside_module, outside_module, diode_module)
        else:
            self.system_output_view = format__output.build__output_view_dict(self, inside_module)
            self.system_output_view.update({'Modulation': self.input_modulation_type})
            if self.rg_output_flag:
                self.system_output_view.update({'rg on [\u03A9]': self.input_rg_on, 'rg off [\u03A9]': self.input_rg_off})
            else:
                self.system_output_view.update({'rg on [\u03A9]': "STOCK", 'rg off [\u03A9]': "STOCK"})

    def calculate__system_outputs(self):
        if self.is_three_level:
            self.system_output_voltage = [self.input_bus_voltage * (self.input_mod_depth * math.sin(deg)) for deg in self.cycle_angle__degree]
        else:
            self.system_output_voltage = [self.input_bus_voltage * (1 + self.input_mod_depth * math.sin(deg)) / 2.0 for deg in self.cycle_angle__degree]
        self.output_current_full = [self.input_ic_peak * math.sin(deg - self.power_factor_phase_shift * math.pi / 180) for deg in self.cycle_angle__degree]

    def set_next_current__SVPWM(self):  # todo fix and/or maybe make into generator? Have to conisder
        modified_input_mod_depth = self.input_mod_depth * math.sqrt(3) / 2
        sector = self.rad_delta_math[-1] * 3 / math.pi
        if sector <= 1:
            duty_cycle = modified_input_mod_depth * math.cos(self.rad_delta_math - math.pi / 6) + (1.0 - modified_input_mod_depth * math.cos(self.rad_delta_math - math.pi / 6)) / 2.0
        elif sector <= 2:
            duty_cycle = modified_input_mod_depth * math.sin(2 * math.pi / 3 - self.rad_delta_math) + (1.0 - modified_input_mod_depth * math.cos(self.rad_delta_math - math.pi / 2)) / 2.0
        elif sector <= 3:
            duty_cycle = (1.0 - modified_input_mod_depth * math.cos(self.rad_delta_math - 5 * math.pi / 6)) / 2.0
        elif sector <= 4:
            duty_cycle = (1.0 - modified_input_mod_depth * math.cos(self.rad_delta_math - 7 * math.pi / 6)) / 2.0
        elif sector <= 5:
            duty_cycle = modified_input_mod_depth * math.sin(self.rad_delta_math - 4 * math.pi / 3) + (1.0 - modified_input_mod_depth * math.cos(self.rad_delta_math - 3 * math.pi / 2)) / 2.0
        elif sector <= 6:
            duty_cycle = modified_input_mod_depth * math.cos(self.rad_delta_math - 11 * math.pi / 6) + (1.0 - modified_input_mod_depth * math.cos(self.rad_delta_math - 11 * math.pi / 6)) / 2.0
        else:
            return

        self.output_voltage.append(self.input_bus_voltage * duty_cycle)
        self.output_current.append(self.input_ic_peak * math.cos((self.rad_delta[-1] - self.power_factor_phase_shift) * math.pi / 180.0))  # todo change power factor phase shift to radians

    def set_next_current__2phase_i(self):
        modified_input_mod_depth = self.input_mod_depth * math.sqrt(3) / 2
        sector = self.rad_delta_math[-1] * 3 / math.pi
        if sector <= 1:
            duty_cycle = modified_input_mod_depth * math.sin(self.rad_delta_math + math.pi / 6)
        elif 1 < sector <= 2:
            duty_cycle = 1.0
        elif 2 < sector <= 3:
            duty_cycle = -modified_input_mod_depth * math.sin(self.rad_delta_math - 7 * math.pi / 6)
        elif 3 < sector <= 4:
            duty_cycle = 1.0 + modified_input_mod_depth * math.sin(self.rad_delta_math + math.pi / 6)
        elif 4 < sector <= 5:
            duty_cycle = 0.0
        elif 5 < sector <= 6:
            duty_cycle = 1.0 - modified_input_mod_depth * math.sin(self.rad_delta_math - 7 * math.pi / 6)
        else:
            return  # todo add an error here

        self.output_voltage.append(self.input_bus_voltage * duty_cycle)
        self.output_current.append(self.input_ic_peak * math.sin((self.rad_delta[-1] - self.power_factor_phase_shift) * math.pi / 180.0))