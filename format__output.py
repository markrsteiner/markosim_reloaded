def build__output_view_dict(system, inside_module, outside_module=None, diode_module=None):
    is_three_level = outside_module is not None and diode_module is not None
    if is_three_level:
        return {
            'Vcc [V]': system.input_bus_voltage,
            'Io [Apk]': system.input_ic_peak,
            'PF [cos(\u03D5)]': system.input_power_factor,
            'Mod. Depth': system.input_mod_depth,
            'fc [kHz]': system.input_carrier_freq,
            'fo [Hz]': system.input_output_freq,
            'Ts [\u00B0C]': system.input_t_sink,

            'P Cond. IGBT Outside [W]': outside_module.conduction_loss_total__igbt,
            'Psw,on IGBT Outside [W]': outside_module.esw_on_loss_total,
            'Psw,off IGBT Outside [W]': outside_module.esw_off_loss_total,
            'Psw IGBT Outside [W]': outside_module.esw_loss_total,
            'P Total IGBT Outside [W]': outside_module.device_loss_total__igbt,

            'P Cond FWD Outside [W]': outside_module.conduction_loss_total__fwd,
            'Prr FWD Outside [W]': outside_module.err_loss_total,
            'P Total FWD Outside [W]': outside_module.device_loss_total__fwd,

            'P Cond. IGBT Inside [W]': inside_module.conduction_loss_total__igbt,
            'Psw,on IGBT Inside [W]': inside_module.esw_on_loss_total,
            'Psw,off IGBT Inside [W]': inside_module.esw_off_loss_total,
            'Psw IGBT Inside [W]': inside_module.esw_loss_total,
            'P Total IGBT Inside [W]': inside_module.device_loss_total__igbt,

            'P Cond FWD Inside [W]': inside_module.conduction_loss_total__fwd,
            'Prr FWD Inside [W]': inside_module.err_loss_total,
            'P Total FWD Inside [W]': inside_module.device_loss_total__fwd,

            'P Cond FWD Diode [W]': diode_module.conduction_loss_total__fwd,
            'Prr FWD Diode [W]': diode_module.err_loss_total,
            'P Total FWD Diode [W]': diode_module.device_loss_total__fwd,

            'P Total Outside [W]': outside_module.module_loss_total * 2,
            'P Total Inside [W]': inside_module.module_loss_total * 2,
            'P Total Diode [W]': diode_module.module_loss_total * 2,

            'ΔT\u2C7C Ave IGBT Outside [K]': outside_module.delta_tj_ave__igbt,
            'ΔT\u2C7C Ave FWD Outside [K]': outside_module.delta_tj_ave__fwd,
            'ΔT\u2C7C Ave IGBT Inside [K]': inside_module.delta_tj_ave__igbt,
            'ΔT\u2C7C Ave FWD Inside [K]': inside_module.delta_tj_ave__fwd,
            'ΔT\u2C7C Ave FWD Diode [K]': diode_module.delta_tj_ave__fwd,

            # Not actually delta_tc, change name - input_tc should be input_ts and this should be nominal tc
            'Tcase Ave. Outside [\u00B0C]': outside_module.delta_tcase_ave + system.input_t_sink,
            'Tcase Ave. Inside [\u00B0C]': inside_module.delta_tcase_ave + system.input_t_sink,
            'Tcase Ave. Diode [\u00B0C]': diode_module.delta_tcase_ave + system.input_t_sink,

            'T\u2C7C Ave IGBT Outside [\u00B0C]': outside_module.nominal_tj_ave__igbt,
            'T\u2C7C Ave FWD Outside [\u00B0C]': outside_module.nominal_tj_ave__fwd,
            'T\u2C7C Ave IGBT Inside [\u00B0C]': inside_module.nominal_tj_ave__igbt,
            'T\u2C7C Ave FWD Inside [\u00B0C]': inside_module.nominal_tj_ave__fwd,
            'T\u2C7C Ave FWD Diode [\u00B0C]': diode_module.nominal_tj_ave__fwd,

            'ΔT\u2C7C Max IGBT Outside [K]': outside_module.delta_tj_max__igbt,
            'ΔT\u2C7C Max FWD Outside [K]': outside_module.delta_tj_max__fwd,
            'ΔT\u2C7C Max IGBT Inside [K]': inside_module.delta_tj_max__igbt,
            'ΔT\u2C7C Max FWD Inside [K]': inside_module.delta_tj_max__fwd,
            'ΔT\u2C7C Max FWD Diode [K]': diode_module.delta_tj_max__fwd,

            'T\u2C7C Max IGBT Outside [\u00B0C]': outside_module.nominal_tj_max__igbt,
            'T\u2C7C Max FWD Outside [\u00B0C]': outside_module.nominal_tj_max__fwd,
            'T\u2C7C Max IGBT Inside [\u00B0C]': inside_module.nominal_tj_max__igbt,
            'T\u2C7C Max FWD Inside [\u00B0C]': inside_module.nominal_tj_max__fwd,
            'T\u2C7C Max FWD Diode [\u00B0C]': diode_module.nominal_tj_max__fwd,

            'Outside Module Name': outside_module.name,
            'Inside Module Name': inside_module.name,
            'Diode Module Name': diode_module.name
        }
    else:
        return {
            'P Total IGBT [W]': inside_module.device_loss_total__igbt,
            'P Cond IGBT [W]': inside_module.conduction_loss_total__igbt,
            'Psw IGBT [W]': inside_module.esw_loss_total,
            'Psw,on IGBT [W]': inside_module.esw_on_loss_total,
            'Psw,off IGBT [W]': inside_module.esw_off_loss_total,
            'ΔT\u2C7C ave. IGBT [K]': inside_module.delta_tj_ave__igbt,
            'T\u2C7C ave. IGBT [\u00B0C]': inside_module.nominal_tj_ave__igbt,
            'ΔT\u2C7C Max_IGBT [K]': inside_module.delta_tj_max__igbt,
            'T\u2C7C Max IGBT [\u00B0C]': inside_module.nominal_tj_max__igbt,
            'Tcase Ave. [\u00B0C]': inside_module.delta_tcase_ave + system.input_t_sink,
            'P Total FWD [W]': inside_module.device_loss_total__fwd,
            'P Cond FWD [W]': inside_module.conduction_loss_total__fwd,
            'Prr FWD [W]': inside_module.err_loss_total,
            'ΔT\u2C7C Ave FWD [K]': inside_module.delta_tj_ave__fwd,
            'T\u2C7C Ave FWD [\u00B0C]': inside_module.nominal_tj_ave__fwd,
            'ΔT\u2C7C Max FWD [K]': inside_module.delta_tj_max__fwd,
            'T\u2C7C Max FWD [\u00B0C]': inside_module.nominal_tj_max__fwd,
            'P Arm [W]': inside_module.module_loss_total,
            'Vcc [V]': system.input_bus_voltage,
            'Io [Apk]': system.input_ic_peak,
            'PF [cos(\u03D5)]': system.input_power_factor,
            'Mod. Depth': system.input_mod_depth,
            'fc [kHz]': system.input_carrier_freq,
            'fo [Hz]': system.input_output_freq,
            'Ts [\u00B0C]': system.input_t_sink,
            'Module Name': inside_module.name
        }


def build__output_file_header(three_level_flag):
    if three_level_flag:
        return [
            'Module Name',
            'Modulation',
            'Vcc [V]',
            'Io [Apk]',
            'PF [cos(\u03D5)]',
            'Mod. Depth',
            'fc [kHz]',
            'fo [Hz]',
            'rg on [\u03A9]',
            'rg off [\u03A9]',
            'Ts [\u00B0C]',

            'Outside Module Name',

            'P Cond. IGBT Outside [W]',
            'Psw IGBT Outside [W]',
            'Psw,on IGBT Outside [W]',
            'Psw,off IGBT Outside [W]',
            'P Total IGBT Outside [W]',

            'P Cond FWD Outside [W]',
            'Prr FWD Outside [W]',
            'P Total FWD Outside [W]',

            'Inside Module Name',

            'P Cond. IGBT Inside [W]',
            'Psw IGBT Inside [W]',
            'Psw,on IGBT Inside [W]',
            'Psw,off IGBT Inside [W]',
            'P Total IGBT Inside [W]',

            'P Cond FWD Inside [W]',
            'Prr FWD Inside [W]',
            'P Total FWD Inside [W]',

            'Diode Module Name',

            'P Cond FWD Diode [W]',
            'Prr FWD Diode [W]',
            'P Total FWD Diode [W]',

            'P Total Outside [W]',
            'P Total Inside [W]',
            'P Total Diode [W]',

            'Tcase Ave. Outside [\u00B0C]',
            'Tcase Ave. Inside [\u00B0C]',
            'Tcase Ave. Diode [\u00B0C]',

            'T\u2C7C Ave IGBT Outside [\u00B0C]',
            'ΔT\u2C7C Ave IGBT Outside [K]',
            'T\u2C7C Max IGBT Outside [\u00B0C]',
            'ΔT\u2C7C Max IGBT Outside [K]',

            'T\u2C7C Ave FWD Outside [\u00B0C]',
            'ΔT\u2C7C Ave FWD Outside [K]',
            'T\u2C7C Max FWD Outside [\u00B0C]',
            'ΔT\u2C7C Max FWD Outside [K]',

            'T\u2C7C Ave IGBT Inside [\u00B0C]',
            'ΔT\u2C7C Ave IGBT Inside [K]',
            'T\u2C7C Max IGBT Inside [\u00B0C]',
            'ΔT\u2C7C Max IGBT Inside [K]',

            'T\u2C7C Ave FWD Inside [\u00B0C]',
            'ΔT\u2C7C Ave FWD Inside [K]',
            'ΔT\u2C7C Max FWD Inside [K]',
            'T\u2C7C Max FWD Inside [\u00B0C]',

            'T\u2C7C Ave FWD Diode [\u00B0C]',
            'ΔT\u2C7C Ave FWD Diode [K]',
            'T\u2C7C Max FWD Diode [\u00B0C]',
            'ΔT\u2C7C Max FWD Diode [K]',

        ]
    else:
        return ['Module Name',
                'Modulation',
                'Vcc [V]',
                'Io [Apk]',
                'PF [cos(\u03D5)]',
                'Mod. Depth',
                'fc [kHz]',
                'fo [Hz]',
                'rg on [\u03A9]',
                'rg off [\u03A9]',
                'Ts [\u00B0C]',
                'Tcase Ave. [\u00B0C]',
                'P Total IGBT [W]',
                'P Cond IGBT [W]',
                'Psw IGBT [W]',
                'Psw,on IGBT [W]',
                'Psw,off IGBT [W]',
                'ΔT\u2C7C ave. IGBT [K]',
                'T\u2C7C ave. IGBT [\u00B0C]',
                'ΔT\u2C7C Max_IGBT [K]',
                'T\u2C7C Max IGBT [\u00B0C]',
                'P Total FWD [W]',
                'P Cond FWD [W]',
                'Prr FWD [W]',
                'ΔT\u2C7C Ave FWD [K]',
                'T\u2C7C Ave FWD [\u00B0C]',
                'ΔT\u2C7C Max FWD [K]',
                'T\u2C7C Max FWD [\u00B0C]'
                ]


def build__module_file_header():
    return ["Module Name",
            "IC - IC VCE",
            "VCE - IC VCE",
            "IF - IF VF",
            "VF - IF VF",
            "IC - IC ESWON",
            "ESWON - IC ESWON",
            "IC - IC ESWOFF",
            "ESWOFF - IC ESWOFF",
            "IC - IC ERR",
            "ERR - IC ERR",
            "ESWON - ESWON RGON",
            "RGON - ESWON RGON",
            "ESWOFF - ESWOFF RGOFF",
            "RGOFF - ESWOFF RGOFF",
            "ERR - ERR RGON",
            "RGON - ERR RGON",
            "IGBT R Values",
            "IGBT T Values",
            "FWD R Values",
            "FWD T Values",
            "IGBT RTH DC",
            "FWD RTH DC",
            "Module RTH DC",
            "Nameplate VCC",
            "Nameplate Current"
            ]


def output_worksheet_formatter(df, workbook, worksheet):
    last_col = column_number_getter(list(df)[-1])
    next_to_last_col = column_number_getter(list(df)[-1] - 1)

    format1 = workbook.add_format()
    format1.set_top(2)
    format1.set_bottom(2)
    format1.set_right(2)
    format1.set_left(2)
    format1.set_bold()

    range1 = 'A1'

    format2 = workbook.add_format()
    format2.set_top(2)
    format2.set_bottom(1)
    format2.set_right(2)
    format2.set_left(2)
    format2.set_bg_color('#d1d1d1')
    format2.set_bold()

    range2 = 'A2'
    range2a = 'A13'
    range2b = 'A18'
    range2c = 'A22'
    range2d = 'A25'
    range2e = 'A11'

    format3 = workbook.add_format()
    format3.set_top(1)
    format3.set_bottom(1)
    format3.set_right(2)
    format3.set_left(2)
    format3.set_bg_color('#d1d1d1')
    format3.set_bold()

    range3 = 'A3:A9'
    range3a = 'A14:A16'
    range3b = 'A19:A20'
    range3c = 'A23'
    range3d = 'A26:A27'

    format4 = workbook.add_format()
    format4.set_top(1)
    format4.set_bottom(2)
    format4.set_right(2)
    format4.set_left(2)
    format4.set_bg_color('#d1d1d1')
    format4.set_bold()

    range4 = 'A10'
    range4a = 'A17'
    range4b = 'A21'
    range4c = 'A24'
    range4d = 'A28'
    range4e = 'A12'

    format5 = workbook.add_format()
    format5.set_top(1)
    format5.set_bottom(1)
    format5.set_right(1)
    format5.set_left(1)

    range5 = 'C3:' + next_to_last_col + '9'
    range5a = 'C14:' + next_to_last_col + '16'
    range5b = 'C19:' + next_to_last_col + '20'
    range5c = 'C23:' + next_to_last_col + '23'
    range5d = 'C26:' + next_to_last_col + '27'

    format6 = workbook.add_format()
    format6.set_top(1)
    format6.set_bottom(1)
    format6.set_right(1)
    format6.set_left(2)

    range6 = 'B3:B9'
    range6a = 'B14:B16'
    range6b = 'B19:B20'
    range6c = 'B23'
    range6d = 'B26:B27'

    format9 = workbook.add_format()
    format9.set_top(2)
    format9.set_bottom(1)
    format9.set_right(1)
    format9.set_left(2)

    range9 = 'B2'
    range9a = 'B13'
    range9b = 'B18'
    range9c = 'B22'
    range9d = 'B25'
    range9e = 'B11'

    format10 = workbook.add_format()
    format10.set_top(2)
    format10.set_bottom(1)
    format10.set_right(1)
    format10.set_left(1)

    range10 = 'C2:' + next_to_last_col + '2'
    range10a = 'C13:' + next_to_last_col + '13'
    range10b = 'C18:' + next_to_last_col + '18'
    range10c = 'C22:' + next_to_last_col + '22'
    range10d = 'C25:' + next_to_last_col + '25'
    range10e = 'C11:' + next_to_last_col + '11'

    format15 = workbook.add_format()
    format15.set_top(2)
    format15.set_bottom(2)
    format15.set_right(2)
    format15.set_left(1)
    format15.set_bg_color('#d1d1d1')
    format15.set_bold()

    range15 = last_col + '1'

    format16 = workbook.add_format()
    format16.set_top(2)
    format16.set_bottom(2)
    format16.set_right(1)
    format16.set_left(2)
    format16.set_bg_color('#d1d1d1')
    format16.set_bold()

    range16 = 'B1'

    format17 = workbook.add_format()
    format17.set_top(2)
    format17.set_bottom(2)
    format17.set_right(1)
    format17.set_left(1)
    format17.set_bg_color('#d1d1d1')
    format17.set_bold()

    range17 = 'C1:' + next_to_last_col + '1'

    format18 = workbook.add_format()
    format18.set_top(2)
    format18.set_bottom(1)
    format18.set_right(2)
    format18.set_left(1)

    range18 = last_col + '2'
    range18a = last_col + '13'
    range18b = last_col + '18'
    range18c = last_col + '22'
    range18d = last_col + '25'
    range18e = last_col + '11'

    format19 = workbook.add_format()
    format19.set_top(1)
    format19.set_bottom(2)
    format19.set_right(1)
    format19.set_left(2)

    range19 = 'B10'
    range19a = 'B17'
    range19b = 'B21'
    range19c = 'B24'
    range19d = 'B28'
    range19e = 'B12'

    format20 = workbook.add_format()
    format20.set_top(1)
    format20.set_bottom(2)
    format20.set_right(1)
    format20.set_left(1)

    range20 = 'C10:' + next_to_last_col + '10'
    range20a = 'C17:' + next_to_last_col + '17'
    range20b = 'C21:' + next_to_last_col + '21'
    range20c = 'C24:' + next_to_last_col + '24'
    range20d = 'C28:' + next_to_last_col + '28'
    range20e = 'C12:' + next_to_last_col + '12'

    format21 = workbook.add_format()
    format21.set_top(1)
    format21.set_bottom(2)
    format21.set_right(2)
    format21.set_left(1)

    range21 = last_col + '10'
    range21a = last_col + '17'
    range21b = last_col + '21'
    range21c = last_col + '24'
    range21d = last_col + '28'
    range21e = last_col + '2'
    range21f = last_col + '12'

    format22 = workbook.add_format()
    format22.set_top(1)
    format22.set_bottom(1)
    format22.set_right(2)
    format22.set_left(1)

    range22 = last_col + '3:' + last_col + '9'
    range22a = last_col + '14:' + last_col + '16'
    range22b = last_col + '19:' + last_col + '20'
    range22c = last_col + '23'
    range22d = last_col + '26:' + last_col + '27'

    worksheet.conditional_format(range1, {'type': 'no_errors', 'format': format1})

    worksheet.conditional_format(range2, {'type': 'no_errors', 'format': format2})
    worksheet.conditional_format(range2a, {'type': 'no_errors', 'format': format2})
    worksheet.conditional_format(range2b, {'type': 'no_errors', 'format': format2})
    worksheet.conditional_format(range2c, {'type': 'no_errors', 'format': format2})
    worksheet.conditional_format(range2d, {'type': 'no_errors', 'format': format2})
    worksheet.conditional_format(range2e, {'type': 'no_errors', 'format': format2})

    worksheet.conditional_format(range3, {'type': 'no_errors', 'format': format3})
    worksheet.conditional_format(range3a, {'type': 'no_errors', 'format': format3})
    worksheet.conditional_format(range3b, {'type': 'no_errors', 'format': format3})
    worksheet.conditional_format(range3c, {'type': 'no_errors', 'format': format3})
    worksheet.conditional_format(range3d, {'type': 'no_errors', 'format': format3})

    worksheet.conditional_format(range4, {'type': 'no_errors', 'format': format4})
    worksheet.conditional_format(range4a, {'type': 'no_errors', 'format': format4})
    worksheet.conditional_format(range4b, {'type': 'no_errors', 'format': format4})
    worksheet.conditional_format(range4c, {'type': 'no_errors', 'format': format4})
    worksheet.conditional_format(range4d, {'type': 'no_errors', 'format': format4})
    worksheet.conditional_format(range4e, {'type': 'no_errors', 'format': format4})

    worksheet.conditional_format(range5, {'type': 'no_errors', 'format': format5})
    worksheet.conditional_format(range5a, {'type': 'no_errors', 'format': format5})
    worksheet.conditional_format(range5b, {'type': 'no_errors', 'format': format5})
    worksheet.conditional_format(range5c, {'type': 'no_errors', 'format': format5})
    worksheet.conditional_format(range5d, {'type': 'no_errors', 'format': format5})

    worksheet.conditional_format(range6, {'type': 'no_errors', 'format': format6})
    worksheet.conditional_format(range6a, {'type': 'no_errors', 'format': format6})
    worksheet.conditional_format(range6b, {'type': 'no_errors', 'format': format6})
    worksheet.conditional_format(range6c, {'type': 'no_errors', 'format': format6})
    worksheet.conditional_format(range6d, {'type': 'no_errors', 'format': format6})

    worksheet.conditional_format(range9, {'type': 'no_errors', 'format': format9})
    worksheet.conditional_format(range9a, {'type': 'no_errors', 'format': format9})
    worksheet.conditional_format(range9b, {'type': 'no_errors', 'format': format9})
    worksheet.conditional_format(range9c, {'type': 'no_errors', 'format': format9})
    worksheet.conditional_format(range9d, {'type': 'no_errors', 'format': format9})
    worksheet.conditional_format(range9e, {'type': 'no_errors', 'format': format9})

    worksheet.conditional_format(range10, {'type': 'no_errors', 'format': format10})
    worksheet.conditional_format(range10a, {'type': 'no_errors', 'format': format10})
    worksheet.conditional_format(range10b, {'type': 'no_errors', 'format': format10})
    worksheet.conditional_format(range10c, {'type': 'no_errors', 'format': format10})
    worksheet.conditional_format(range10d, {'type': 'no_errors', 'format': format10})
    worksheet.conditional_format(range10e, {'type': 'no_errors', 'format': format10})

    worksheet.conditional_format(range15, {'type': 'no_errors', 'format': format15})

    worksheet.conditional_format(range16, {'type': 'no_errors', 'format': format16})

    worksheet.conditional_format(range17, {'type': 'no_errors', 'format': format17})

    worksheet.conditional_format(range18, {'type': 'no_errors', 'format': format18})
    worksheet.conditional_format(range18a, {'type': 'no_errors', 'format': format18})
    worksheet.conditional_format(range18b, {'type': 'no_errors', 'format': format18})
    worksheet.conditional_format(range18c, {'type': 'no_errors', 'format': format18})
    worksheet.conditional_format(range18d, {'type': 'no_errors', 'format': format18})
    worksheet.conditional_format(range18e, {'type': 'no_errors', 'format': format18})

    worksheet.conditional_format(range19, {'type': 'no_errors', 'format': format19})
    worksheet.conditional_format(range19a, {'type': 'no_errors', 'format': format19})
    worksheet.conditional_format(range19b, {'type': 'no_errors', 'format': format19})
    worksheet.conditional_format(range19c, {'type': 'no_errors', 'format': format19})
    worksheet.conditional_format(range19d, {'type': 'no_errors', 'format': format19})
    worksheet.conditional_format(range19e, {'type': 'no_errors', 'format': format19})

    worksheet.conditional_format(range20, {'type': 'no_errors', 'format': format20})
    worksheet.conditional_format(range20a, {'type': 'no_errors', 'format': format20})
    worksheet.conditional_format(range20b, {'type': 'no_errors', 'format': format20})
    worksheet.conditional_format(range20c, {'type': 'no_errors', 'format': format20})
    worksheet.conditional_format(range20d, {'type': 'no_errors', 'format': format20})
    worksheet.conditional_format(range20e, {'type': 'no_errors', 'format': format20})

    worksheet.conditional_format(range21, {'type': 'no_errors', 'format': format21})
    worksheet.conditional_format(range21a, {'type': 'no_errors', 'format': format21})
    worksheet.conditional_format(range21b, {'type': 'no_errors', 'format': format21})
    worksheet.conditional_format(range21c, {'type': 'no_errors', 'format': format21})
    worksheet.conditional_format(range21d, {'type': 'no_errors', 'format': format21})
    worksheet.conditional_format(range21e, {'type': 'no_errors', 'format': format21})
    worksheet.conditional_format(range21f, {'type': 'no_errors', 'format': format21})

    worksheet.conditional_format(range22, {'type': 'no_errors', 'format': format22})
    worksheet.conditional_format(range22a, {'type': 'no_errors', 'format': format22})
    worksheet.conditional_format(range22b, {'type': 'no_errors', 'format': format22})
    worksheet.conditional_format(range22c, {'type': 'no_errors', 'format': format22})
    worksheet.conditional_format(range22d, {'type': 'no_errors', 'format': format22})

    center_format_left = workbook.add_format()
    center_format_left.set_align('center')
    center_format_left.set_align('vcenter')

    center_format_right = workbook.add_format()
    center_format_right.set_align('center')
    center_format_left.set_align('vcenter')

    worksheet.set_column('A:A', 16, center_format_left)
    worksheet.set_column('B:' + last_col, 21, center_format_right)
    return worksheet, workbook


def column_number_getter(col_num):  # doesn't really work right
    if col_num < 25:
        return chr(col_num + 66)
    if col_num >= 25:
        return chr(col_num // 25 + 65) + chr(col_num + 39)
