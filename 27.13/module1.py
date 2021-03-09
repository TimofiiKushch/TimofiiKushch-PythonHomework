import openpyxl

wb = openpyxl.load_workbook("data/passengers.xlsx")
ws = wb.active
print([row[0].value for row in ws.rows if len(row) == 3])