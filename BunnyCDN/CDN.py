import json
import requests
from requests.exceptions import HTTPError


class CDN:
    # initializer function
    def __init__(self, api_key):

        """
        Parameters
        ----------
        api_key     : String
                      BunnyCDN account api key

        """
        assert api_key != "", "api_key for the account must be specified"
        self.headers = {
            "AccessKey": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.base_url = "https://bunnycdn.com/api/"

    def _Geturl(self, Task_name):
        """
        This function is helper for the other methods in code
        to create appropriate url.

        """
        if Task_name[0] == "/":
            if Task_name[-1] == "/":
                url = self.base_url + Task_name[1:-1]
            else:
                url = self.base_url + Task_name[1:]
        elif Task_name[-1] == "/":
            url = self.base_url + Task_name[1:-1]
        else:
            url = self.base_url + Task_name
        return url

    def AddCertificate(self,
                       PullZoneId,
                       Hostname,
                       Certificate,
                       CertificateKey):
        """
        This function adds custom certificate to the given pullzone

        Parameters
        ----------
        PullZoneId          : int64
                              The ID of the Pull Zone to which the certificate
                              will be added.

        Hostname            : string
                              The hostname to which the certificate belongs to.

        Certificate         : string
                              A base64 encoded binary certificate file data
                              Value must be of format 'base64'

        CertificateKey      : string
                              A base64 encoded binary certificate key file data
                              Value must be of format 'base64'
        """
        values = json.dumps(
            {
                "PullZoneId": PullZoneId,
                "Hostname": Hostname,
                "Certificate": Certificate,
                "CertificateKey": CertificateKey,
            }
        )

        try:
            response = requests.post(
                self._Geturl("pullzone/addCertificate"),
                data=values,
                headers=self.headers,
            )
            response.raise_for_status()
        except HTTPError as http:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": http}
        except Exception as err:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": err}
        else:
            return {
                "status": "success",
                "HTTP": response.status_code,
                "msg": f"Certificated Added successfully Hostname:{Hostname}",
            }

    def AddBlockedIp(self, PullZoneId, BlockedIp):
        """
        This method adds an IP to the list of blocked IPs that are not
        allowed to access the zone.

        Parameters
        ----------
        PullZoneId      : int64
                          The ID of the Pull Zone to which the IP block
                          will be added.
        BlockedIP       : string
                          The IP address that will be blocked
        """
        values = json.dumps(
            {"PullZoneId": PullZoneId,
             "BlockedIp": BlockedIp}
            )

        try:
            response = requests.post(
                self._Geturl("pullzone/addBlockedIp"), data=values,
                headers=self.headers
            )
            response.raise_for_status()
        except HTTPError as http:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": http}
        except Exception as err:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": err}
        else:
            return {
                "status": "success",
                "HTTP": response.status_code,
                "msg": "Ip successfully added to list of blocked IPs",
            }

    def RemoveBlockedIp(self, PullZoneId, BlockedIp):
        """
        This method removes mentioned IP from the list of blocked IPs
        that are not allowed to access the zone.

        Parameters
        ----------
        PullZoneId      : int64
                          The ID of the Pull Zone to which the
                          IP block will be added.
        BlockedIP       : string
                          The IP address that will be blocked
        """
        values = json.dumps({"PullZoneId": PullZoneId, "BlockedIp": BlockedIp})

        try:
            response = requests.post(
                self._Geturl("pullzone/removeBlockedIp"),
                data=values,
                headers=self.headers,
            )
            response.raise_for_status()
        except HTTPError as http:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": http}
        except Exception as err:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": err}
        else:
            return {
                "status": "success",
                "HTTP": response.status_code,
                "msg": "Ip removed from blocked IPs list "
            }

    def StorageZoneData(self):
        """
        This function returns a list of details of each storage zones
        in user's account

        """
        try:
            response = requests.get(self._Geturl("storagezone"),
                                    headers=self.headers)
            response.raise_for_status()
        except HTTPError as http:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": http}
        except Exception as err:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": err}
        else:
            storage_summary = []
            for storagezone in response.json():
                storage_zone_details = {}
                storage_zone_details["Id"] = storagezone["Id"]
                storage_zone_details["Storage_Zone_Name"] = storagezone["Name"]
                storage_zone_details["Usage"] = storagezone["StorageUsed"]
                hostnames = []
                pullzone = []
                for data in storagezone["PullZones"]:
                    pullzone.append(data["Name"])
                    for host_name in data["Hostnames"]:
                        hostnames.append(host_name["Value"])
                storage_zone_details["host_names"] = hostnames
                storage_zone_details["PullZones"] = pullzone
                storage_summary.append(storage_zone_details)
            return storage_summary

    def StorageZoneList(self):
        """
        Returns list of dictionaries containing storage zone
        name and storage zone id
        """
        try:
            response = requests.get(self._Geturl("storagezone"),
                                    headers=self.headers)
            response.raise_for_status()
        except HTTPError as http:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": http}
        except Exception as err:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": err}
        else:
            storage_list = []
            for storagezone in response.json():
                storage_list.append({storagezone["Name"]: storagezone["Id"]})
            return storage_list

    def AddStorageZone(
        self, storage_zone_name, storage_zone_region="DE",
        ReplicationRegions=["DE"]
    ):
        """
        This method creates a new storage zone

        Parameters
        ----------
        storage_zone_name        : string
                                   The name of the storage zone
                                        1.Matches regex pattern: ^[a-zA-Z0-9]+$
                                        2.Length of string must be less than,
                                          or equal to 20
                                        3.Length of string must be
                                          greater than, or equal to 3

        storage_zone_region      : string
        (optional)                 The main region code of storage zone
                                        1.Matches regex pattern: ^[a-zA-Z0-9]+$
                                        2.Length of string must be less than,
                                          or equal to 2
                                        3.Length of string must be
                                          greater than, or equal to 2

        ReplicationsRegions      : array
        (optional)                 The list of active replication regions
                                   for the zone

        """
        values = json.dumps(
            {
                "Name": storage_zone_name,
                "Region": storage_zone_region,
                "ReplicationRegions": ReplicationRegions,
            }
        )
        try:
            response = requests.post(
                self._Geturl("storagezone"), data=values, headers=self.headers
            )
            response.raise_for_status()
        except HTTPError as http:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": http}
        except Exception as err:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": err}
        else:
            return {
                "status": "success",
                "HTTP": response.status_code,
                "msg": response.json(),
            }

    def GetStorageZone(self, storage_zone_id):

        """
        This function returns details about the storage zone
        whose id is mentioned

        Parameters
        ----------
        storage_zone_id     :   int64
                                The ID of the Storage Zone to return

        """
        try:
            response = requests.get(
                self._Geturl(f"storagezone/{storage_zone_id}"),
                headers=self.headers
            )
            response.raise_for_status()
        except HTTPError as http:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": http}
        except Exception as err:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": err}
        else:
            return response.json()

    def DeleteStorageZone(self, storage_zone_id):
        """
        This method deletes the Storage zone with id : storage_zone_id

        Parameters
        ----------
        storage_zone_id :   int64
                            The ID of the storage zone that should be deleted
        """
        try:
            response = requests.delete(
                self._Geturl(f"storagezone/{storage_zone_id}"),
                headers=self.headers
            )
            response.raise_for_status()
        except HTTPError as http:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": http}
        except Exception as err:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": err}
        else:
            return {
                "status": "Success",
                "HTTP": response.status_code,
                "msg": response.json(),
            }

    def PurgeUrlCache(self, url):
        """
        This method purges the given URL from our edge server cache.

        Parameters
        ----------
        url : string
              The URL of the file that will be purged.
              Use a CDN enabled URL such as http://myzone.b-cdn.net/style.css
        """
        try:
            response = requests.post(
                self._Geturl("purge"), params={"url": url},
                headers=self.headers
            )
            response.raise_for_status()
        except HTTPError as http:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": http}
        except Exception as err:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": err}
        else:
            return {
                "status": "Success",
                "HTTP": response.status_code,
                "msg": f"Purged Cache for url:{url}",
            }

    def Billing(self):
        """
        This method returns the current billing summary of the account

        """
        try:
            response = requests.get(self._Geturl("billing"),
                                    headers=self.headers)
            response.raise_for_status()
        except HTTPError as http:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": http}
        except Exception as err:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": err}
        else:
            return response.json()

    def ApplyCode(self, couponCode):
        """
        This method applys promo code to the account

        Parameters
        ----------
        couponCode  :  The promo code that will be applied

        """
        try:
            response = requests.get(
                self._Geturl("billing/applycode"),
                params={"couponCode": couponCode},
                headers=self.headers,
            )
            response.raise_for_status()
        except HTTPError as http:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": http}
        except Exception as err:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": err}
        else:
            return {
                "status": "success",
                "HTTP": response.status_code,
                "msg": f"Applied promo code:{couponCode} successfully",
            }

    def Stats(
        self,
        dateFrom=None,
        dateTo=None,
        pullZone=None,
        serverZoneId=None,
        loadErrors=True,
    ):
        """
        This method returns the statistics associated
        with your account as json object

        Parameters
        ----------

        dateFrom        : string
        (optional)        The start date of the range the statistics
                          should be returned for. Format: yyyy-mm-dd

        dateTo          : string
        (optional)        The end date of the range the statistics
                          should be returned for. Format: yyyy-MM-dd

        pullZone        : int64
        (optional)        The ID of the Pull Zone for which the
                          statistics should be returned

        serverZoneId    : int64
        (optional)        The server zone for which the data
                          should be returned.

        loadErrors      : boolean
        (optional)        Set to true by default
        """

        params = {
            "dateFrom": dateFrom,
            "dateTo": dateTo,
            "pullZone": pullZone,
            "serverZoneId": serverZoneId,
            "loadErrors": loadErrors,
        }

        try:
            response = requests.get(
                self._Geturl("statistics"), params=params, headers=self.headers
            )
            response.raise_for_status()
        except HTTPError as http:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": http}
        except Exception as err:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": err}
        else:
            return response.json()

    def GetPullZoneList(self):
        """
        This function fetches the list of pullzones in the User's Account

        Parameters
        ----------
        None
        """
        try:
            response = requests.get(self._Geturl("pullzone"),
                                    headers=self.headers)
            response.raise_for_status()
        except HTTPError as http:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": http}
        except Exception as err:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": err}
        else:
            pullzone_list = []
            for pullzone in response.json():
                pullzone_list.append({pullzone["Name"]: pullzone["Id"]})
            return pullzone_list

    def CreatePullZone(self, Name, OriginURL, Type, StorageZoneId=None):
        """
        This function creates a new Pulzone in User's Account
        Parameters
        ----------
        Name                : string
                              The name of the new pull zone

        Type                : string
                              number
                              The pricing type of the pull zone to be added.
                              0 = Standard, 1 = High Volume

        OriginURL           : string
                              The origin URL where the pull zone files
                              are pulled from.

        StorageZoneId       : int64
                              The ID(number) of the storage zone to which
                              the pull zone will be linked (Optional)

        """

        if StorageZoneId is None:
            values = json.dumps(
                {"Name": Name,
                 "Type": Type,
                 "OriginURL": OriginURL}
                )
        else:
            values = {
                "Name": Name,
                "Type": Type,
                "OriginURL": OriginURL,
                "StorageZoneId": StorageZoneId,
            }
        try:
            response = requests.post(
                self._Geturl("pullzone"), data=values, headers=self.headers
            )
            response.raise_for_status()
        except HTTPError as http:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": http}
        except Exception as err:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": err}
        else:
            return response.json()

    def GetPullZone(self, PullZoneID):
        """
        This function returns the pullzone details
        for the zone with the given ID

        Parameters
        ----------
        PullZoneID            : int64
                                The ID (number) of the pullzone to return
        """
        try:
            response = requests.get(
                self._Geturl(f"pullzone/{PullZoneID}"), headers=self.headers
            )
            response.raise_for_status()
        except HTTPError as http:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": http}
        except Exception as err:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": err}
        else:
            return response.json()

    def UpdatePullZone(
        self,
        PullZoneID,
        OriginUrl,
        AllowedReferrers,
        BlockedIps,
        EnableCacheSlice,
        EnableGeoZoneUS,
        EnableGeoZoneEU,
        EnableGeoZoneASIA,
        EnableGeoZoneSA,
        EnableGeoZoneAF,
        ZoneSecurityEnabled,
        IncludeHashRemoteIP,
        IgnoreQueryStrings,
        MonthlyBandwidthLimit,
        OriginHeaderExtensions,
        EnableOriginHeader,
        BlockRootPathAccess,
        EnableWebpVary,
        EnableHostnameVary,
        EnableCountryCodeVary,
        EnableLogging,
        DisableCookies,
        BudgetRedirectedCountries,
        BlockedCountries,
        EnableOriginShield,
        EnableQueryStringOrdering,
        CacheErrorResponses,
        OriginShieldZoneCode,
        AddCanonicalHeader,
        CacheControlMaxAgeOverride,
        AddHostHeader,
        AWSSigningEnabled,
        AWSSigningKey,
        AWSSigningRegionName,
        AWSSigningSecret,
        EnableTLS1,
        LoggingSaveToStorage,
        LoggingStorageZoneId,
        LogForwardingEnabled,
        LogForwardingHostname,
        LogForwardingPort,
        LogForwardingToken,
    ):
        """
        This function updates the pullzone with the given ID

        Parameters
        ----------
        PullZoneID                    : int64
                                        The ID (number) of the
                                        pullzone to update

        OriginUrl                     : string
                                        The origin URL of the pull zone

        AllowedReferrers              : array

        BlockedIps                    : array

        EnableCacheSlice              : boolean
                                        If enabled, the cached data will be
                                        stored in small chunks and allow the
                                        server to process byte range requests
                                        even for uncached files.

        EnableGeoZoneUS               : boolean
                                        If enabled, the zone will serve data
                                        through our United States PoPs.

        EnableGeoZoneEU               : boolean
                                        If enabled, the zone will serve data
                                        through our European PoPs.

        EnableGeoZoneASIA             : boolean
                                        If enabled, the zone will serve data
                                        through our Asian and Oceanian PoPs.

        EnableGeoZoneSA               : boolean
                                        If enabled, the zone will serve data
                                        through our South American PoPs.

        EnableGeoZoneAF               : boolean
                                        If enabled, the zone will serve data
                                        through our African PoPs.

        ZoneSecurityEnabled           : boolean
                                        If enabled, the zone will be secured
                                        using token authentication.

        IncludeHashRemoteIP : boolean
                                          If enabled, the zone token
                                          authentication hash will
                                          include the remote IP.

        IgnoreQueryStrings            : boolean
                                        If enabled, the URLs will ignore any
                                        kind of query strings when looking
                                        for and storing cached files

        MonthlyBandwidthLimit         : number
                                        Set the monthly pull zone
                                        bandwidth limit in bytes.

        OriginHeaderExtensions        : array

        EnableOriginHeader            : boolean
                                        If enabled the CORS headers will be
                                        returned with the requests to CORS
                                        enabled extensions.

        BlockRootPathAccess           : boolean
                                        Set to true if you want to block all
                                        requests going to root directories
                                        instead of files.

        EnableWebpVary                : boolean
                                        If enabled, the zone will dynamically
                                        vary the cached based on WebP support

        EnableHostnameVary            : boolean
                                        Set to true if the cache files should
                                        vary based on the request hostname

        EnableCountryCodeVary         : boolean
                                        Set to true if the cache files should
                                        vary based on the country code

        EnableLogging                 : boolean
                                        Set to true if the logging for the
                                        zone should be enabled

        DisableCookies                : boolean
                                        If true, the cookies are disabled
                                        for the pull zone

        BudgetRedirectedCountries     : array

        BlockedCountries              : array

        EnableOriginShield            : boolean
                                        Set to true to enable the origin
                                        shield for this zone

        EnableQueryStringOrdering     : boolean
                                        Set to true to enable query string
                                        sorting when caching files

        CacheErrorResponses           : boolean
                                        Set to true to temporary cache error
                                        responses from the origins erver

        OriginShieldZoneCode          : string
                                        The zone code of the origin
                                        shield location

        AddCanonicalHeader            : boolean
                                        True if the zone should return an
                                        automatically generated canonical
                                        header

        CacheControlMaxAgeOverride    : number
                                        Set the cache control override,
                                        set to 0 to respect the origin headers

        CacheControlBrowserMaxAgeOverride : number
                                            Set the browser cache control
                                            override,set to -1 for this
                                            to match the internal cache-control

        AddHostHeader                 : boolean
                                        If enabled, the original host header
                                        of the request will be forwarded to
                                        the origin server.

        AWSSigningEnabled             : boolean
                                        If enabled, this will send Amazon S3
                                        authentication headers back to
                                        the origin.

        AWSSigningKey                 : string
                                        The Amazon S3 signing key used
                                        to sign origin requests

        AWSSigningRegionName          : string
                                        The Amazon S3 region name used
                                        to sign origin requests

        AWSSigningSecret              : string
                                        The Amazon S3 secret used to
                                        sign origin requests

        EnableTLS1                    : boolean
                                        True if the zone should allow legacy
                                        TLS 1 connections

        EnableTLS1_1                  : boolean
                                        True if the zone should allow legacy
                                        TLS 1.1 connections

        LoggingSaveToStorage          : boolean
                                        True to enable permanent log storage.
                                        This must be sent together with a
                                        valid LoggingStorageZoneId property.

        LoggingStorageZoneId          : number
                                        The ID of the permanent log
                                        storage zone.

        LogForwardingEnabled          : boolean
                                        True if the log forwarding feature
                                        should be enabled.

        LogForwardingHostname         : string
                                        The hostname of the log forwarding
                                        endpoint.

        LogForwardingPort             : number
                                        The port of the log forwarding
                                        endpoint.

        LogForwardingToken            : string
                                        The authentication token for the log
                                        forwarding endpoint.

        """
        values = json.dumps(
            {
                "PullZoneID": PullZoneID,
                "OriginUrl": OriginUrl,
                "AllowedReferrers": AllowedReferrers,
                "BlockedIps": BlockedIps,
                "EnableCacheSlice": EnableCacheSlice,
                "EnableGeoZoneUS": EnableGeoZoneUS,
                "EnableGeoZoneEU": EnableGeoZoneEU,
                "EnableGeoZoneASIA": EnableGeoZoneASIA,
                "EnableGeoZoneSA": EnableGeoZoneSA,
                "EnableGeoZoneAF": EnableGeoZoneAF,
                "ZoneSecurityEnabled": ZoneSecurityEnabled,
                "ZoneSecurityIncludeHashRemoteIP": IncludeHashRemoteIP,
                "IgnoreQueryStrings": IgnoreQueryStrings,
                "MonthlyBandwidthLimit": MonthlyBandwidthLimit,
                "AccessControlOriginHeaderExtensions": OriginHeaderExtensions,
                "EnableAccessControlOriginHeader": EnableOriginHeader,
                "BlockRootPathAccess": BlockRootPathAccess,
                "EnableWebpVary": EnableWebpVary,
                "EnableHostnameVary": EnableHostnameVary,
                "EnableCountryCodeVary": EnableCountryCodeVary,
                "EnableLogging": EnableLogging,
                "DisableCookies": DisableCookies,
                "BudgetRedirectedCountries": BudgetRedirectedCountries,
                "BlockedCountries": BlockedCountries,
                "EnableOriginShield": EnableOriginShield,
                "EnableQueryStringOrdering": EnableQueryStringOrdering,
                "CacheErrorResponses": CacheErrorResponses,
                "OriginShieldZoneCode": OriginShieldZoneCode,
                "AddCanonicalHeader": AddCanonicalHeader,
                "CacheControlMaxAgeOverride": CacheControlMaxAgeOverride,
                "AddHostHeader": AddHostHeader,
                "AWSSigningEnabled": AWSSigningEnabled,
                "AWSSigningKey": AWSSigningKey,
                "AWSSigningRegionName": AWSSigningRegionName,
                "AWSSigningSecret": AWSSigningSecret,
                "EnableTLS1": EnableTLS1,
                "LoggingSaveToStorage": LoggingSaveToStorage,
                "LoggingStorageZoneId": LoggingStorageZoneId,
                "LogForwardingEnabled": LogForwardingEnabled,
                "LogForwardingHostname": LogForwardingHostname,
                "LogForwardingPort": LogForwardingPort,
                "LogForwardingToken": LogForwardingToken,
            }
        )
        try:
            response = requests.post(
                self._Geturl(f"pullzone/{PullZoneID}"),
                data=values,
                headers=self.headers
            )
            response.raise_for_status()
        except HTTPError as http:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": http}
        except Exception as err:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": err}
        else:
            return {
                "status": "success",
                "HTTP": response.status_code,
                "msg": "Update successful",
            }

    def DeletePullZone(self, PullZoneID):
        """
        This function updates the pullzone with the given ID

        Parameters
        ----------
        PullZoneID            : int64
                                The ID (number) of the pullzone to delete

        """
        try:
            response = requests.delete(
                self._Geturl(f"pullzone/{PullZoneID}"), headers=self.headers
            )
            response.raise_for_status()
        except HTTPError as http:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": http}
        except Exception as err:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": err}
        else:
            return {
                "status": "success",
                "HTTP": response.status_code,
                "msg": "Successfully Deleted Pullzone",
            }

    def PurgePullZoneCache(self, PullZoneID):
        """
        This function purges the full cache of given pullzone

        Parameters
        ----------
        PullZoneID            : int64
                                The ID (number) of the pullzone
                                who's cache is to be Purged
        """
        try:
            response = requests.post(
                self._Geturl(f"pullzone/{PullZoneID}/purgeCache"),
                headers=self.headers
            )
            response.raise_for_status()
        except HTTPError as http:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": http}
        except Exception as err:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": err}
        else:
            return {
                "status": "success",
                "HTTP": response.status_code,
                "msg": "successfully purged the cache of the given pullzone ",
            }

    def AddorUpdateEdgerule(
        self,
        PullZoneID,
        ActionParameter1,
        ActionParameter2,
        Enabled,
        Description,
        ActionType,
        TriggerMatchingType,
        Triggers,
        GUID=None,
    ):

        """
        This function Adds or Updates the Edgerule

        Parameters
        ----------
        PullZoneID              :int64
                                 The Id(number) of the pullzone whose edgerule
                                 is to be updated or where new edgerule has to
                                 be added

        GUID                    :number
                                 Guid of the edgerule
                                 (exclude when adding a new edgerule)

        ActionParameter1        :string
                                 The action parameter 1 of the edge rule

        ActionParameter2        :string
                                 The action parameter 2 of the edge rule

        Enabled                 :boolean
                                 The boolean

        Description             :string
                                 The description of the Edge rule

        ActionType              :number
                                 The action type of the edge rule.
                                 The possible values are: ForceSSL = 0
                                 Redirect = 1,OriginUrl = 2
                                 OverrideCacheTime = 3,BlockRequest = 4,
                                 SetResponseHeader = 5,SetRequestHeader = 6,
                                 ForceDownload =7,DisableTokenAuthentication=8,
                                 EnableTokenAuthentication = 9

        TriggerMatchingType     :number
                                 Trigger matching type

        Triggers                :array

        """
        if GUID is None:
            values = json.dumps(
                {
                    "ActionParameter1": ActionParameter1,
                    "ActionParameter2": ActionParameter2,
                    "Enabled": Enabled,
                    "Description": Description,
                    "ActionType": ActionType,
                    "TriggerMatchingType": TriggerMatchingType,
                    "Triggers": Triggers,
                }
            )
            try:
                response = requests.post(
                  self._Geturl(f"pullzone/{PullZoneID}/edgerules/addOrUpdate"),
                  data=values,
                  headers=self.headers,
                )
                response.raise_for_status()
            except HTTPError as http:
                return {"status": "error",
                        "HTTP": response.status_code,
                        "msg": http}
            except Exception as err:
                return {"status": "error",
                        "HTTP": response.status_code,
                        "msg": err}
            else:
                return {
                    "status": "success",
                    "HTTP": response.status_code,
                    "msg": "successfully added edgerule ",
                }
        else:
            values = json.dumps(
                {
                    "GUID": GUID,
                    "ActionParameter1": ActionParameter1,
                    "ActionParameter2": ActionParameter2,
                    "Enabled": Enabled,
                    "Description": Description,
                    "ActionType": ActionType,
                    "TriggerMatchingType": TriggerMatchingType,
                    "Triggers": Triggers,
                }
            )

            try:
                response = requests.post(
                  self._Geturl(f"pullzone/{PullZoneID}/edgerules/addOrUpdate"),
                  data=values,
                  headers=self.headers,
                )
                response.raise_for_status()
            except HTTPError as http:
                return {"status": "error",
                        "HTTP": response.status_code,
                        "msg": http}
            except Exception as err:
                return {"status": "error",
                        "HTTP": response.status_code,
                        "msg": err}
            else:
                return {
                    "status": "success",
                    "HTTP": response.status_code,
                    "msg": "successfully updated edgerule ",
                }

    def DeleteEdgeRule(self, PullZoneID, EdgeRuleID):
        """
        This function deletes the edgerule

        Parameters
         ---------
        PullZoneID          :number
                             ID of the pullzone that holds the edgerule

        EdgeRuleID          :string
                             ID of the edgerule to be deleted

        """
        try:
            response = requests.delete(
                self._Geturl(f"pullzone/{PullZoneID}/edgerules/{EdgeRuleID}"),
                headers=self.headers,
            )
            response.raise_for_status()
        except HTTPError as http:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": http}
        except Exception as err:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": err}
        else:
            return {
                "status": "success",
                "HTTP": response.status_code,
                "msg": "Successfully Deleted edgerule",
            }

    def AddCustomHostname(self, PullZoneID, Hostname):
        """
        This function is used to add custom hostname to a pullzone

        Parameters
        ----------
        PullZoneID:         : int64
                              ID of the pullzone to which hostname
                              will be added

        Hostname:           : string
                              The hostname that will be registered

        """
        values = json.dumps({"PullZoneID": PullZoneID, "Hostname": Hostname})

        try:
            response = requests.post(
                self._Geturl("pullzone/addHostname"),
                data=values,
                headers=self.headers
            )
            response.raise_for_status()
        except HTTPError as http:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": http}
        except Exception as err:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": err}
        else:
            return {
                "status": "success",
                "HTTP": response.status_code,
                "msg": "Update was Successfull",
            }

    def DeleteCustomHostname(self, PullZoneID, Hostname):

        """
        This function is used to delete custom hostname of a pullzone

        Parameters
        ----------
        PullZoneID:         :number
                             ID of the pullzone of which custom hostname
                             will be delted

        Hostname:           :string
                             The hostname that will be deleted

        """
        params = {"id": PullZoneID, "hostname": Hostname}
        try:
            response = requests.delete(
                self._Geturl("pullzone/deleteHostname"),
                params=params,
                headers=self.headers,
            )
            response.raise_for_status()
        except HTTPError as http:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": http}
        except Exception as err:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": err}
        else:
            return {
                "status": "success",
                "HTTP": response.status_code,
                "msg": "Successfully Deleted Hostname",
            }

    def SetForceSSL(self, PullZoneID, Hostname, ForceSSL):
        """
        This function is used to enable or disable the ForceSSL
        setting for a pulzone

        Parameters
        ----------
        PullZoneID          :number
                             The id of the pull zone that the hostname
                             belongs to

        Hostname            :string
                             The hostname that will be updated

        ForceSSL            :boolean
                             If enabled, the zone will force redirect
                             to the SSL version of the URLs

        """
        values = json.dumps(
            {"PullZoneID": PullZoneID,
             "Hostname": Hostname,
             "ForceSSL": ForceSSL}
        )
        try:
            response = requests.post(
                self._Geturl("pullzone/setForceSSL"),
                data=values,
                headers=self.headers
            )
            response.raise_for_status()
        except HTTPError as http:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": http}
        except Exception as err:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": err}
        else:
            return {
                "status": "success",
                "HTTP": response.status_code,
                "msg": "successfully added Hostname ",
            }

    def LoadFreeCertificate(self, Hostname):
        """
        This function Loads a FREE SSL Certificate to the domain
        provided by Let's Encrypt

        Parameters
        ----------
        Hostname            : string
                              Hostname that the ForceSSL certificate
                              will be loaded for

        """
        try:
            response = requests.get(
             self._Geturl(f"pullzone/loadFreeCertificate?hostname={Hostname}"),
             headers=self.headers,
            )
            response.raise_for_status()
        except HTTPError as http:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": http}
        except Exception as err:
            return {"status": "error",
                    "HTTP": response.status_code,
                    "msg": err}
        else:
            return self.GetPullZoneList()
