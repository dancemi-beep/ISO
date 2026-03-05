import openpyxl

excel_file = "files/IS-004-01資產及風險評鑑表.xlsx"
wb = openpyxl.load_workbook(excel_file, data_only=True)
sheet = wb["資產及風險評鑑表"]

print("--- Data Dump Rows 3-6 (Col 1-25) ---")
for r in range(3, 7):
    row_data = []
    for c in range(1, 26):
        val = sheet.cell(row=r, column=c).value
        # clean up newlines for printing
        if isinstance(val, str):
            val = val.replace('\n', ' ')
        row_data.append(val)
    print(f"Row {r}: {row_data}")
