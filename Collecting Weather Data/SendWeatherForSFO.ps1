#*********************************************************************************
# Copyright © 2016 OSIsoft, LLC All rights reserved.
# THIS SOFTWARE CONTAINS CONFIDENTIAL INFORMATION AND TRADE SECRETS OF
# OSIsoft, LLC  USE, DISCLOSURE, OR REPRODUCTION IS PROHIBITED WITHOUT
# THE PRIOR EXPRESSED WRITTEN PERMISSION OF OSIsoft, LLC
# RESTRICTED RIGHTS LEGEND
# Use, duplication, or disclosure by the Government is subject to restrictions
# as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and
# Computer Software clause at DFARS 252.227.7013
# OSIsoft, LLC
# 777 Davis Street, Suite 250, San Leandro CA 94577
#*********************************************************************************

# PI Connector for UFL REST endpoint data
$URL = "https://W2012HRMSERVER:5462/connectordata/RESTWeather/" 
$UserName = "user"
$Password = "password"

# Getting data from a public endpoint
$weather = New-WebServiceProxy 'http://www.webservicex.net/globalweather.asmx?WSDL'
$data = $weather.GetWeather('San Francisco','United States')
print($data)

add-type @"
	using System.Net;
	using System.Security.Cryptography.X509Certificates;
	public class TrustAllCertsPolicy : ICertificatePolicy {
		public bool CheckValidationResult(
			ServicePoint srvPoint, X509Certificate certificate,
			WebRequest request, int certificateProblem) {
			return true;
		}
	}
"@
[System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy

# Data needs to be converted to bytes and send in a body
$dataBytes = [System.Text.Encoding]::UTF8.GetBytes($Data)   
$encodedCreds = [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes("$($UserName):$($Password)"))
$basicAuthValue = "Basic $encodedCreds"
$headers = @{
	Authorization = $basicAuthValue
	}

Try{
	write-host "****** Sending data to the $URL endpoint *****" -ForegroundColor DarkGreen
	# Using PUT HTTP request for sending data to the PI Connector for UFL REST endpoint
	$result = Invoke-RestMethod -Method PUT -Uri "$URL" -Body $dataBytes -Headers $Headers
	write-host "****** Success: $result ******" -ForegroundColor DarkGreen
}Catch
{
	write-host "****** Sending data failed. Reason: $_ ******" -ForegroundColor Red
}
write-host
Read-Host -Prompt "Press Enter to exit..."