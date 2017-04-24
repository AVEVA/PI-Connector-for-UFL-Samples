#*********************************************************************************
# Copyright © 2016-2017 OSIsoft, LLC All rights reserved.
# THIS SOFTWARE CONTAINS CONFIDENTIAL INFORMATION AND TRADE SECRETS OF
# OSIsoft, LLC  USE, DISCLOSURE, OR REPRODUCTION IS PROHIBITED WITHOUT
# THE PRIOR EXPRESSED WRITTEN PERMISSION OF OSIsoft, LLC
# RESTRICTED RIGHTS LEGEND
# Use, duplication, or disclosure by the Government is subject to restrictions
# as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and
# Computer Software clause at DFARS 252.227.7013
# OSIsoft, LLC
# 1600 Alvarado Street, San Leandro CA 94577
#*********************************************************************************


# =========================================================================================================================================================================================================
# Process script parameters
# Usage:
#    putExample.ps1 -URL <host> -Data <data> -UserName <RestAuthUser> -Password <RestAuthPassword> 
# Example:
#    putExample.ps1 -URL https://localhost:5460/connectordata/rest/ -Data "point1;01/01/2016 10:10:10;10" -UserName admin -Password adminadmin
#

param(
[string]$URL = "",
[string]$FilePath = "",
[string]$Data = "",
[string]$UserName = "",
[string]$Password = ""
)

Function Print-Help{
	write-host "
	This script sends data to your UFL Rest endpoint.
	---------------------------------------------------
	You must specify:
	-URL {REST endpoint url}
	
	Source of data (one of them):
	-Data {data in a string form}
	-FilePath {path to a data file}

	In case of the enabled authentication:
	-UserName {userName}
	-Password {password}

	Example:
	putExample.ps1 -URL https://localhost:5460/connectordata/rest/ -Data ""point1;01/01/2016 10:10:10;10"" -UserName admin -Password adminadmin
	putExample.ps1 -URL https://localhost:5460/connectordata/rest/ -FilePath ""c:\temp\a.dat""
	---------------------------------------------------
	"

    write-host
}

Function Send-Data{
    Try{
	    write-host "****** Sending data to the $URL endpoint *****" -ForegroundColor Green
	    $result = Invoke-RestMethod -Method PUT -Uri "$URL" -Body $dataBytes -Headers $Headers
	    write-host "****** Success: $result ******" -ForegroundColor Green
        return $true
    }Catch
    {
        Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__ -ForegroundColor Red
	    write-host "****** Sending data failed. Reason: $_ ******" -ForegroundColor Red
        return $false
    }
    write-host
    Send-Data
    # Read-Host -Prompt "Press Enter to exit..."
}


If ([string]::IsNullOrEmpty($URL))
{
    Print-Help
    Write-Host "URL parameter must be specified. Please see the instructions above." -ForegroundColor Red	
    Read-Host -Prompt "Press Enter to exit."
	Exit
}

if([string]::IsNullOrEmpty($Data) -and [string]::IsNullOrEmpty($Filepath))
{
    Print-Help
    Write-Host "Filepath or Data parameter must be specified. Please see the instructions above." -ForegroundColor Red	
    Read-Host -Prompt "Press Enter to exit."
	Exit
}

If (![string]::IsNullOrEmpty($FilePath)) 
{
	If (Test-Path $FilePath)
	{
		write-host "file"
		$Data = [IO.File]::ReadAllText($FilePath)
	}
	else
	{
		Write-Host "Wrong FilePath or the file does not exist" -ForegroundColor Red
	}
}

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
$dataBytes = [System.Text.Encoding]::UTF8.GetBytes($Data)   

If (![string]::IsNullOrEmpty($Password))
{
	if([string]::IsNullOrEmpty($UserName))
	{
        Print-Help
        Write-Host "UserName parameter must be specified. Please see the instructions above." -ForegroundColor Red		
        Read-Host -Prompt "Press Enter to exit."
	    Exit
		
	}
	$encodedCreds = [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes("$($UserName):$($Password)"))
	$basicAuthValue = "Basic $encodedCreds"
	$headers = @{
		Authorization = $basicAuthValue
	}
}

# The script keeps sending data every 500ms until success
Do {
	 $res = Send-Data
	 Start-Sleep -m 500 
	} while($res -eq $false)