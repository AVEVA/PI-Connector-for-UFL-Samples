
Remove-Item c:\TempData\USGSTemp\*

$source = "http://waterservices.usgs.gov/nwis/iv/?format=waterml,1.1&sites=03455500&parameterCd=00060,00065"
$destination = "C:\TempData\USGSTemp\USGS_03455500_W_F_PIGEON_R_ABOVE_LAKE_LOGAN_NR_HAZELWOOD_NC.xml"
 
Invoke-WebRequest $source -OutFile $destination

$source = "http://waterservices.usgs.gov/nwis/iv/?format=waterml,1.1&sites=0345577330&parameterCd=00060,00065"
$destination = "C:\TempData\USGSTemp\USGS_0345577330_WEST_FORK_PIGEON_RIVER_NEAR_RETREAT_NC.xml"
 
Invoke-WebRequest $source -OutFile $destination

$source = "http://waterservices.usgs.gov/nwis/iv/?format=waterml,1.1&sites=03456100&parameterCd=00060,00065"
$destination = "C:\TempData\USGSTemp\USGS_03456100_WEST_FORK_PIGEON_RIVER_AT_BETHEL_NC.xml"
 
Invoke-WebRequest $source -OutFile $destination

$source = "http://waterservices.usgs.gov/nwis/iv/?format=waterml,1.1&sites=03456500&parameterCd=00060,00065"
$destination = "C:\TempData\USGSTemp\USGS_03456500_EAST_FORK_PIGEON_RIVER_NEAR_CANTON_NC.xml"
 
Invoke-WebRequest $source -OutFile $destination

$source = "http://waterservices.usgs.gov/nwis/iv/?format=waterml,1.1&sites=03456991&parameterCd=00060,00065"
$destination = "C:\TempData\USGSTemp\USGS_03456991_PIGEON_RIVER_NEAR_CANTON_NC.xml"
 
Invoke-WebRequest $source -OutFile $destination

$source = "http://waterservices.usgs.gov/nwis/iv/?format=waterml,1.1&sites=03459500&parameterCd=00060,00065"
$destination = "C:\TempData\USGSTemp\USGS_03459500_PIGEON_RIVER_NEAR_HEPCO_NC.xml"
 
Invoke-WebRequest $source -OutFile $destination

$source = "http://waterservices.usgs.gov/nwis/iv/?format=waterml,1.1&sites=03460000&parameterCd=00060,00065"
$destination = "C:\TempData\USGSTemp\USGS_03460000_CATALOOCHEE_CREEK_NEAR_CATALOOCHEE_NC.xml"
 
Invoke-WebRequest $source -OutFile $destination

$source = "http://waterservices.usgs.gov/nwis/iv/?format=waterml,1.1&sites=03460795&parameterCd=00060,00065"
$destination = "C:\TempData\USGSTemp\USGS_03460795_PIGEON_R_BL_POWER_PLANT_NR_WATERVILLE_NC.xml"
 
Invoke-WebRequest $source -OutFile $destination

$source = "http://waterservices.usgs.gov/nwis/iv/?format=waterml,1.1&sites=07263650&parameterCd=00060,00065"
$destination = "C:\TempData\USGSTemp\USGS_07263650_Arkansas_River_at_Pine_Bluff_AR.xml"
 
Invoke-WebRequest $source -OutFile $destination


$source = "http://waterservices.usgs.gov/nwis/iv/?format=waterml,1.1&sites=06715000&parameterCd=00060,00065"
$destination = "C:\TempData\USGSTemp\CLEAR CREEK ABV WEST FORK CLEAR CREEK NR EMPIRE CO.xml"
 
Invoke-WebRequest $source -OutFile $destination

$source = "http://waterservices.usgs.gov/nwis/iv/?format=waterml,1.1&sites=06716500&parameterCd=00060,00065"
$destination = "C:\TempData\USGSTemp\CLEAR CREEK NEAR LAWSON, CO.xml"
 
Invoke-WebRequest $source -OutFile $destination


$source = "http://waterservices.usgs.gov/nwis/iv/?format=waterml,1.1&sites=06719505&parameterCd=00060,00065"
$destination = "C:\TempData\USGSTemp\CLEAR CREEK AT GOLDEN, CO.xml"
 
Invoke-WebRequest $source -OutFile $destination