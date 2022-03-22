import subprocess
import datetime
import json
import requests
import os
import configparser

class Up2data:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("<config file path>") # config.ini
        self.clientId = config.get('KEYS', 'clientId')
        self.clientSecret = config.get('KEYS', 'clientSecret')
        self.password = config.get('KEYS', 'password')
        self.input_path = config.get('PATH', 'input_path')
        self.destination_path = config.get('PATH', 'destination_path')
        self.market_channels = {
            'Commodities': 'SettlementPrice',
            'Currency': 'SettlementPrice'
        }

    def get_date(self) -> str:
        """The functions returns the last business/weekday

        Returns:
            str: the last business day in a specific date format "YYYYMMDD" as a string
        """        
        today = datetime.date.today()
        weekends = ['Saturday', 'Sunday']
        lookup_date = True
        n = 1
        while lookup_date:
            yesterday = today - datetime.timedelta(days=n)
            yesterday_name = yesterday.strftime('%A')
            if yesterday_name in weekends:
                n += 1
            else:
                lookup_date = False
        string_date = self.format_date(yesterday)
        return string_date

    def format_date(self, date: datetime.date) -> str:
        """formats a date object into a string to fit formatting needs

        Args:
            date (datetime.date): last business day

        Returns:
            str: the last business day in a specific date format "YYYYMMDD" as a string
        """        
        day = date.day
        month = date.month
        year = date.year
        string_date = f'{year}{month:02d}{day:02d}'
        return string_date

    def define_headers(self) -> dict:
        """defines the initial headers to be passed into the token api

        Returns:
            dict: headers for the token api
        """        
        headers = {
            'clientId': self.clientId,
            'clientSecret': self.clientSecret,
            'password': self.password
        }
        with open(os.path.join(self.input_path, 'base64.txt')) as f:
            cert = f.read()
        
        headers['certificate'] = cert
        return headers

    def get_auth_token(self, headers: dict) -> dict:
        """does a post request to the token api and retrives an auth token,
        the token is also added to the headers dict to be used on the SaS api

        Args:
            headers (dict): initial headers dict

        Returns:
            dict: headers with auth token
        """        
        token_url = 'https://up2data.b3.com.br/cloud/oauth/token'
        r = requests.post(token_url, headers=headers)
        json_response = r.json()
        sas_token = json_response['access_token']
        headers['Authorization'] = f'Bearer {sas_token}'
        return headers

    def generate_sas(self, headers: dict) -> json:
        """Does a post request authenticated by the initial headers provided by the company,
        and the token obtained through them, that returns a json response with all the available blob containers

        Args:
            headers (dict): headers for client authentication

        Returns:
            json: json object that contains the diferent blob containers names and their urls
        """        
        sas_url = 'https://up2data.b3.com.br/cloud/storage/sas'
        r = requests.post(sas_url, headers=headers)
        json_response = r.json()
        return json_response

    def get_blob_url(self, sas_urls: json, channel: str) -> str:
        """Looks for the desired blob cointainer by the name and returns it's url

        Args:
            sas_urls (json): json object with all the containers
            channel (str): string containing the desired channel(container)

        Returns:
            str: url for the desired channel
        """        
        for blob in sas_urls:
            if channel in blob['name']:
                blob_url = blob['sas']
                return blob_url

    def generate_source_url(self, str_date: str, blob_url: str, channel_info: str) -> str:
        """concatenates the arguments to create the source url for the azcopy command

        Args:
            str_date (str): date to be used in the filter
            blob_url (str): core container url
            channel_info (str): information desired from that channel (eg. Currency)

        Returns:
            str: the complete source url with the applied filters by the prefix
        """        
        info_type = self.market_channels[channel_info]
        prefix = f'prefix={str_date}/{channel_info}/{info_type}'
        source_url = f'{blob_url}&{prefix}'
        return source_url

    def generate_azcopy_cmd(self, source_url: str) -> str:
        """concatenates the source_url, destination_path, type_filters and the azcopy command sytax
        into a sigle string to be passed as a shell command later on

        Args:
            source_url (str): source url with the path to the wanted data on the blob

        Returns:
            str: full command string
        """        
        type_filter = '--include-pattern "*.csv"'
        azcopy_command = f'azcopy copy "{source_url}" "{self.destination_path}" {type_filter} --recursive'
        return azcopy_command

    def execute_comand(self, command: str):
        """executes a shell command using azcopy

        Args:
            command (str): string containing the full azcopy command to be executed
        """        
        subprocess.run(command, shell=True, stdout=subprocess.PIPE)


