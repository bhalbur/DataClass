Attribute VB_Name = "Module4"
Sub stockscrub()

Dim t As Double
t = Timer

' this is the HARD version of the homework

Dim firstrow, lastrow, rownum As Long
Dim printrow, printcol As Integer
Dim volsum, first, last, lowgrow, highgrow, highvol, growth As Double
Dim lowgrtick, highgrtick, highvoltick As String

Dim pagenum As Integer
Dim lastpage As Integer

lastpage = ActiveWorkbook.Sheets.Count

For pagenum = 1 To lastpage
ActiveWorkbook.Sheets(pagenum).Activate

firstrow = 2
lastrow = ActiveSheet.UsedRange.Rows.Count + 1
rownum = firstrow
printrow = 2
printcol = 9
volsum = 0
lowgrow = 99
highgrow = -99
highvol = 0
lowgrtick = ""
highgrtick = ""
highvoltick = ""


For rownum = firstrow To lastrow
    volsum = volsum + Cells(rownum, 7).Value
    If Cells(rownum, 1).Value <> Cells(rownum - 1, 1).Value Then first = Cells(rownum, 3).Value
    If first = 0 Then GoTo ZeroVal
ResumeLoop:
        If Cells(rownum, 1).Value = Cells(rownum + 1, 1).Value Then
            Else
                last = Cells(rownum, 6).Value
                Cells(printrow, printcol).Value = Cells(rownum, 1).Value
                Cells(printrow, printcol + 1).Value = last - first
                    If first = 0 Then
                        growth = 0
                    Else: growth = (last / first) - 1
                    End If
                    Cells(printrow, printcol + 2).Value = growth
                    Cells(printrow, printcol + 3).Value = volsum
                If growth > 0 Then
                    Cells(printrow, printcol + 2).Interior.Color = RGB(0, 200, 0)
                    Else: Cells(printrow, printcol + 2).Interior.Color = RGB(200, 0, 0)
                End If
                    If growth - 1 < lowgrow Then
                        lowgrow = growth
                        lowgrtick = Cells(rownum, 1).Value
                    End If
                    If growth > highgrow Then
                        highgrow = growth
                        highgrtick = Cells(rownum, 1).Value
                    End If
                    If volsum > highvol Then
                        highvol = volsum
                        highvoltick = Cells(rownum, 1).Value
                    End If
                printrow = printrow + 1
                volsum = 0
                End If
Next

ZeroVal:
    For rownum = rownum To lastrow
    If Cells(rownum, 1).Value <> Cells(rownum - 1, 1).Value And Cells(rownum, 3).Value = 0 Then
    Else
        first = Cells(rownum, 3).Value
        GoTo ResumeLoop
    End If
    Next
    
    
Range("J:J").Style = "Currency"
Range("K:K").NumberFormat = "0.0%"
Range("L:L").NumberFormat = "0,000"

Range("I1").Value = "Ticker"
Range("J1").Value = "Year Change"
Range("K1").Value = "% Change"
Range("L1").Value = "Total Volume"
Range("O1").Value = "Ticker"
Range("P1").Value = "Value"

Cells(2, 14) = "Biggest Gainer"
Cells(3, 14) = "Biggest Loser"
Cells(4, 14) = "Highest Volume"
Cells(2, 15) = highgrtick
Cells(3, 15) = lowgrtick
Cells(4, 15) = highvoltick
Cells(2, 16) = highgrow
Cells(3, 16) = lowgrow
Cells(4, 16) = highvol
Cells(2, 16).NumberFormat = "0.0%"
Cells(3, 16).NumberFormat = "0.0%"
Cells(4, 16).NumberFormat = "0,000"

Range("I:P").Columns.AutoFit

Next


MsgBox ("Execution completed in " & Round(Timer - t, 1) & " seconds")

End Sub

Sub reset()

Dim lastpage As Integer
lastpage = ActiveWorkbook.Sheets.Count

For pagenum = 1 To lastpage
ActiveWorkbook.Sheets(pagenum).Activate
Range("I:P").Delete
Next

End Sub
