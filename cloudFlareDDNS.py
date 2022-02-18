#! /usr/bin/python3
import os, requests, json

# Dynamic DNS script - Checks every x Minutes for current IP, perform matching to local file, and updates CloudFlare API if it has changed

zoneId = "INSERT ZONE ID HERE"
sicher = "INSET KEY HERE"
dnsId = "INSERT DNS ID HERE"
apiPath = f"https://api.cloudflare.com/client/v4/zones/{zoneId}/dns_records/{dnsId}"
awsChecker = "http://checkip.amazonaws.com"
isIpSynced = ""
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def checkDNS():
    global isIpSynced
    currentIp = requests.get("http://checkip.amazonaws.com").text.strip()
    dnsIp = ""
    localFile = open(os.path.join(__location__, 'currentIp.txt'), "r", encoding = "UTF-8")
    lastUpdatedIp = localFile.readline().strip()
    localFile.close()
    if lastUpdatedIp == True:
        if currentIp == lastUpdatedIp:           
            isIpSynced = True
            print('No Change to IP')
            return currentIp
        else:
            isIpSynced = False
            print('IP Update Required')
            return currentIp
    else:
        isIpSynced = False
        return currentIp
        

def updateDNS(currentIp):
    payload = json.dumps({
    "type": "A",
    "name": "blockgame.plss.top",
    "content": f"{currentIp}"
    })
    headers = {
    'Authorization': f'bearer {sicher}',
    'Content-Type': 'application/json',
    }
    print('DONE')

    # Sending Payload
    response = requests.request("PUT", apiPath, headers=headers, data=payload)
    print(response.text)

def updateFile(currentIp):
    with open(os.path.join(__location__, 'currentIp.txt'), "w", encoding = "UTF-8") as f:
        f.write(currentIp)
        f.close()

def getCloudFlareDNS():
    headers = {
    'Authorization': f'bearer {sicher}',
    'Content-Type': 'application/json',
    }

    response = requests.request("GET", apiPath, headers=headers)
    cloudFlareDNS = response.json['result']['content']
    print(f'latest DNS: {cloudFlareDNS}')
    return cloudFlareDNS



# Start the application
iptoUpdate = checkDNS()
updateFile(iptoUpdate)
if isIpSynced == False:
    updateDNS(iptoUpdate)
