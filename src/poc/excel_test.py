import sys
print(f"Python path: {sys.executable}")
print("Trying to import openpyxl...")
try:
    import openpyxl
    import os
    
    excel_file = "files/IS-004-01資產及風險評鑑表.xlsx"
    output_file = "output/IS-004-01_processed.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"Error: Could not find {excel_file}")
        sys.exit(1)
        
    print(f"Loading workbook: {excel_file}")
    wb = openpyxl.load_workbook(excel_file)
    print(f"Sheet names: {wb.sheetnames}")
    
    sheet = wb.active
    print(f"Active sheet: {sheet.title}")
    
    # Just a simple test: update a cell to prove we can read/write
    # We will expand this to actual risk logic later based on the sheet structure
    sheet['A1'] = f"Updated by Engine: {sheet['A1'].value if sheet['A1'].value else ''}"
    
    # Check what's around row 1-5 to understand headers
    for i in range(1, 6):
        row_vals = [str(cell.value) for cell in sheet[i][:5]]
        print(f"Row {i}: {row_vals}")
        
    wb.save(output_file)
    print(f"Successfully saved to {output_file}")
    
except Exception as e:
    print(f"Error: {e}")
