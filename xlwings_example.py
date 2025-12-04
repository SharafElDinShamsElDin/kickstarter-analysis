import xlwings as xw
import numpy as np
import pandas as pd

# Example: Connect xlwings with your Kickstarter analysis project

# Method 1: Read data from Excel
def read_data_from_excel(file_path):
    """Read Kickstarter data from Excel file"""
    sht = xw.Book(file_path).sheets[0]
    data = sht.used_range.value
    return pd.DataFrame(data[1:], columns=data[0])

# Method 2: Write results to Excel
def write_results_to_excel(df, output_file):
    """Write analysis results to Excel file"""
    wb = xw.Book()
    sht = wb.sheets[0]
    sht.range('A1').value = df
    wb.save(output_file)
    wb.close()

# Example usage:
if __name__ == "__main__":
    # Create a new workbook
    wb = xw.Book()
    sht = wb.sheets[0]
    
    # Write sample data
    sht.range('A1').value = 'Sample Data'
    sht.range('A2').value = np.random.rand(5, 5)
    
    print("xlwings is successfully integrated with your project!")
    print("You can now:")
    print("- Read data from Excel files")
    print("- Write analysis results to Excel")
    print("- Automate Excel tasks with Python")
