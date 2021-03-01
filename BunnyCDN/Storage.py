"""This code is to use the BunnyCDN Storage API"""

import os
import requests
from requests.exceptions import HTTPError


class Storage:

    # initializer for storage account

    def __init__(self, api_key, storage_zone, storage_zone_region="de"):
        """
        Creates an object for using BunnyCDN Storage API
        Parameters
        ----------
        api_key                                 : String
                                                  Your bunnycdn storage
                                                  Apikey/FTP password of
                                                  storage zone

        storage_zone                            : String
                                                  Name of your storage zone

        storage_zone_region(optional parameter) : String
                                                  The storage zone region code
                                                  as per BunnyCDN
        """
        self.headers = {
            # headers to be passed in HTTP requests
            "AccessKey": api_key,
            "Content-Type": "application/json",
            "Accept": "applcation/json",
        }

        # applying constraint that storage_zone must be specified
        assert storage_zone != "", "storage_zone is not specified/missing"

        # For generating base_url for sending requests
        if storage_zone_region == "de" or storage_zone_region == "":
            self.base_url = "https://storage.bunnycdn.com/" + storage_zone + "/"
        else:
            self.base_url = (
                "https://"
                + storage_zone_region
                + ".storage.bunnycdn.com/"
                + storage_zone
                + "/"
            )

    def DownloadFile(self, storage_path, download_path=os.getcwd()):
        """
        This function will get the files and subfolders of storage zone mentioned in path
        and download it to the download_path location mentioned
        Parameters
        ----------
        storage_path  : String
                        The path of the directory
                        (including file name and excluding storage zone name)
                        from which files are to be retrieved
        download_path : String
                        The directory on local server to which downloaded file must be saved
        Note:For download_path instead of '\' '\\' should be used example: C:\\Users\\XYZ\\OneDrive
        """

        assert (
            storage_path != ""
        ), "storage_path must be specified"  # to make sure storage_path is not null
        # to build correct url
        if storage_path[0] == "/":
            storage_path = storage_path[1:]
        if storage_path[-1] == "/":
            storage_path = storage_path[:-1]
        url = self.base_url + storage_path
        file_name = url.split("/")[-1]  # For storing file name

        # to return appropriate help messages if file is present or not and download file if present
        try:
            response = requests.get(url, headers=self.headers, stream=True)
            response.raise_for_status()
        except HTTPError as http:
            return {
                "status": "error",
                "HTTP": response.status_code,
                "msg": f"Http error occured {http}",
            }
        except Exception as err:
            return {
                "status": "error",
                "HTTP": response.status_code,
                "msg": f"error occured {err}",
            }
        else:
            download_path = os.path.join(download_path, file_name)
            # Downloading file
            with open(download_path, "wb") as file:

                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
                return {
                    "status": "success",
                    "HTTP": response.status_code,
                    "msg": "File downloaded Successfully",
                }

    def PutFile(
        self,
        file_name,
        storage_path=None,
        local_upload_file_path=os.getcwd(),
    ):

        """
        This function uploads files to your BunnyCDN storage zone
        Parameters
        ----------
        storage_path                : String
                                      The path of directory in storage zone
                                      (including the name of file as desired and excluding storage zone name)
                                      to which file is to be uploaded
        file_name                   : String
                                      The name of the file as stored in local server
        local_upload_file_path      : String
                                      The path of file as stored in local server(excluding file name)
                                      from where file is to be uploaded
        Examples
        --------
        file_name                   : 'ABC.txt'
        local_upload_file_path      : 'C:\\User\\Sample_Directory'
        storage_path                : '<Directory name in storage zone>/<file name as to be uploaded on storage zone>.txt'
                                        #Here .txt because the file being uploaded in example is txt
        """
        local_upload_file_path = os.path.join(local_upload_file_path, file_name)

        # to build correct url
        if storage_path is not None and storage_path != "":
            if storage_path[0] == "/":
                storage_path = storage_path[1:]
            if storage_path[-1] == "/":
                storage_path = storage_path[:-1]
            url = self.base_url + storage_path
        else:
            url = self.base_url + file_name
        with open(local_upload_file_path, "rb") as file:
            file_data = file.read()
        response = requests.put(url, data=file_data, headers=self.headers)
        try:
            response.raise_for_status()
        except HTTPError as http:
            return {
                "status": "error",
                "HTTP": response.status_code,
                "msg": f"Upload Failed HTTP Error Occured: {http}",
            }
        else:
            return {
                "status": "success",
                "HTTP": response.status_code,
                "msg": "The File Upload was Successful",
            }

    def DeleteFile(self, storage_path=""):
        """
        This function deletes a file mentioned in the storage_path from the storage zone
        Parameters
        ----------
        storage_path : The directory path to your file(including file name) which is to be deleted.
                       If this is the root of your storage zone, you can ignore this parameter.
        """
        # Add code below
        assert (
            storage_path != ""
        ), "storage_path must be specified"  # to make sure storage_path is not null
        # to build correct url
        if storage_path[0] == "/":
            storage_path = storage_path[1:]
        if storage_path[-1] == "/":
            storage_path = storage_path[:-1]
        url = self.base_url + storage_path

        try:
            response = requests.delete(url, headers=self.headers)
            response.raise_for_status
        except HTTPError as http:
            return {
                "status": "error",
                "HTTP": response.raise_for_status(),
                "msg": f"HTTP Error occured: {http}",
            }
        except Exception as err:
            return {
                "status": "error",
                "HTTP": response.status_code,
                "msg": f"Object Delete failed ,Error occured:{err}",
            }
        else:
            return {
                "status": "success",
                "HTTP": response.status_code,
                "msg": "Object Successfully Deleted",
            }

    def GetStoragedObjectsList(self, storage_path=None):
        """
        This functions returns a list of files and directories located in given storage_path.
        Parameters
        ----------
        storage_path : The directory path that you want to list.
        """
        # to build correct url
        if storage_path is not None:
            if storage_path[0] == "/":
                storage_path = storage_path[1:]
            if storage_path[-1] != "/":
                url = self.base_url + storage_path + "/"
        else:
            url = self.base_url
        # Sending GET request
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
        except HTTPError as http:
            return {
                "status": "error",
                "HTTP": response.status_code,
                "msg": f"http error occured {http}",
            }
        else:
            storage_list = []
            for dictionary in response.json():
                temp_dict = {}
                for key in dictionary:
                    if key == "ObjectName" and dictionary["IsDirectory"] is False:
                        temp_dict["File_Name"] = dictionary[key]
                    if key == "ObjectName" and dictionary["IsDirectory"]:
                        temp_dict["Folder_Name"] = dictionary[key]
                storage_list.append(temp_dict)
            return storage_list
