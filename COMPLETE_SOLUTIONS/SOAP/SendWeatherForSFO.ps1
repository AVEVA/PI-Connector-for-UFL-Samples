<#
   Copyright 2016 OSIsoft, LLC.
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
#>

param([Parameter(Mandatory=$true)][string]$url, [string]$username = "", [string]$password = "")

# How to call the script .\SendWeatherForSFO.ps1 -url https://JLEFEBVRENEW:5460/connectordata/RESTWeather/ -userName john -password p@ssw0rd!

# Getting data from a public endpoint
# By sending a POST request to http://www.webservicex.net/globalweather.asmx
# That contains the SOAP body: 
# <soap:Body><GetWeather xmlns="http://www.webserviceX.NET"><CityName>San Francisco</CityName><CountryName>United States</CountryName></GetWeather></soap:Body>
$weather = New-WebServiceProxy 'http://www.webservicex.net/globalweather.asmx?WSDL'
$data = $weather.GetWeather('San Francisco','United States')
Write-Host "Data about to be sent:"
Write-Host $data

# Required to ignore issues with self-signed certificates.
# Please remove if using a trusted certficated
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
$encodedCreds = [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes("$($userName):$($password)"))
$basicAuthValue = "Basic $encodedCreds"
$headers = @{ Authorization = $basicAuthValue }

Try {
	Write-Host "****** Sending data to the $URL endpoint *****" -ForegroundColor DarkGreen
	# Using PUT HTTP request for sending data to the PI Connector for UFL REST endpoint
	$result = Invoke-RestMethod -Method PUT -Uri "$URL" -Body $dataBytes -Headers $Headers
	Write-Host "****** Success: $result ******" -ForegroundColor DarkGreen
}
Catch {
	write-host "****** Sending data has failed. Reason: $_ ******" -ForegroundColor Red
}
Write-Host "See the PI Connectors windows event logs on the PI connector for UFL machine for futher details on the request."
Write-Host
Read-Host -Prompt "Press Enter to exit"