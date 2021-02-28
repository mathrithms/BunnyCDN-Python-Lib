
import os
import json
import requests
from requests.exceptions import HTTPError



class CDN():
    #initializer function
    def __init__(self,api_key):
        
        '''
        Parameters
        ----------
        api_key     : String
                      BunnyCDN account api key
        
        '''
        assert api_key !='',"api_key for the account must be specified"
        self.headers={
            'AccessKey':api_key,
            'Content-Type':'application/json',
            'Accept':'application/json'
        }
        self.base_url="https://bunnycdn.com/api/"

    def _Geturl(self,Task_name):
        '''
        This function is helper for the other methods in code to create appropriate url.

        '''
        if Task_name[0]=='/':
            if Task_name[-1]=='/':
                url=self.base_url + Task_name[1:-1]
            else:
                url=self.base_url + Task_name[1:]
        elif Task_name[-1]=='/':
             url=self.base_url + Task_name[1:-1]
        else:
            url=self.base_url + Task_name
        return url
    

    def AddCertificate(self,PullZoneId,Hostname,Certificate,CertificateKey):
        '''
        This function adds custom certificate to the given pullzone

        Parameters
        ----------
        PullZoneId          : int64
                              The ID of the Pull Zone to which the certificate will be added.
        
        Hostname            : string
                              The hostname to which the certificate belongs to.
        
        Certificate         : string
                              A base64 encoded binary certificate file data
                              Value must be of format 'base64'
       
        CertificateKey      : string
                              A base64 encoded binary certificate key file data
                              Value must be of format 'base64'
        '''
        values =json.dumps({
            "PullZoneId": PullZoneId,
            "Hostname": Hostname,
            "Certificate": Certificate,
            "CertificateKey": CertificateKey
        })

        try:
            response=requests.post(self._Geturl('pullzone/addCertificate'),data=values,headers=self.headers)
            response.raise_for_status()
        except HTTPError as http:
            return {'status':'error','HTTP':response.status_code,'msg':http}
        except Exception as err:
            return {'status':'error','HTTP':response.status_code,'msg':err}
        else:
           return {'status':'success','HTTP':response.status_code,'msg':f'Certificated Added successfully to PullZoneId:{PullZoneId},Hostname:{Hostname}'}
    
    def AddBlockedIp(self,PullZoneId,BlockedIp):
        '''
        This method adds an IP to the list of blocked IPs that are not allowed to access the zone.
        
        Parameters
        ----------
        PullZoneId      : int64
                          The ID of the Pull Zone to which the IP block will be added.
        BlockedIP       : string
                          The IP address that will be blocked
        '''
        values=json.dumps({
            "PullZoneId": PullZoneId,
            "BlockedIp": BlockedIp
        })

        try :
            response=requests.post(self._Geturl('pullzone/addBlockedIp'),data=values,headers=self.headers)
            response.raise_for_status()
        except HTTPError as http:
            return {'status':'error','HTTP':response.status_code,'msg':http}
        except Exception as err:
            return {'status':'error','HTTP':response.status_code,'msg':err}
        else:
            return {'status':'success','HTTP':response.status_code,'msg':f"Ip successfully added to list of blocked IPs for pullzone id: {PullZoneId}"}
        
    def RemoveBlockedIp(self,PullZoneId,BlockedIp):
        '''
        This method removes mentioned IP from the list of blocked IPs that are not allowed to access the zone.
        
        Parameters
        ----------
        PullZoneId      : int64
                          The ID of the Pull Zone to which the IP block will be added.
        BlockedIP       : string
                          The IP address that will be blocked
        '''
        values=json.dumps({
            "PullZoneId":PullZoneId,
            "BlockedIp": BlockedIp
        })

        try :
            response=requests.post(self._Geturl('pullzone/removeBlockedIp'),data=values,headers=self.headers)
            response.raise_for_status()
        except HTTPError as http:
            return {'status':'error','HTTP':response.status_code,'msg':http}
        except Exception as err:
            return {'status':'error','HTTP':response.status_code,'msg':err}
        else:
            return {'status':'success','HTTP':response.status_code,'msg':f"Ip successfully removed from list of blocked IPs for pullzone id: {PullZoneId}"}
    
    def StorageZoneData(self):
        '''
        This function returns a list of details of each storage zones in user's account

        '''
        try :
            response=requests.get(self._Geturl('storagezone'),headers=self.headers)
            response.raise_for_status()
        except HTTPError as http:
            return {'status':'error','HTTP':response.status_code,'msg':http}
        except Exception as err:
            return {'status':'error','HTTP':response.status_code,'msg':err}
        else:

            storage_summary=[]
            for storagezone in response.json():
                storage_zone_details={}
                storage_zone_details['Id']=storagezone['Id']
                storage_zone_details['Storage_Zone_Name']=storagezone['Name']
                storage_zone_details['Storage_used']=storagezone['StorageUsed']
                hostnames=[]
                pullzone=[]
                for data in storagezone['PullZones']: 
                    pullzone.append(data['Name'])
                    for host_name in data['Hostnames']:
                        hostnames.append(host_name['Value'])
                storage_zone_details['host_names']=hostnames
                storage_zone_details['PullZones']=pullzone
                storage_summary.append(storage_zone_details)
            return storage_summary

    def StorageZoneList(self):
        '''
        This function returns list of dictionaries containing storage zone name and storage zone id 
        '''
        try :
            response=requests.get(self._Geturl('storagezone'),headers=self.headers)
            response.raise_for_status()
        except HTTPError as http:
            return {'status':'error','HTTP':response.status_code,'msg':http}
        except Exception as err:
            return {'status':'error','HTTP':response.status_code,'msg':err}
        else:

            storage_list=[]
            for storagezone in response.json():
                storage_list.append({storagezone['Name']:storagezone['Id']})
               
            return storage_list
    
    def AddStorageZone(self,storage_zone_name,storage_zone_region='DE',ReplicationRegions=[]):
        '''
        This method creates a new storage zone

        Parameters
        ----------
        storage_zone_name        : string
                                   The name of the storage zone
                                        1.Matches regex pattern: ^[a-zA-Z0-9]+$
                                        2.Length of string must be less than, or equal to 20
                                        3.Length of string must be greater than, or equal to 3
        
        storage_zone_region      : string 
        (optional)                 The main region code of storage zone
                                        1.Matches regex pattern: ^[a-zA-Z0-9]+$
                                        2.Length of string must be less than, or equal to 2
                                        3.Length of string must be greater than, or equal to 2
        
        ReplicationsRegions      : array
        (optional)                 The list of active replication regions for the zone

        '''
        values =  json.dumps( {
            "Name": storage_zone_name,
            "Region": storage_zone_region,
            "ReplicationRegions":ReplicationRegions
    
        })
        try :
            response=requests.post(self._Geturl('storagezone'),data=values,headers=self.headers)
            response.raise_for_status()
        except HTTPError as http:
            return {'status':'error','HTTP':response.status_code,'msg':http}
        except Exception as err:
            return {'status':'error','HTTP':response.status_code,'msg':err}
        else:
            return {'status':'success','HTTP':response.status_code,'msg':response.json()}

    
    def GetStorageZone(self,storage_zone_id):

        '''
        This function returns details about the storage zone whose id is mentioned

        Parameters
        ----------
        storage_zone_id     :   int64 
                                The ID of the Storage Zone to return

        '''
        try :
            response=requests.get(self._Geturl(f'storagezone/{storage_zone_id}'),headers=self.headers)
            response.raise_for_status()
        except HTTPError as http:
            return {'status':'error','HTTP':response.status_code,'msg':http}
        except Exception as err:
            return {'status':'error','HTTP':response.status_code,'msg':err}
        else:
            return response.json()

    
    def DeleteStorageZone(self,storage_zone_id):
        '''
        This method deletes the Storage zone with id : storage_zone_id
        
        Parameters
        ----------
        storage_zone_id :   int64
                            The ID of the storage zone that should be deleted
        '''
        try :
            response=requests.delete(self._Geturl(f'storagezone/{storage_zone_id}'),headers=self.headers)
            response.raise_for_status()
        except HTTPError as http:
            return {'status':'error','HTTP':response.status_code,'msg':http}
        except Exception as err:
            return {'status':'error','HTTP':response.status_code,'msg':err}
        else:
            return {'status':'Success','HTTP':response.status_code, 'msg':response.json()}
        
    def PurgeUrlCache(self,url):
        '''
        This method purges the given URL from our edge server cache.
        
        Parameters
        ----------
        url : string
              The URL of the file that will be purged. Use a CDN enabled URL such as http://myzone.b-cdn.net/style.css
        '''
        try :
            response=requests.post(self._Geturl('purge'),params={'url':url} ,headers=self.headers)
            response.raise_for_status()
        except HTTPError as http:
            return {'status':'error','HTTP':response.status_code,'msg':http}
        except Exception as err:
            return {'status':'error','HTTP':response.status_code,'msg':err}
        else:
            return {'status':'Success','HTTP':response.status_code, 'msg':f'Purged Cache for url:{url}'}

    def Billing(self):
        '''
        This method returns the current billing summary of the account

        '''
        try :
            response=requests.get(self._Geturl('billing'),headers=self.headers)
            response.raise_for_status()
        except HTTPError as http:
            return {'status':'error','HTTP':response.status_code,'msg':http}
        except Exception as err:
            return {'status':'error','HTTP':response.status_code,'msg':err}
        else:
            return response.json()

    def ApplyCode(self,couponCode):
        '''
        This method applys promo code to the account
        
        Parameters
        ----------
        couponCode  :  The promo code that will be applied

        '''
        try :
            response=requests.get(self._Geturl('billing/applycode'),params={'couponCode':couponCode} ,headers=self.headers)
            response.raise_for_status()
        except HTTPError as http:
            return {'status':'error','HTTP':response.status_code,'msg':http}
        except Exception as err:
            return {'status':'error','HTTP':response.status_code,'msg':err}
        else:
            return {'status':'success','HTTP':response.status_code,'msg':f'Applied promo code:{couponCode} successfully'}
    
    def Stats(self,dateFrom=None,dateTo=None,pullZone=None,serverZoneId=None,loadErrors=True):
        '''
        This method returns the statistics associated with your account as json object
        
        Parameters
        ----------

        dateFrom        : string
        (optional)        The start date of the range the statistics should be returned for. Format: yyyy-mm-dd
        
        dateTo          : string
        (optional)        The end date of the range the statistics should be returned for. Format: yyyy-MM-dd
        
        pullZone        : int64
        (optional)        The ID of the Pull Zone for which the statistics should be returned
        
        serverZoneId    : int64
        (optional)        The server zone for which the data should be returned.
        
        loadErrors      : boolean
        (optional)        Set to true by default
        '''

        params={
            'dateFrom':dateFrom,
            'dateTo':dateTo,
            'pullZone':pullZone,
            'serverZoneId':serverZoneId,
            'loadErrors':loadErrors 
        }

        try :
            response=requests.get(self._Geturl('statistics'),params=params ,headers=self.headers)
            response.raise_for_status()
        except HTTPError as http:
            return {'status':'error','HTTP':response.status_code,'msg':http}
        except Exception as err:
            return {'status':'error','HTTP':response.status_code,'msg':err}
        else:
            return response.json()








           


                
               



        


        
        

                              


