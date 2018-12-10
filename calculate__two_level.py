import Module_class
import System_class
import MaxCurrent_class

def simulation__two_level(simulation_instance):  # todo clean up and comment
    simulation_module_file, simulation_user_input = simulation_instance.get__present_simulation_files_two_level()
    max_current = MaxCurrent_class.MaxCurrent()
    # tj_hold__condition_met = False
    # tj_hold__count = 0
    # tj_hold__current = [0]
    # tj_hold__temp = []
    # error = 0.01

    while max_current.is__searching_for_max_current():
        system = System_class.System(simulation_user_input)
        system.set__modulation(simulation_instance.get__modulation_type())

        max_current.modify__max_current(system, simulation_instance)

        # if simulation_instance.get__tj_hold_flag():
        #
        #     if tj_hold__count == 0:
        #         tj_hold__temp.append(system.get__input_t_sink())
        #
        #     if tj_hold__count > 0:
        #         guess_slope = (tj_hold__temp[-1] - tj_hold__temp[-2]) / (tj_hold__current[-1] - tj_hold__current[-2])
        #         new_current = abs(tj_hold__current[-1] - (tj_hold__temp[-1] - simulation_instance.get__module_max_temp()) / guess_slope)
        #         system.set__input_current(new_current)

        system.calculate__system_output()

        module = Module_class.Module(simulation_module_file)
        module.set__vcc_ratio_and_get_values(False, system)
        module.set__rg(simulation_instance, system)

        igbt_current = [val if val > 0.0 else 0.0 for val in system.get__system_output_current()]
        fwd_current = [abs(val) if val < 0.0 else 0.0 for val in system.get__system_output_current()]

        module.set__current_igbt(igbt_current)
        module.set__current_fwd(fwd_current)

        module.calculate__conduction_loss__igbt(system.get__duty_cycle__p())
        module.calculate__switching_loss__igbt()

        module.calculate__conduction_loss__fwd(system.get__duty_cycle__p())
        module.calculate__switching_loss__fwd()

        module.calculate__power_and_temps()

        max_current.check__for_max_current(system, module, simulation_instance)

        # if simulation_instance.get__tj_hold_flag():
        #     tj_hold__temp.append(module.get__max_current())
        #     tj_hold__current.append(system.get__input_current())
        #     tj_hold__count += 1
        #     if abs(tj_hold__temp[-1] - simulation_instance.get__module_max_temp()) < error:
        #         tj_hold__condition_met = True
        # else:
        #     tj_hold__condition_met = True

    system.create__output_view(module)
    if simulation_instance.nerd_output_flag:
        simulation_instance.nerd_output_module = module
    return system.get__system_output_view()
