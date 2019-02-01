import os
from time import strftime

import xlsxwriter
from numpy import ndarray, append
from pandas import DataFrame, ExcelWriter, Series


def output_file_three_level_writer(output_file, output_file_directory):
    columns = ['Modulation',
               'Vcc [V]',
               'Io [Apk]',
               'PF [cos(\u03D5)]',
               'Mod. Depth',
               'fc [kHz]',
               'fo [Hz]',
               'Ts [\u00B0C]',
               'rg on Outside [\u03A9]',
               'rg off Outside [\u03A9]',
               'rg on Inside [\u03A9]',
               'rg off Inside [\u03A9]',
               'Outside Module Name',
               'P Cond. IGBT Outside [W]',
               'Psw IGBT Outside [W]',
               'Psw,on IGBT Outside [W]',
               'Psw,off IGBT Outside [W]',
               'P Total IGBT Outside [W]',
               'P Cond FWD Outside [W]',
               'Prr FWD Outside [W]',
               'P Total FWD Outside [W]',
               'P Total Outside [W]',
               'Tc Ave Outside [\u00B0C]',
               'ΔT\u2C7C Ave IGBT Outside [K]',
               'T\u2C7C Ave IGBT Outside [\u00B0C]',
               'ΔT\u2C7C Max IGBT Outside [K]',
               'T\u2C7C Max IGBT Outside [\u00B0C]',
               'ΔT\u2C7C Ave FWD Outside [K]',
               'T\u2C7C Ave FWD Outside [\u00B0C]',
               'ΔT\u2C7C Max FWD Outside [K]',
               'T\u2C7C Max FWD Outside [\u00B0C]',
               'Inside Module Name',
               'P Cond. IGBT Inside [W]',
               'Psw IGBT Inside [W]',
               'Psw,on IGBT Inside [W]',
               'Psw,off IGBT Inside [W]',
               'P Total IGBT Inside [W]',
               'P Cond FWD Inside [W]',
               'Prr FWD Inside [W]',
               'P Total FWD Inside [W]',
               'P Total Inside [W]',
               'Tc Ave Inside [\u00B0C]',
               'ΔT\u2C7C Ave IGBT Inside [K]',
               'T\u2C7C Ave IGBT Inside [\u00B0C]',
               'ΔT\u2C7C Max IGBT Inside [K]',
               'T\u2C7C Max IGBT Inside [\u00B0C]',
               'ΔT\u2C7C Ave FWD Inside [K]',
               'T\u2C7C Ave FWD Inside [\u00B0C]',
               'ΔT\u2C7C Max FWD Inside [K]',
               'T\u2C7C Max FWD Inside [\u00B0C]',
               'Diode Module Name',
               'P Cond FWD Diode [W]',
               'Prr FWD Diode [W]',
               'P Total FWD Diode [W]',
               'P Total Diode [W]',
               'Tc Ave Diode [\u00B0C]',
               'ΔT\u2C7C Ave FWD Diode [K]',
               'T\u2C7C Ave FWD Diode [\u00B0C]',
               'ΔT\u2C7C Max FWD Diode [K]',
               'T\u2C7C Max FWD Diode [\u00B0C]'
               ]
    if output_file_directory is None:
        output_file_directory = os.getcwd()
    output_file_name = output_file_directory + '/output' + strftime("__%b_%d__%H_%M_%S") + '.xlsx'
    df = DataFrame(dict([(k, Series(v)) for k, v in output_file.items()]), columns=columns).T
    df.reset_index(level=0, inplace=True)
    xl_writer = ExcelWriter(output_file_name, engine='xlsxwriter', options={'strings_to_numbers': True})
    workbook = xl_writer.book
    df.to_excel(xl_writer, index=False, header=False)
    worksheet = xl_writer.sheets['Sheet1']
    # worksheet, workbook = output_worksheet_formatter(df, workbook, worksheet) #todo fix output formatter
    xl_writer.save()

    f = open(output_file_name)
    f.close()


def output_file_wrangler(output_file_a, output_file_b):  # todo what was this needed for
    if type(output_file_b['Vcc [V]']) is ndarray:
        for key in output_file_b.keys():
            if key in output_file_a.keys():
                output_file_b[key] = append(output_file_b[key], output_file_a[key])
        full_file_dict = output_file_b
    else:
        full_file_dict = output_file_b
    return full_file_dict


def get_col_widths(dataframe):  # todo fix this
    # First we find the maximum length of the index column
    idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
    # Then, we concatenate this to the max of the lengths of column name and its values for each column, left to right
    return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]


def make__two_level_template(file_location):
    row_list = [['Vcc [V]',
                 'Io [Apk]',
                 'PF [cos(\u03D5)]',
                 'Mod. Depth',
                 'fc [kHz]',
                 'fo [Hz]',
                 'rg on [\u03A9]',
                 'rg off [\u03A9]',
                 'Ts [\u00B0C]'
                 ]]
    workbook = xlsxwriter.Workbook(file_location + '/input_file_two_level_template.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:A', 20)
    row_list_map = row_list[0]
    worksheet.write(0, 0, "Iteration")
    worksheet.write(0, 1, "1")
    worksheet.write(0, 2, "3")
    worksheet.write(0, 3, "3")
    for x in range(len(row_list_map)):
        worksheet.write(0, x + 1, row_list_map[x])
    workbook.close()


def make__three_level_template(file_location):
    row_list = [['Vcc [V]',
                 'Io [Apk]',
                 'PF [cos(\u03D5)]',
                 'Mod. Depth',
                 'fc [kHz]',
                 'fo [Hz]',
                 'Inside rg on [\u03A9]',
                 'Inside rg off [\u03A9]',
                 'Outside rg on [\u03A9]',
                 'Outside rg off [\u03A9]',
                 'Ts [\u00B0C]'
                 ]]
    workbook = xlsxwriter.Workbook(file_location + '/input_file__three_level_template.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:A', 20)
    row_list_map = row_list[0]
    worksheet.write(0, 0, "Iteration")
    worksheet.write(0, 1, "1")
    worksheet.write(0, 2, "3")
    worksheet.write(0, 3, "3")
    for x in range(len(row_list_map)):
        worksheet.write(0, x + 1, row_list_map[x])
    workbook.close()


def make__six_step_template(file_location):
    row_list = [['Vcc [V]',
                 'Io [Apk]',
                 'Duty',
                 'fc [kHz]',
                 'fo [Hz]',
                 'Upper rg on [\u03A9]',
                 'Upper rg off [\u03A9]',
                 'Lower rg on [\u03A9]',
                 'Lower rg off [\u03A9]',
                 'Ts [\u00B0C]'
                 ]]
    workbook = xlsxwriter.Workbook(file_location + '/input_file__six_step_template.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:A', 20)
    row_list_map = row_list[0]
    worksheet.write(0, 0, "Iteration")
    worksheet.write(0, 1, "1")
    worksheet.write(0, 2, "3")
    worksheet.write(0, 3, "3")
    for x in range(len(row_list_map)):
        worksheet.write(0, x + 1, row_list_map[x])
    workbook.close()


def make__chopper_template(file_location):
    row_list = [['V_in [V]',
                 'V_out [V]',
                 'Io [Apk]',
                 'Duty',
                 'fc [kHz]',
                 'rg on [\u03A9]',
                 'rg off [\u03A9]',
                 'Ts [\u00B0C]'
                 ]]
    workbook = xlsxwriter.Workbook(file_location + '/input_file__chopper_template.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:A', 20)
    row_list_map = row_list[0]
    worksheet.write(0, 0, "Iteration")
    worksheet.write(0, 1, "1")
    worksheet.write(0, 2, "3")
    worksheet.write(0, 3, "3")
    for x in range(len(row_list_map)):
        worksheet.write(0, x + 1, row_list_map[x])
    workbook.close()


def make__motor_lock_template(file_location):
    row_list = [['Vcc [V]',
                 'Io [Apk]',
                 'Duty',
                 'fc [kHz]',
                 'rg on [\u03A9]',
                 'rg off [\u03A9]',
                 'Ts [\u00B0C]'
                 ]]
    workbook = xlsxwriter.Workbook(file_location + '/input_file__motor_lock_template.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:A', 20)
    row_list_map = row_list[0]
    worksheet.write(0, 0, "Iteration")
    worksheet.write(0, 1, "1")
    worksheet.write(0, 2, "3")
    worksheet.write(0, 3, "3")
    for x in range(len(row_list_map)):
        worksheet.write(0, x + 1, row_list_map[x])
    workbook.close()


def module_file_template_maker(file_location):
    row_list = [["Module Name",
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
                 ]]
    workbook = xlsxwriter.Workbook(file_location + '/module_file_template.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:A', 20)
    row_list_map = row_list[0]
    for x in range(len(row_list_map)):
        worksheet.write(0, x + 1, row_list_map[x])
    workbook.close()
