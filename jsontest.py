import sys, json

def main(argv):
    i = 0
    list_json = []
    list_node = []
    timestamp_beg = 0
    timestamp_end = 0
    timestamp = 0
    value = 0
    name = ""
    quality = 0
    input_file = argv[0]
    with open(input_file) as data_file:
        data = json.load(data_file)
    for dic in data:
        for series in data[i]:
            if (series == "ID") :
                name = data[i][series]
            if (series == "TimeStampStart"):
                timestamp_beg = (int)(data[i][series])
                timestamp = timestamp_beg + (int)((timestamp_end - timestamp_beg) / 2)
            elif (series == "TimeStampEnd"):
                timestamp_end = (int)(data[i][series])
            elif (series == "y"):
                value = (float)(data[i][series])
            elif (series == "Quality"):
                quality = (int)(data[i][series])
        list_node = (name, timestamp, value, quality)
        if list_node:
            print (list_node)
            list_json += list_node
        i += 1

if __name__ == "__main__":
   main(sys.argv[1:])
