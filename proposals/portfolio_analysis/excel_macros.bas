Attribute VB_Name = "PortfolioAnalysis"
Sub CreateInvestmentSheets()
    Dim wsSrc As Worksheet
    Dim wsInv As Worksheet
    Dim lastRow As Long
    Dim startDate As String, endDate As String
    Dim investment As Double
    Dim i As Long
    Dim invRow As Long
    
    ' Create or clear investment sheet
    On Error Resume Next
    Set wsInv = ThisWorkbook.Sheets("investment")
    If wsInv Is Nothing Then
        Set wsInv = ThisWorkbook.Sheets.Add
        wsInv.Name = "investment"
    Else
        wsInv.Cells.Clear
    End If
    On Error GoTo 0
    
    ' Set investment budget
    investment = 100000
    
    ' Write headers
    wsInv.Rows(1).Font.Bold = True
    wsInv.Range("A1").Value = "Investment and %"
    wsInv.Range("B1").Value = "Shares Name"
    wsInv.Range("C1").Value = "Start Date"
    wsInv.Range("D1").Value = "End Date"
    wsInv.Range("E1").Value = "Buy Price Per Share"
    wsInv.Range("F1").Value = "Sell Price Per Share"
    wsInv.Range("G1").Value = "Purchase Total"
    wsInv.Range("H1").Value = "Proceeds From Sale"
    wsInv.Range("I1").Value = "Gain/Loss = (Proceeds - Purchase)"
    wsInv.Range("J1").Value = "Gain/Loss %"
    wsInv.Columns("A:I").ColumnWidth = 15
    
    invRow = 2
    ' invested money - whole sum
    wsInv.Cells(invRow, 1).Value = investment
    wsInv.Rows(invRow).Font.Bold = True
    invRow = invRow + 1
    
    ' Loop through all sheets
    For Each wsSrc In ThisWorkbook.Sheets
        If wsSrc.Name <> wsInv.Name Then
            
            ' Find last row in source sheet
            lastRow = wsSrc.Cells(wsSrc.Rows.Count, "A").End(xlUp).Row
            
            ' Get start and end dates
            startDate = wsSrc.Cells(2, 1).Value
            endDate = wsSrc.Cells(lastRow, 1).Value
            
            ' Write values
            wsInv.Cells(invRow, 1).Value = "=1/" & (ThisWorkbook.Sheets.Count - 1)
            wsInv.Cells(invRow, 1).NumberFormat = "0.00%"
            
            wsInv.Cells(invRow, 2).Value = wsSrc.Name
            wsInv.Cells(invRow, 3).Value = startDate
            wsInv.Cells(invRow, 4).Value = endDate
            
            ' Formulas referencing the source sheet
            wsInv.Cells(invRow, 5).Formula = "=VLOOKUP(TEXT(C" & invRow & ",""yyyy-mm-dd"")," & wsSrc.Name & "!A:F,2,FALSE)"
            wsInv.Cells(invRow, 6).Formula = "=VLOOKUP(TEXT(D" & invRow & ",""yyyy-mm-dd"")," & wsSrc.Name & "!A:F,2,FALSE)"
            ' (invested money * %) / share price
            wsInv.Cells(invRow, 7).Formula = "=(A2 * A" & invRow & ")/E" & invRow
            wsInv.Cells(invRow, 8).Formula = "=G" & invRow & "*F" & invRow
            wsInv.Cells(invRow, 9).Formula = "=H" & invRow & "- A2 * A" & invRow
            
            wsInv.Cells(invRow, 10).Formula = "=I" & invRow & " / A2"
            wsInv.Cells(invRow, 10).NumberFormat = "0.00%"
            
            
            invRow = invRow + 1
        End If
    Next wsSrc
    
    ' Total line (H, I, J) columns
    wsInv.Rows(invRow).Font.Bold = True
    wsInv.Cells(invRow, 8).Value = "Total Gain"
    wsInv.Cells(invRow, 9).Formula = "=SUM(I2:I" & (invRow - 1) & ")"
    wsInv.Cells(invRow, 10).Formula = "=I" & invRow & " / A2"
    wsInv.Cells(invRow, 10).NumberFormat = "0.00%"
    
    wsInv.Rows(invRow + 1).Font.Bold = True
    wsInv.Cells(invRow + 1, 8).Value = "Total Sum"
    wsInv.Cells(invRow + 1, 9).Formula = "=A2 + I" & invRow
    
    ' Color into yellow
    wsInv.Range("A1:A" & (invRow - 1)).Interior.Color = RGB(255, 255, 0)
    wsInv.Range("H" & (invRow) & ":I" & (invRow + 1)).Interior.Color = RGB(255, 255, 0)
    
    ' Apply borders
    With wsInv.Range("A1:J" & invRow).Borders
        .LineStyle = xlContinuous
        .Weight = xlThin
        .Color = vbBlack
    End With
    
    ' Add historical data
    CreateCombinedChart "investment", 15 * (invRow + 1)
    
End Sub

Sub CreateCombinedChart(destSheetName As String, top As Integer)
    Dim wsInv As Worksheet
    Dim wsSrc As Worksheet
    Dim chartObj As ChartObject
    Dim lastRow As Long
    Dim seriesCount As Long
    
    Set wsInv = ThisWorkbook.Sheets(destSheetName)
    
    ' Add chart object
    Set chartObj = wsInv.ChartObjects.Add(left:=10, top:=top, width:=800, height:=300)
    chartObj.Chart.ChartType = xlLine
    chartObj.Chart.HasTitle = True
    chartObj.Chart.ChartTitle.Text = "Open Price Per Share (Historical Data)"
    
    seriesCount = 0
    
    ' Loop through all sheets
    For Each wsSrc In ThisWorkbook.Sheets
        If wsSrc.Name <> wsInv.Name Then
            ' Find last row in source sheet
            lastRow = wsSrc.Cells(wsSrc.Rows.Count, "A").End(xlUp).Row
            
            ' Add series from this sheet
            chartObj.Chart.SeriesCollection.NewSeries
            chartObj.Chart.SeriesCollection(seriesCount + 1).Name = wsSrc.Name
            chartObj.Chart.SeriesCollection(seriesCount + 1).XValues = wsSrc.Range("A2:A" & lastRow)   ' Dates
            chartObj.Chart.SeriesCollection(seriesCount + 1).Values = wsSrc.Range("B2:B" & lastRow)   ' Open price
            seriesCount = seriesCount + 1
        End If
    Next wsSrc
End Sub
