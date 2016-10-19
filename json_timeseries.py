import sys, getopt
import websocket
import json

def main(argv):
    input_file = argv[0]
    uaa = '''{
  "header": {
    "alg": "RS256",
    "kid": "legacy-token-key",
    "typ": "JWT"
  },
  "payload": {
    "jti": "d73ced66c357444595e71d9972ed7f76",
    "sub": "app_client_id",
    "scope": [
      "timeseries.zones.7de86dcd-074d-4383-88d1-d4f15746efe5.query",
      "uaa.resource",
      "openid",
      "uaa.none",
      "predix-asset.zones.ef39ad6c-9525-4209-8f18-f093ca50a9d0.user",
      "timeseries.zones.7de86dcd-074d-4383-88d1-d4f15746efe5.user",
      "timeseries.zones.7de86dcd-074d-4383-88d1-d4f15746efe5.ingest"
    ],
    "client_id": "app_client_id",
    "cid": "app_client_id",
    "azp": "app_client_id",
    "grant_type": "client_credentials",
    "rev_sig": "94597d8a",
    "iat": 1476899789,
    "exp": 1476942989,
    "iss": "https://6f54b399-ceb4-437e-8a94-b7f539c8e001.predix-uaa.run.aws-usw02-pr.ice.predix.io/oauth/token",
    "zid": "6f54b399-ceb4-437e-8a94-b7f539c8e001",
    "aud": [
      "timeseries.zones.7de86dcd-074d-4383-88d1-d4f15746efe5",
      "predix-asset.zones.ef39ad6c-9525-4209-8f18-f093ca50a9d0",
      "uaa",
      "openid",
      "app_client_id"
    ]
  }
}'''
    uri = "wss://gateway-predix-data-services.run.aws-usw02-pr.ice.predix.io/v1/stream/messages"
    zone_id = "7de86dcd-074d-4383-88d1-d4f15746efe5"
    origin = "run.aws-usw02-pr.ice.predix.io"
    elec_type = argv[1]
    with open(input_file) as data_file:
        data = json.load(data_file)
    openWSS(uaa, uri, zone_id, origin, data)

def send_first_data(ws, name):
    first_data = '''{
                      "messageId": ''' + name + ''',
                      "body":[
                         {
                            "name":"''' + name + '''",
                            "datapoints": ['''
    ws.send(first_data)

def send_datapoints(ws):
    datapoint = ""
    for n in PAYLOADS:
        datapoint = '''[
                        ''' + n[0] + '''
                        ''' + n[1] + '''
                        ''' + n[2] + '''
                       ]'''
        ws.send(datapoint)

def send_last_data(ws, elec_type):
    last_data = '''],
                "attributes":{
                              "type":"''' + elec_type + '''"
                              }
                           }
                        ]
                     }'''
    ws.send(last_data)

def sendPayload(ws):
    i = 0
    list_node = []
    timestamp_beg = 0
    timestamp_end = 0
    timestamp = 0
    name = ""
    value = 0
    quality = 0
    input_file = argv[0]
    payloads = []
    for dic in data:
        for series in data[i]:
            if (series == "ID"):
                name = data[i][series]
            elif (series == "TimeStampStart"):
                timestamp_beg = (int)(data[i][series])
                timestamp = timestamp_beg + (int)((timestamp_end - timestamp_beg) / 2)
            elif (series == "TimeStampEnd"):
                timestamp_end = (int)(data[i][series])
            elif (series == "y"):
                value = (float)(data[i][series])
            elif (series == "Quality"):
                quality = (int)(data[i][series])
        list_node = (timestamp, value, quality)
        if list_node:
            payloads += list_node
        i += 1

    send_first_data(ws, name)
    send_datapoints(ws, payloads)
    send_last_data(ws, elec_type)

def openWSS(uaaToken, tsUri, tsZone, origin, data):
    websocket.enableTrace(False)
    host = tsUri
    headers = {
                'Authorization:bearer ' + uaaToken,
                'Predix-Zone-Id:' + tsZone,
                'Origin:' + origin
    }
    ws = websocket.WebSocketApp(
                                host,
                                header = headers,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close
    )
    sendPayload(ws, data)

if __name__ == "__main__":
   main(sys.argv[1:])
