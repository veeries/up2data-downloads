# UP2DATA CLOUD B3 - SCRIPT TO AUTOMATE DATA DOWNLOAD
UP2DATA is a cloud service provided by B3 based on Microsoft Azure, where multiple market indicators and transactions are stored.

## OBJECTIVE
The data on UP2DATA is cycled every 30 days, meaning, the data concerning the last business days inside those 30 days is available,
but once a new day is added, the oldest date is removed. 
This repo aims to share different script examples for an automated download of the data
for those that need to mantain a history of the data locally or on their respective cloud providers.

## AZCOPY
AzCopy is a tool that helps with copying blobs and files from storage to storage,
more can be read on it on the official documentation here:
"https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10"  


OBS: Add AzCopy to your envinronment variables for the scripts to work.

## LANGUAGES
### PYTHON
#### STATUS
* Working script example that generates the Auth Token and blob URLs automatically;


* .pfx certificate decoding to base64 still not automated and must be done manually using: "https://www.base64encode.org/"
