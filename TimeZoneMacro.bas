Attribute VB_Name = "Module1"
Function FetchTZ(qLat As Double, qLong As Double) As String

    Dim JSON_content As String
    Dim IANAtz As String
    Dim temp_l As Long
    Dim XMLobj As Object
    Dim qURL As String
    Dim CheckCountry As String
    
    temp_l = 0
    JSON_content = vbNullString
    IANAtz = vbNullString
    
        
    qURL = "http://api.geonames.org/timezoneJSON?lat=" & qLat & "&lng=" & qLong & "&username=enmayordomo"
    
    
    Set XMLobj = CreateObject("MSXML2.ServerXMLHTTP.3.0")
    With XMLobj
        .Open "GET", qURL, False
        .send
        JSON_content = .responseText
    End With
    Set XMLobj = Nothing
            
    
    temp_l = InStr(1, JSON_content, "timezoneId")
    IANAtz = Mid(JSON_content, (temp_l + 13), ((InStr(temp_l, JSON_content, ",") - 1) - (temp_l + 13)))
    IANAtz = Replace(IANAtz, "\/", "/")
    FetchTZ = IANAtz

End Function

Sub TimeZone()

End Sub
