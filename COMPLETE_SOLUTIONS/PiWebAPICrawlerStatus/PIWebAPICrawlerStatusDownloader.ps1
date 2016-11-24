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

<#
Powershell script tp periodically download WebAPI Search status (For Coresight Crawler)
Output should be fed into UFL etc. 
#>


#Where to store the files (in the format $output_Path + [DateTime.Now()] + $output_extension)
$output_path = "D:\{filepath}\"
$output_extension = "status.json"
$append_dateTime = true

$url = "https://{piwebapiservice}/piwebapi/search/sources"
$timeout =  30  #How often do you want this to run (in seconds)


# Credentials are optional, but you may run into auth issues with the WebAPI. PS doesn't allow you to use the
# PowerShell doesn't (easily) allow you to use the credentials/impersonation from the execution context.
# The following call will require user input and is thus only useful for testing.

$Cred = Get-Credential 
$continue = $TRUE


while($continue) {

    $output = $output_path

    if ($append_dateTime) {
        $output += Get-Date -Format s
    }

    $output += $output_extension

    Invoke-RestMethod -Uri $url -Credential $Cred | ConvertTo-JSON -depth 999 | Out-File -FilePath $output -Encoding ascii
    Start-Sleep -Seconds $timeout
}




