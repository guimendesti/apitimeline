from flask import Flask, json
import requests

def requestEvents():
    url = "https://storage.googleapis.com/dito-questions/events.json"
    r = requests.get(url=url)
    return r.json()

def orderByTransaction(events):
    eventsorder = sorted(events['events'], key=lambda k: k['timestamp'], reverse=False)
    orders = {}
    for event in eventsorder:
        if "custom_data" in event:
            for customdata in event["custom_data"]:
                if "key" in customdata and "value" in customdata and customdata["key"] == "transaction_id":
                    transaction_id = customdata["value"]
                    if transaction_id not in orders:
                        orders[transaction_id] = []
                    orders[transaction_id].append(event)
                    break
    return orders


def groupByEventBuy(orders):
    groupdata = []
    for transaction_id, events in orders.iteritems():
        returnitem = {}
        returnitem["transaction_id"] = transaction_id
        returnitem["revenue"] = 0
        returnitem["products"] = []

        # event by store
        for event in events:
            productdata = {}
            if "event" in event:
                if "custom_data" in event:
                    for customdata in event["custom_data"]:
                        if "key" in customdata and "value" in customdata:
                            if customdata["key"] == "store_name":
                                returnitem["store_name"] = customdata["value"]
                                break

                            if customdata["key"] == "product_name":
                                productdata["name"] = customdata["value"]

                            if customdata["key"] == "product_price":
                                productdata["price"] = customdata["value"]

                if event["event"] == "comprou":
                    if "timestamp" in event:
                        returnitem["timestamp"] = event["timestamp"]
                else:
                    returnitem['products'].append(productdata)

        groupdata.append(returnitem)
    return groupdata


api = Flask(__name__)

@api.route('/timeline', methods=['GET'])
def getEventsTimeline():
    events = requestEvents();
    orders = orderByTransaction(events);
    timeline = groupByEventBuy(orders)
    objtimeline = {"timeline" : timeline }
    return json.dumps(objtimeline)

if __name__ == '__main__':
    api.run(port=8080)