#!/usr/bin/env python3
import requests
import pprint
import sys
from functools import lru_cache

@lru_cache(maxsize=1)
def get_settings():
    from os.path import expanduser, realpath, join, dirname, isfile
    possible_location = [expanduser("~"), dirname(realpath(__file__))]
    settings={}
    for path in possible_location:
        config_file=join(path,'.nanoleaf')
        if isfile(config_file):
            with open(config_file,'r') as config_file_obj:
                for line in config_file_obj.readlines():
                    confdata=line.strip().split(';')
                    data={
                      "ip" : confdata[1],
                      "key" : confdata[2]
                      }
                    settings[confdata[0]]=data
    return settings



def get_ip(name):
    for x in get_settings():
        if x.startswith(name):
            return get_settings()[x]["ip"]

def get_key(name):
    for x in get_settings():
        if x.startswith(name):
            return get_settings()[x]["key"]

def get_url(name):
    return 'http://'+ get_ip(name) +':16021/api/v1/' + get_key(name) + '/'

def is_online(name):
    url = 'http://'+ get_ip(name) +':16021/'
    try:
        response = requests.request(url=url,method="GET", timeout=0.1)
        return True
    except requests.exceptions.ConnectTimeout as e:
        return False


def get_infos(name):
    url = get_url(name)
    response = requests.request(url=url,method="GET")
    print(response.text)

def is_on(name):
    url= get_url(name) + "state/on/value"
    response = requests.get(url=url)
    return ("true" in response.text)

def set_state(name,value):
    payload = "{\n  \"on\": {\n    \"value\": " + value + "\n  }\n}"
    headers = { 'Content-Type': 'application/json'  }
    url= get_url(name) + "state"
    response=requests.request('PUT',url,headers=headers,data=payload)
    print(response.text)

def get_state(name):
    url = get_url(name)+"state"
    response = requests.request(url=url,method="GET")
    print(response.text)

def get_brightness(name):
    url = get_url(name)+"state/brightness"
    response = requests.request(url=url,method="GET")
    print(response.text)

def set_brightness(name,value,time=2):
    payload = "{\"brightness\" : {\"value\":"+str(value)+", \"duration\":"+str(time)+"}}"
    headers = { 'Content-Type': 'application/json'  }
    # headers = {}
    url= get_url(name) + "state"
    response=requests.request('PUT',url,headers=headers,data=payload)
    print(response.text)

def get_effects(name):
    url=get_url(name)+"effects/effectsList"
    response = requests.request(url=url,method="GET")
    print(response.text)

def set_effect(name_lamp, name_effect):
    url = get_url(name_lamp) + 'effects'
    payload = "{\"select\" : \"" + name_effect + "\"}"
    headers = { 'Content-Type': 'application/json' }
    response = requests.request('PUT', url, headers = headers, data = payload)
    print(response.text)

def toggle(name):
    if is_online(name):
        if is_on(name):
            set_state(name,"false")
        else:
            set_state(name,"true")
    else:
        print("Offline")

if __name__ == "__main__":
    if len(sys.argv)>1:
        arguments=sys.argv[1:]
        if arguments[0]=="get":
            if arguments[1]=="effects":
                get_effects(arguments[-1])
            if arguments[1]=="brightness":
                get_brightness(arguments[-1])
            if arguments[1]=="state":
                get_state(arguments[-1])
        if arguments[0]=="set":
            if arguments[1]=="effects":
                name=arguments[2]
                effect=arguments[3]
                set_effect(name,effects)
            if arguments[1]=="brightness":
                if len(arguments)==4:
                    name=arguments[2]
                    brightness=arguments[3]
                    set_brightness(name,brightness)
                if len(arguments)==5:
                    name=arguments[2]
                    brightness=arguments[3]
                    duration=arguments[4]
                    set_brightness(name,brightness,duration)
        elif len(arguments)==1:
            toggle(arguments[0])
