import Module_class
import System_class


def calculate_3_level(simulation_instance):  # todo clean up and comment
    simulation_module_files, simulation_user_input = simulation_instance.get__present_simulation_files_two_level()
    tj_hold__condition_met = False
    tj_hold__count = 0
    tj_hold__current = [0]
    tj_hold__temp = []
    error = 0.01

    inside_module_file = simulation_module_files['inside_module']
    outside_module_file = simulation_module_files['outside_module']
    diode_module_file = simulation_module_files['diode_module']

    while not tj_hold__condition_met:

        system = System_class.System(simulation_user_input)

        system.set__modulation(simulation_instance.get__modulation_type())
        system.set__three_level(True)

        if simulation_instance.get__tj_hold_flag():

            if tj_hold__count == 0:
                tj_hold__temp.append(system.get__input_t_sink())

            if tj_hold__count > 0:
                guess_slope = (tj_hold__temp[-1] - tj_hold__temp[-2]) / (tj_hold__current[-1] - tj_hold__current[-2])
                new_current = abs(tj_hold__current[-1] - (tj_hold__temp[-1] - simulation_instance.get__module_max_temp()) / guess_slope)
                system.set__input_current(new_current)

        inside_module = Module_class.Module(inside_module_file)
        outside_module = Module_class.Module(outside_module_file)
        diode_module = Module_class.Module(diode_module_file)

        inside_module.set__rg(simulation_instance, system, "inside")
        outside_module.set__rg(simulation_instance, system, "outside")
        diode_module.set__rg(simulation_instance, system, "diode")

        system.calculate__system_output()

        inside_module.set__vcc_ratio_and_get_values(True, system)
        outside_module.set__vcc_ratio_and_get_values(True, system)
        diode_module.set__vcc_ratio_and_get_values(True, system)

        outside_module_fwd_current = [abs(current) if current < 0.0 < voltage else 0.0 for current, voltage in zip(system.get__system_output_current(), system.get__system_output_voltage())]
        outside_module_igbt_current = [abs(current) if current > 0.0 and voltage > 0.0 else 0.0 for current, voltage in zip(system.get__system_output_current(), system.get__system_output_voltage())]

        inside_module_fwd_current = [abs(current) if current < 0.0 < voltage else 0.0 for current, voltage in zip(system.get__system_output_current(), system.get__system_output_voltage())]
        inside_module_igbt_current = [abs(current) if current > 0.0 else 0.0 for current in system.get__system_output_current()]

        diode_module_fwd_current = [abs(current) if current > 0.0 else 0.0 for current in system.get__system_output_current()]

        outside_module.set__current_igbt(outside_module_igbt_current)
        outside_module.set__current_fwd(outside_module_fwd_current)

        inside_module.set__current_igbt(inside_module_igbt_current)
        inside_module.set__current_fwd(inside_module_fwd_current)

        diode_module_igbt_current = [0.0 for _ in system.get__system_output_current()]

        diode_module.set__current_igbt(diode_module_igbt_current)
        diode_module.set__current_fwd(diode_module_fwd_current)

        outside_module.calculate__conduction_loss__igbt(system.duty_cycle__p)
        outside_module.calculate__switching_loss__igbt()

        outside_module.calculate__conduction_loss__fwd(system.duty_cycle__p)
        outside_module.calculate__switching_loss__fwd()

        outside_module.calculate__power_and_temps()

        inside_igbt_switching_duty = [1.0 - duty if voltage < 0.0 else 0.0 for duty, voltage in zip(system.duty_cycle__n, system.get__system_output_voltage())]
        inside_fwd_switching_duty = [0.0 for _ in system.get__system_output_current()]
        inside_conduction_duty = [1.0 - duty for duty in system.duty_cycle__n]

        inside_module.calculate__conduction_loss__igbt(inside_conduction_duty)
        inside_module.calculate__switching_loss__igbt(inside_igbt_switching_duty)

        inside_module.calculate__conduction_loss__fwd(system.duty_cycle__p)
        inside_module.calculate__switching_loss__fwd(inside_fwd_switching_duty)

        inside_module.calculate__power_and_temps()

        diode_igbt_duty = [0.0 for _ in system.get__system_output_current()]
        diode_fwd_switching_duty = [1 - duty for duty in system.duty_cycle__p]
        diode_fwd_conduction_duty = [1 - duty_p if voltage > 0 else 1 - duty_n for duty_p, duty_n, voltage in zip(system.duty_cycle__p, system.duty_cycle__n, system.get__system_output_voltage())]

        diode_module.calculate__conduction_loss__igbt(diode_igbt_duty)
        diode_module.calculate__switching_loss__igbt(diode_igbt_duty)

        diode_module.calculate__conduction_loss__fwd(diode_fwd_conduction_duty)
        diode_module.calculate__switching_loss__fwd(diode_fwd_switching_duty)

        diode_module.calculate__power_and_temps()

        if simulation_instance.get__tj_hold_flag:
            system_max_temp = max(inside_module.get__max_current(), outside_module.get__max_current(), diode_module.get__max_current())
            tj_hold__temp.append(system_max_temp)
            tj_hold__current.append(system.get__input_current())
            tj_hold__count += 1
            if abs(tj_hold__temp[-1] - simulation_instance.get__module_max_temp()) < error:
                tj_hold__condition_met = True
        else:
            tj_hold__condition_met = True

    system.create__output_view(inside_module, outside_module, diode_module)
    return system.system_output_view
