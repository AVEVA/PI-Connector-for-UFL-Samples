function Unzip-File {

<#
.SYNOPSIS
   Unzip-File is a function which extracts the contents of a zip file.

.DESCRIPTION
   Unzip-File is a function which extracts the contents of a zip file specified via the -File parameter to the
location specified via the -Destination parameter. This function first checks to see if the .NET Framework 4.5
is installed and uses it for the unzipping process, otherwise COM is used.

.PARAMETER File
    The complete path and name of the zip file in this format: C:\zipfiles\myzipfile.zip 
 
.PARAMETER Destination
    The destination folder to extract the contents of the zip file to. If a path is no specified, the current path
is used.

.PARAMETER ForceCOM
    Switch parameter to force the use of COM for the extraction even if the .NET Framework 4.5 is present.

.EXAMPLE
   Unzip-File -File C:\zipfiles\AdventureWorks2012_Database.zip -Destination C:\databases\

.EXAMPLE
   Unzip-File -File C:\zipfiles\AdventureWorks2012_Database.zip -Destination C:\databases\ -ForceCOM

.EXAMPLE
   'C:\zipfiles\AdventureWorks2012_Database.zip' | Unzip-File

.EXAMPLE
    Get-ChildItem -Path C:\zipfiles | ForEach-Object {$_.fullname | Unzip-File -Destination C:\databases}

.INPUTS
   String

.OUTPUTS
   None

.NOTES
   Author:  Mike F Robbins
   Website: http://mikefrobbins.com
   Twitter: @mikefrobbins

#>



    [CmdletBinding()]



    param (
        [Parameter(Mandatory=$true, 
                   ValueFromPipeline=$true)]
        [ValidateScript({
            If ((Test-Path -Path $_ -PathType Leaf) -and ($_ -like "*.zip")) {
                $true
            }
            else {
                Throw "$_ is not a valid zip file. Enter in 'C:\TempData\all_xml.zip' format"
            }
        })]
        [string]$File,

        [ValidateNotNullOrEmpty()]
        [ValidateScript({
            If (Test-Path -Path $_ -PathType Container) {
                $true
            }
            else {
                Throw "$_ is not a valid destination folder. Enter in 'C:\TempData\WeatherData' format"
            }
        })]
        [string]$Destination = (Get-Location).Path,

        [switch]$ForceCOM
    )


    If (-not $ForceCOM -and ($PSVersionTable.PSVersion.Major -ge 3) -and
       ((Get-ItemProperty -Path "HKLM:\Software\Microsoft\NET Framework Setup\NDP\v4\Full" -ErrorAction SilentlyContinue).Version -like "4.5*" -or
       (Get-ItemProperty -Path "HKLM:\Software\Microsoft\NET Framework Setup\NDP\v4\Client" -ErrorAction SilentlyContinue).Version -like "4.5*")) {

        Write-Verbose -Message "Attempting to Unzip $File to location $Destination using .NET 4.5"

        try {
            [System.Reflection.Assembly]::LoadWithPartialName("System.IO.Compression.FileSystem") | Out-Null
            [System.IO.Compression.ZipFile]::ExtractToDirectory("$File", "$Destination")
        }
        catch {
            Write-Warning -Message "Unexpected Error. Error details: $_.Exception.Message"
        }


    }
    else {

        Write-Verbose -Message "Attempting to Unzip $File to location $Destination using COM"

        try {
            $shell = New-Object -ComObject Shell.Application
            $shell.Namespace($destination).copyhere(($shell.NameSpace($file)).items())
        }
        catch {
            Write-Warning -Message "Unexpected Error. Error details: $_.Exception.Message"
        }

    }

}


Remove-Item c:\TempData\Weatherdata\*
Remove-Item c:\TempData\WeatherZip\*

$source = "http://w1.weather.gov/xml/current_obs/all_xml.zip"
$destination = "c:\TempData\WeatherZip\all_XML.zip"
 
Invoke-WebRequest $source -OutFile $destination

Unzip-File -File C:\TempData\WeatherZip\all_xml.zip -Destination C:\TempData\WeatherData

Remove-Item c:\TempData\WeatherTemp\*

Copy-Item c:\TempData\WeatherData\KBDU.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KGXY.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KAFF.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KAPA.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KBJC.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KITR.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KDEN.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KFNL.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KFMM.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KSBS.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KEIK.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KLIC.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KCCU.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\K0CO.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\K20V.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\K7BM.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KOGD.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KATW.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KPRX.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KBFL.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KOAK.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KPAO.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KSDM.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KSFO.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KSJC.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KTRK.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KPTV.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KBFL.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KEDW.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KLAX.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KCYS.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KCOD.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KMSP.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KDLH.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KLAR.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KHOU.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KAUS.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KBRO.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KELP.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KPIT.XML c:\TempData\WeatherTemp
Copy-Item c:\TempData\WeatherData\KPHL.XML c:\TempData\WeatherTemp

<#
.SYNOPSIS
   
   Using National Weather Service XML Weather Output from 
   "http://w1.weather.gov/xml/current_obs/all_xml.zip"
.DESCRIPTION
   


.INPUTS
   String

.OUTPUTS
   None

.NOTES
   Author:  
   Website: 
   Twitter: 

#>