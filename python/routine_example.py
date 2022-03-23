from up2data import Up2data

up2data = Up2data()

# Getting the latest available closed day date
string_date = up2data.get_last_weekday()

# Wanted channels and information
channel = 'Market Channels'
channel_info = ['Currency', 'Commodities']

# Authentication and generating the wanted channels blob urls
headers = up2data.define_headers()
auth_headers = up2data.get_auth_token(headers=headers)
sas_urls = up2data.generate_sas(headers=auth_headers)
blob_url = up2data.get_blob_url(sas_urls=sas_urls, channel=channel)

for info in channel_info:
    src_url = up2data.generate_source_url(string_date, blob_url, info)
    azcopy_command = up2data.generate_azcopy_cmd(source_url=src_url)
    up2data.execute_comand(azcopy_command)
    print(f'data from {string_date}/{info} has been downloaded!!')
