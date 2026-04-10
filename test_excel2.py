import openpyxl
wb = openpyxl.load_workbook('C:/s/Sistema/wiao/wioa/WIOA/Tabla - AMSI - Original - 5enero2026.xlsx', data_only=True, read_only=True)
print("Sheet names:", wb.sheetnames)
