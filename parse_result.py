import json
import xlsxwriter
import datetime
import re
from get_result import region

date_for_file = datetime.date

if region == 55:
    path = 'result/fssp-OMSK-{}.json'.format(
        date_for_file.today().strftime('%d.%m.%Y'))
else:
    path = 'result/fssp-VLD-{}.json'.format(
        date_for_file.today().strftime('%d.%m.%Y'))


with open(path, 'r') as f:
    data = json.load(f)

# List of dicts from JSON
result_dicts = data['response']['result'][0]['result']

# Creates a excel book
if region == 55:
    workbook = xlsxwriter.Workbook(
        'result/result-OMSK-{}.xlsx'.format(date_for_file.today().strftime('%d.%m.%Y')))
else:
    workbook = xlsxwriter.Workbook(
        'result/result-VLD-{}.xlsx'.format(date_for_file.today().strftime('%d.%m.%Y')))
worksheet = workbook.add_worksheet()
worksheet.set_column('A:D', 30)


# Creates format for columns
bold_text = workbook.add_format({'bold': 1})
date_format = workbook.add_format({'num_format': 'dd.mm.yyyy'})
money_format = workbook.add_format({'num_format': '# ##0'})

# Creates sheet Headers
worksheet.write('A1', 'Дата ИП', bold_text)
worksheet.write('B1', 'Номер ИЛ', bold_text)
worksheet.write('C1', 'Сумма ИЛ', bold_text)
worksheet.write('D1', 'Дата выгрузки', bold_text)

row, col = 1, 0

# Recording data on enforcement proceedings in the book
for i in range(len(result_dicts)):
    exe_production = result_dicts[i]['exe_production']
    exe_production_result = re.findall(r'\d\d.\d\d.\d{4}', exe_production)
    print(exe_production_result)
    if len(exe_production_result) == 1:
        worksheet.write_string(row, col, exe_production_result[0])
    else:
        worksheet.write_string(row, col, exe_production_result[1])
    details = result_dicts[i]['details']
    details_result = re.findall(r'от \d+.{8}\D+\d+', details)
    worksheet.write_string(row, col + 1, details_result[0])
    subject = result_dicts[i]['subject']
    subject_result = re.findall(r'\d+\.\d+', subject)  # Search sum in string
    if subject_result != []:
        worksheet.write(row, col + 2, float(subject_result[0]))
    else:
        worksheet.write(row, col + 2, 'none')
    date = datetime.date
    worksheet.write_datetime(row, col + 3, date.today(), date_format)
    row += 1

workbook.close()
