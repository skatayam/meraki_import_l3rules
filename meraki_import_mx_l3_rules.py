# -*- coding: utf-8 -*-
import sys
import requests
from jinja2 import Template, Environment, FileSystemLoader
import csv

args = sys.argv

baseUrl = "https://api.meraki.com/api/v1"
apikey = "YOUR_MERAKI_API_KEY"
netid = "YOUR_NETWROK_ID"


def main():
    headers = {'X-Cisco-Meraki-API-Key': apikey, 'Content-Type': 'application/json'}
    api_url = baseUrl + '/networks/' + netid + '/appliance/firewall/l3FirewallRules'

    try:
        r = None
        env = Environment(loader=FileSystemLoader('./templates'))
        template = env.get_template('meraki_policy.j2')

        data = [i for i in csv.DictReader(open(args[1]))]
        post_data = template.render({"data": data})

        print(post_data)

        r = requests.put(api_url, data=post_data, headers=headers)
        status_code = r.status_code
        resp = r.text
        print("Status code is: " + str(status_code))
        if status_code == 200:
            print("Update L3 firewall rule was successful...")
            return resp
        else:
            print("Error occurred in POST L3 firewall rule --> " + resp)
    except requests.exceptions.HTTPError as err:
        print("Error in connection --> " + str(err))
    finally:
        if r: r.close()

if __name__ == '__main__':
    main()