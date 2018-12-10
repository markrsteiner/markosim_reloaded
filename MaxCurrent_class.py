import System_class
class MaxCurrent:
    def __init__(self):
        self.searching_for_max_current = True
        self.tj_hold__count = 0
        self.tj_hold__current = [0]
        self.tj_hold__temp = []
        self.error = 0.01

    def modify__max_current(self, system, simulation_instance):
        if self.tj_hold__count == 0:
            self.tj_hold__temp.append(system.get__input_t_sink())

        if self.tj_hold__count > 0:
            guess_slope = (self.tj_hold__temp[-1] - self.tj_hold__temp[-2]) / (self.tj_hold__current[-1] - self.tj_hold__current[-2])
            new_current = abs(self.tj_hold__current[-1] - (self.tj_hold__temp[-1] - simulation_instance.get__module_max_temp()) / guess_slope)
            system.set__input_current(new_current)

    def check__for_max_current(self, system, module, simulation_instance):
        if simulation_instance.get__tj_hold_flag():
            self.tj_hold__temp.append(module.get__max_current())
            self.tj_hold__current.append(system.get__input_current())
            self.tj_hold__count += 1
            if abs(self.tj_hold__temp[-1] - simulation_instance.get__module_max_temp()) < self.error:
                self.searching_for_max_current = False
        else:
            self.searching_for_max_current = False

    def is__searching_for_max_current(self):
        return self.searching_for_max_current

