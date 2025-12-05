' VBA module to import into the .xlsm workbook
' Edit the path in the RunPython string to point to your project folder

Sub GetPrediction()
    ' Adjust the project path below to the full path where your project .py files live
    RunPython "import sys; sys.path.append(r'/Users/emkanlaptop/Desktop/model'); from excel_integration import vba_predict; vba_predict('artifacts')"
End Sub
