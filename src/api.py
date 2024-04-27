import requests
import logging

"""
This is a wrapper class for SSLLabs
"""
class SSLlabsApiClient:
    def __init__(self, logger:logging.Logger, base_url:str="https://api.ssllabs.com/api/v4", email:str=None):
        self.base_url = base_url.rstrip('/')
        self.email = email
        self.logger = logger
  
    def register(self, firstName:str, lastName:str, email:str, organization:str):
        url = f'{self.base_url}/register'
        headers = {'Content-Type': 'application/json'}
        data = {
            'firstName' : firstName,
            'lastName' : lastName,
            'email': email,
            'organization': organization
        }        
        response = requests.post(url, headers=headers, json=data)
        if response.ok:
            self.logger.info(f"API email: {email} registered successfully!")
            self.email = email
            return True
        else:
            self.logger.error(response.json()["errors"][0]["message"])
            return False
    
    def is_api_available(self)->bool:
        url = f'{self.base_url}/info'
        response = requests.get(url)
        if response.ok:
            self.logger.info("API is available and ready for use")
            return True
        else:
            self.logger.error("Error checking API availability")
            self.logger.error(response.json()["errors"][0]["message"])
        return False

    def get_ssl_scan_results(self, hostname:str):
        url = f'{self.base_url}/analyze?host={hostname}&publish=off&all=done'
        headers = {"email": self.email}
        response = requests.get(url, headers=headers)
        
        if response.ok:
            self.logger.info(f'API {url} executed successfully')
            return response.json()
        else:
            self.logger.error(response.json()["errors"][0]["message"])
            return None
        
    def get_endpoint_data(self, hostname:str, ip:str, fromCache:str="off"):
        headers = {"email": self.email}
        url = f'{self.base_url}/getEndpointData?host={hostname}&s={ip}&fromCache={fromCache}'
        response = requests.get(url, headers=headers)
        return response

    def get_status_codes(self):
        url = f'{self.base_url}/getStatusCodes'
        response = requests.get(url)
        if response.ok:
            return response.json()["statusDetails"]
        else:       
            self.logger.error(response.json()["errors"][0]["message"])
            return None
