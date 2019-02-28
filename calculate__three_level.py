import Module_class
import System_class
import MaxCurrent_class


def calculate_3_level(simulation_instance):  # todo clean up and comment
    simulation_module_files, simulation_user_input = simulation_instance.get__present_simulation_files_two_level()
    max_current = MaxCurrent_class.MaxCurrent()

    inside_module_file = simulation_module_files['inside_module']
    outside_module_file = simulation_module_files['outside_module']
    diode_module_file = simulation_module_files['diode_module']

    while max_current.is__searching_for_max_current():

        system = System_class.System(simulation_user_input, simulation_instance)

        max_current.modify__max_current(system, simulation_instance)

        inside_module = Module_class.Module(inside_module_file)
        outside_module = Module_class.Module(outside_module_file)
        diode_module = Module_class.Module(diode_module_file)

        inside_module.set__vcc_ratio_and_get_values(system)
        outside_module.set__vcc_ratio_and_get_values(system)
        diode_module.set__vcc_ratio_and_get_values(system)

        inside_module.set__rg(simulation_instance, system, "inside")
        outside_module.set__rg(simulation_instance, system, "outside")
        diode_module.set__rg(simulation_instance, system, "diode")


        outside_module_fwd_current = [abs(current) if current < 0.0 < voltage else 0.0 for current, voltage in zip(system.get__system_output_current(), system.get__system_output_voltage())]
        outside_module_igbt_current = [abs(current) if current > 0.0 and voltage > 0.0 else 0.0 for current, voltage in zip(system.get__system_output_current(), system.get__system_output_voltage())]

        inside_module_fwd_current = [abs(current) if current < 0.0 < voltage else 0.0 for current, voltage in zip(system.get__system_output_current(), system.get__system_output_voltage())]
        inside_module_igbt_current = [abs(current) if current > 0.0 else 0.0 for current in system.get__system_output_current()]

        diode_module_igbt_current = [0.0 for _ in system.get__system_output_current()]
        diode_module_fwd_current = [abs(current) if current > 0.0 else 0.0 for current in system.get__system_output_current()]

        outside_module.set__current_igbt(outside_module_igbt_current)
        outside_module.set__current_fwd(outside_module_fwd_current)

        inside_module.set__current_igbt(inside_module_igbt_current)
        inside_module.set__current_fwd(inside_module_fwd_current)

        diode_module.set__current_igbt(diode_module_igbt_current)
        diode_module.set__current_fwd(diode_module_fwd_current)

        outside_module.calculate__module_loss_and_temps(igbt_cond_duty=system.get__duty_cycle__p(), fwd_cond_duty=system.get__duty_cycle__p())

        inside_igbt_switching_duty = [1.0 - duty if voltage < 0.0 else 0.0 for duty, voltage in zip(system.get__duty_cycle__n(), system.get__system_output_voltage())]
        inside_fwd_switching_duty = [0.0 for _ in system.get__system_output_current()]
        inside_conduction_duty = [1.0 - duty for duty in system.get__duty_cycle__n()]

        inside_module.calculate__conduction_loss__igbt(inside_conduction_duty)
        inside_module.calculate__switching_loss__igbt(inside_igbt_switching_duty)

        inside_module.calculate__module_loss_and_temps(
            igbt_cond_duty=inside_conduction_duty,
            igbt_sw_duty=inside_igbt_switching_duty,
            fwd_cond_duty=system.get__duty_cycle__p(),
            fwd_sw_duty=inside_fwd_switching_duty
        )

        inside_module.calculate__conduction_loss__fwd(system.get__duty_cycle__p())
        inside_module.calculate__switching_loss__fwd(inside_fwd_switching_duty)

        inside_module.calculate__power_and_temps()

        diode_igbt_duty = [0.0 for _ in system.get__system_output_current()]
        diode_fwd_switching_duty = [1 - duty for duty in system.get__duty_cycle__p()]
        diode_fwd_conduction_duty = [1 - duty_p if voltage > 0 else 1 - duty_n for duty_p, duty_n, voltage in zip(system.get__duty_cycle__p(), system.get__duty_cycle__n(), system.get__system_output_voltage())]

        diode_module.calculate__conduction_loss__igbt(diode_igbt_duty)
        diode_module.calculate__switching_loss__igbt(diode_igbt_duty)

        diode_module.calculate__conduction_loss__fwd(diode_fwd_conduction_duty)
        diode_module.calculate__switching_loss__fwd(diode_fwd_switching_duty)

        diode_module.calculate__power_and_temps()

        max_current.check__for_max_current(system, max_current.get__max_current_module(inside_module, outside_module, diode_module), simulation_instance)

    system.create__output_view(inside_module, outside_module, diode_module)
    return system.get__system_output_view()
