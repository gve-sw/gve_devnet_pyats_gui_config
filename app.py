""" Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. 
"""

# Import Section
from flask import Flask, render_template, request, url_for, redirect
from collections import defaultdict
import datetime
import requests
import json
from dotenv import load_dotenv
import os
from networking import update_port_vlan, copy_port_config, assign_vlan_ip_address
import traceback


# load all environment variables
load_dotenv()


# Global variables
app = Flask(__name__)


@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/progress')
def ajax_index():
    global i
    i+=20
    print(i)
    return str(i)

# Methods
# Returns location and time of accessing device
def getSystemTimeAndLocation():
    # request user ip
    userIPRequest = requests.get('https://get.geojs.io/v1/ip.json')
    userIP = userIPRequest.json()['ip']

    # request geo information based on ip
    geoRequestURL = 'https://get.geojs.io/v1/ip/geo/' + userIP + '.json'
    geoRequest = requests.get(geoRequestURL)
    geoData = geoRequest.json()
    
    #create info string
    location = geoData['country']
    timezone = geoData['timezone']
    current_time=datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")
    timeAndLocation = "System Information: {}, {} (Timezone: {})".format(location, current_time, timezone)
    
    return timeAndLocation

##Routes
#Instructions
@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "GET":
        try:
            #Page without error message and defined header links
            return render_template('update_form.html', hiddenLinks=False, timeAndLocation=getSystemTimeAndLocation())
        except Exception as e:
            print(e)
            #OR the following to show error message
            return render_template('update_form.html', error=False, errormessage="CUSTOMIZE: Add custom message here.", errorcode=e, timeAndLocation=getSystemTimeAndLocation())

    else:
        try:
            print(request.form)

            # Management IP Address
            management_ip = request.form['management-ip']

            # Assign IP to VLAN
            if 'vlan-interface' and 'ip-address-interface-vlan' and 'subnet-mask-interface-vlan' in request.form:
                if request.form['vlan-interface'] and request.form['ip-address-interface-vlan'] and request.form['subnet-mask-interface-vlan'] != '':
                    assign_ip_vlan_interface = request.form['vlan-interface']
                    assign_ip_address = request.form['ip-address-interface-vlan']
                    assign_ip_subnet_mask = request.form['subnet-mask-interface-vlan']

                    assign_vlan_ip_address(vlan=assign_ip_vlan_interface, device_ip=management_ip, ip_assignment=assign_ip_address, subnet_assignment=assign_ip_subnet_mask)



            # Assign VLAN to Interface
            if 'interface-name-vlan' and 'VLAN Number' in request.form:
                if request.form['interface-name-vlan'] and request.form['VLAN Number'] != '':
                    assign_vlan_interface_name = request.form['interface-name-vlan']
                    assign_vlan_number = request.form['VLAN Number']

                    update_port_vlan(device_ip=management_ip,interface=assign_vlan_interface_name, vlan=assign_vlan_number, mode="access")

            # Copy Port Config
            if 'source-interface' and 'destination-interface' in request.form:
                if request.form['source-interface'] and request.form['destination-interface'] != '':
                    copy_port_source_interface = request.form['source-interface']
                    copy_port_destination_interface = request.form['destination-interface']

                    copy_port_config(device_ip=management_ip, source_port=copy_port_source_interface, destination_port=copy_port_destination_interface)





            return render_template('update_form.html', hiddenLinks=False, timeAndLocation=getSystemTimeAndLocation())

        except Exception as e:
            print(traceback.format_exc())

            return e


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=9000, debug=True)