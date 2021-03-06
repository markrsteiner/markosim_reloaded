import Module_class
import System_class
import MaxCurrent_class

def simulation__two_level(simulation_instance):  # todo clean up and comment
    simulation_module_file, simulation_user_input = simulation_instance.get__present_simulation_files_two_level()
    max_current = MaxCurrent_class.MaxCurrent()

    while max_current.is__searching_for_max_current():
        system = System_class.System(simulation_user_input, simulation_instance)

        max_current.modify__max_current(system, simulation_instance)

        module = Module_class.Module(simulation_module_file)
        module.set__vcc_ratio_and_get_values(system)
        module.set__rg(simulation_instance, system)

        igbt_current = [val if val > 0.0 else 0.0 for val in system.get__system_output_current()]
        fwd_current = [abs(val) if val < 0.0 else 0.0 for val in system.get__system_output_current()]

        module.set__current_igbt(igbt_current)
        module.set__current_fwd(fwd_current)

        module.calculate__module_loss_and_temps()

        max_current.check__for_max_current(system, module, simulation_instance)

    system.create__output_view(module)
    if simulation_instance.nerd_output_flag:
        simulation_instance.nerd_output_module = module
    return system.get__system_output_view()
