#!/usr/bin/python
import getpass
import os
import platform
import requests
import sys

def get_bluecat_token(usr, passwd):
    requests.packages.urllib3.disable_warnings()
    url = ''
    headers = {'content-type': 'application/json', 'cache-control': 'no-cache'}
    data = '{"username":"' + usr + '", "password":"' + passwd + '"}'
    print ('Getting token from BlueCat...')
    response = requests.post(url, headers=headers, data=data, verify=False)
    if response.status_code is 200:
        print ('Token acquired...')
        return response.json()['access_token']
    else:
        print ('Failed to get token. API Response was:')
        exit()


def get_bluecat_subnet(token, fqdn, ip):
    requests.packages.urllib3.disable_warnings()
    url = ''
    headers = {
        'auth': 'Basic {}'.format(token),
        'content-type': 'application/json',
        'cache-control': 'no-cache'
        }


    data = '{"fqdn":"' + fqdn + '", "ip":"' + ip + '"}'
    response = requests.request('POST', url, headers=headers, data=data, verify=False)

    if response.status_code is 200:
        output = response.json()
        if output.get('error'):
            return 'Host Not Created'
        else:
            return output.get('success').split()[2]
    else:
        print ('Failed API Response was:\n')
        print ('Status Code: {}').format(response.status_code)
        print ('Description: {}').format(response.json()['description'])
        print ('Status: {}').format(response.json()['status'])
        exit()


def main():
    usr = str(sys.argv[1])
    passwd = str(sys.argv[2])
    fqdn = str(sys.argv[3])
    ip = str(sys.argv[4])

    token = get_bluecat_token(usr, passwd)
    hostname = get_bluecat_subnet(token, fqdn, ip)
    print (hostname)


if __name__ == '__main__':
    main()
