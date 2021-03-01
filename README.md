# BunnyCDN Python Lib
BunnyCDN is one of the fastest and most cost effective CDN.

With this BunnyCDN Python Library you can easily implement it and turbo charge your website content to deliver it at lighting speed to your visitors.


## Getting Started

These instructions will let you install the bunnycdnpython python library running on your local machine.

### Prerequisites
Programming language: Python

* version required : >=3.6

* Python Library(s) required : requests library
```
pip install requests
```

OS : Any OS  (ex: Windows , Mac , Linux)

*Account* : A account on -: (https://bunny.net/)

* Authentication : API Keys of of  Account and Storage API


### Installing
Step1: Open CMD

Step2: type 
``` 
pip install bunnycdnpython
```
Now bunnycdnpython python library is installed

### Using bunnycdnpython library
* #### Importing the bunnycdnpython library Storage and CDN module
```
      from BunnyCDN.Storage import Storage 
      from BunnyCDN.CDN import CDN
```
        
 * ##### Using Storage Module    

    For using Storage API you have to initialize an object with your storage api key,storage zone name and storage zone region(optional)

```
    obj_storage = Storage(storage_api_key,storage_zone_name,storage_zone_region)
```
* ##### Using CDN module 
    For using Account API you have to initialize an object with your account api key
    
    ```
    obj_cdn = CDN(account_api_key)
    
    ```
## Summary of functions in Storage module
Storage module has functions that utilize APIs mentioned in official Bunnycdn storage apiary SA
[storage api documentation](https://bunnycdnstorage.docs.apiary.io/)


* ### Download File
    To download a file from a storage zone to a particular path on your local server/PC
    ```
    >>obj_storage.DownloadFile(storage_path,download_path(optional))
    ```
    if download_path is not mentioned then file gets downloaded to current working directory

* ### Put File
    To upload a file to a specific directory in the storage zone
    ```
    >>obj_storage.PutFile(file_name, storage_path=None, local_upload_file_path(optional) )
    ```
    The storage_path here does not include storage zone name and it should end with the desired file name to be stored in storage zone.(example: 'sample_dir/abc.txt')
    
    The local_upload_file_path is the path of the file in the local PC excluding file name
* ### Delete File
    To delete a file from a specific directory in storage zone
    ```
    >>obj_storage.DeleteFile(storage_path)
    ```
* ### Get Storaged Objects List
    Returns a list containing name of all the files and folders in the directory specified in storage path
    ```
    >>obj_storage.GetStoragedObjectsList(storage_path)
    ```


## Summary of functions in CDN module
CDN module has functions that utilize APIs mentioned in official Bunnycdn apiary [CDN api documentation](https://bunnycdn.docs.apiary.io)

* ### Get Pullzone list
    To fetch the list of pullzones in the User's Account
    ```
    >>obj_cdn.GetPullZoneList()
    ```
* ### Create Pullzone
    To create a new Pulzone in User's Account
    ```
    >>obj_cdn.CreatePullZone(Name,OriginURL,Type,StorageZoneId (optional))
    ```
* ### Get Pullzone
    To return the pullzone details for the zone with the given ID
    ```
    >>obj_cdn.GetPullZone(PullZoneID)
    ```

* ### Update Pullzone
    To update the pullzone with the given ID
    ```
    >>obj_cdn.UpdatePullZone(PullZoneID,OriginUrl,AllowedReferrers,BlockedIps,EnableCacheSlice,EnableGeoZoneUS,EnableGeoZoneEU,EnableGeoZoneASIA,EnableGeoZoneSA,EnableGeoZoneAF,ZoneSecurityEnabled,ZoneSecurityIncludeHashRemoteIP,IgnoreQueryStrings,MonthlyBandwidthLimit,AccessControlOriginHeaderExtensions,EnableAccessControlOriginHeader,BlockRootPathAccess,EnableWebpVary,EnableHostnameVary,EnableCountryCodeVary,EnableLogging,DisableCookies,BudgetRedirectedCountries,BlockedCountries,EnableOriginShield,EnableQueryStringOrdering,CacheErrorResponses,OriginShieldZoneCode,AddCanonicalHeader,CacheControlMaxAgeOverride,AddHostHeader,AWSSigningEnabled,AWSSigningKey,AWSSigningRegionName,AWSSigningSecret,EnableTLS1,LoggingSaveToStorage,LoggingStorageZoneId,LogForwardingEnabled,LogForwardingHostname,LogForwardingPort,LogForwardingToken)
    ```
    * Success Response
    ```
           {
                "status": "success",
                "HTTP": 200,
                "msg": "Update successful",
            }
    ```
* ### Delete Pullzone
    To delete the pullzone with the given ID
    ```
    >>obj_cdn.DeletePullZone(PullZoneID)
    ```
    * Success Response
    ```
            {
                "status": "success",
                "HTTP": response.status_code,
                "msg": "Successfully Deleted Pullzone",
            }
    ```
* ### Purge Pullzone Cache
    To purge the full cache of given pullzone
    ```
    >>obj_cdn.PurgePullZoneCache(PullZoneID)
    ```
    * Success Response
    ```
            {
                "status": "success",
                "HTTP": 200,
                "msg": "successfully purged the cache of the given pullzone ",
            }

    ```
* ### Add or Update Edgerule
    To Add or Update an Edgerule of a particular Pullzone
    ```
    >>obj_cdn.AddorUpdateEdgerule(PullZoneID,ActionParameter1,ActionParameter2,Enabled,Description,ActionType,TriggerMatchingType,Triggers,GUID(optional))
    ```
    * Success Response
    ```
                {
                    "status": "success",
                    "HTTP": 201,
                    "msg": "successfully updated edgerule ",
                }
    ```
* ### Delete Edgerule
    To Delete the pullzone with the given ID
    ```
    >>obj_cdn.DeleteEdgeRule(PullZoneID,EdgeRuleID)
    ```
    * Success Response
    ```
            {
                "status": "success",
                "HTTP": 204,
                "msg": "Successfully Deleted edgerule",
            }
    ```
* ### Add Custom Hostname
    To add custom hostname to a pullzone
    ```
    >>obj_cdn.AddCustomHostname(PullZoneID,Hostname)
    ```
    * Success Response
    ```
            {
                "status": "success",
                "HTTP": 200,
                "msg": "Update was Successfull",
            }
    ```
* ### Delete Custom Hostname
    To delete custom hostname of a pullzone
    ```
    >>obj_cdn.DeleteCustomHostname(PullZoneID,Hostname)
    ```
    * Success Response
    ```
            {
                "status": "success",
                "HTTP": 200,
                "msg": "Successfully Deleted Hostname",
            }

    ```
* ### Set Force SSL
    To enable or disable the ForceSSL setting for a pulzone
    ```
    >>obj_cdn.SetForceSSL(PullZoneID,Hostname,ForceSSL)
    ```
    * Success Response
    ```
            {
                "status": "success",
                "HTTP": 200,
                "msg": "successfully added Hostname ",
            }
    ```
* ### Load Free Certificate
    To Load a FREE SSL Certificate to the domain provided by Let's Encrypt
    ```
    >>obj_cdn.LoadFreeCertificate(self,Hostname)
    ```
    * Success Response
    ```
    [{"Name":"pullzone1","Id":"pullzoneid1"},{"Name":"pullzone2","Id":"pullzoneid2"}]
    ```
* ### Add Certificate
    To Add a custom certificate to the given Pull Zone.
    ```
    >>obj_cdn.AddCertificate(PullZoneId,Hostname,Certificate,CertificateKey)
    ```
    * Success Response
    ```
            {
                "status": "success",
                "HTTP": 200,
                "msg": f"Certificated Added successfully Hostname:{Hostname}",
            }
    ```
* ### Add Blocked IP
    To add an IP to the list of blocked IPs that are not allowed to access the zone
    ```
    >>obj_cdn.AddBlockedIp(PullZoneId, BlockedIp)
    ```
    * Success Response
    ```
            {
                "status": "success",
                "HTTP": 200,
                "msg": "Ip successfully added to list of blocked IPs",
            }
    ```
* ### Remove Blocked IP
    To removes mentioned IP from the list of blocked IPs that are not allowed to access the zone
    ```
    >>obj_cdn.RemoveBlockedIp(PullZoneId, BlockedIp)
    ```
    * Success Response
    ```
            {
                "status": "success",
                "HTTP": 200,
                "msg": "Ip removed from blocked IPs list "
            }
    ```
* ### Get Storagezone List 
    Returns list of dictionaries containing storage zone name and its id
    ```
    >>obj_cdn.StorageZoneList()
    ```
    * Success Response
    ```
    [{"Name":"storagezone1","Id":"storagezoneid1"},{"Name":"storagezone2","Id":"storagezoneid2"}]
    ```
* ### Add Storagezone
    This function creates an new storage zone
    ```
    >>obj_cdn.AddStorageZone(storage_zone_name, storage_zone_region(optional),ReplicationRegions(optional))
    ```
    * Success Response
    ```
           {
                "status": "success",
                "HTTP": 201,
                "msg": {
                        "Name": "mystoragezone",
                        "Region": "DE",
                        "ReplicationRegions": [
                            "NY",
                            "SG"
                          ]
                        }
            }
    ```
* ### Get Storagezone
    This function returns details about the storage zone with id:storage_zone_id
    ```
    >>obj_cdn.GetStorageZone(storage_zone_id)
    ```
    * Success Response
    ```
           {
            "Id": 4122,
            "Name": "mystoragezone",
            "Password": "storage-zone-password-key",
            "ReadOnlyPassword": "storage-zone-password-key",
            "UserId": "user-id",
            "FilesStored": 20,
            "StorageUsed": 1024,
            "Deleted": false,
            "DateModified": "2017-04-22T00:00:00Z"
          }
    ```
* ### Delete Storagezone
    Deletes the Storage Zone with the given ID
    ```
    >>obj_cdn.DeleteStorageZone(storage_zone_id)
    ```
    * Success Response
    ```     {
                "status": "Success",
                "HTTP": 201,
                "msg": "Deleted Storagezone successfully",
            }
    ```
* ### Delete Video Library
    This method deletes the Storage zone with id :storage_zone_id
    ```
    >>obj.
    ```
    * Success Response
    ```
    ```
* ### Purge Url Cache
    This method purges the given URL from our edge server cache.
    ```
    >>obj_cdn.PurgeUrlCache(url)
    ```
    * Success Response
    ```
            {
                "status": "Success",
                "HTTP": 200,
                "msg": f"Purged Cache for url:{url}",
            }
    ```
* ### Get Statistics
    Returns the statistics associated with the account
    ```
    >>obj_cdn.Stats(dateFrom=None,dateTo=None,pullZone=None,serverZoneId=None,loadErrors=True)
    ```
    Here all the parameters are optional the method can also be called without any parameters
* ### Get Billing Summary
    Returns the current billing summary of the account
    ```
    >>obj_cdn.Billing()
    ```
* ### Apply a Promo Code
    Applies a promo code to the account
    ```
    >>obj_cdn.ApplyCode( couponCode )
    ```


## Versioning

 For the versions available, see the [tags on this repository](https://github.com/mathrithms/BunnyCDN-Python-Lib/tags). 

## Authors

* **MATHIRITHMS** - (https://mathrithms.com/)

See also the list of [contributors](https://github.com/mathrithms/BunnyCDN-Python-Lib/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Used similar format as per the official libraries published by [BunnyCDN](https://bunnycdnstorage.docs.apiary.io/)
