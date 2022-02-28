"""Functionality related to DynamoDB."""

import boto3
from datetime import datetime

TABLE_NAME = "TechForUkraine-CIG"

client = boto3.client("dynamodb", region_name="us-east-1")

def write_to_dynamo(country: str, event: object, general: list, reception: list, source: str):
    """
    Write the data to DynamoDB.

    Args:
        country (str): The name of the country.
        general (list[str]): More general information.
        reception (list): Border crossing points.
    """

    #######################################################################################################################################
    # USED FOR TESTING IN LAMBDA. Include 'testSuffix' in your lambda test object so that the dynamo items used in prod are not overwritten
    if event != "":
        testSuffix = "" if ('testSuffix' not in event) else event["testSuffix"]
        country += testSuffix
    #######################################################################################################################################

    # Get the existing object, that object will be PUT back into dynamo, but marked as 'old' so it can be compared.
    # The comparison will be used to determine if the translator needs to translate any of the newly scraped data or not.
    existingItem = get_existing_object(country)
    update_existing_item_as_old(existingItem)

    now = datetime.now()
    dateTimeString = now.strftime('%Y-%m-%d  %X  %z')
    isoString = now.isoformat()

    # Remove duplicate strings and create entries into the 'general' attribute of the dynamo item/object
    uniqueGeneralList = []
    general_list = []
    for line in general:
        if line not in uniqueGeneralList:
            uniqueGeneralList.append(line)
            general_list.append({ "S": line })

    reception_list = []
    for rec in reception:
        reception_list.append({
            "M": {
                "name": { "S": rec.name },
                "lat": { "S": rec.lat },
                "lon": { "S": rec.lon },
                "address": { "S": rec.address },
                "qr": { "S": rec.qr }
            }
        })

    client.put_item(
        TableName = TABLE_NAME,
        Item = {
            "country": { "S": country },
            "general": { "L": general_list },
            "reception": { "L": reception_list },
            "source": { "S": source },
            "isoFormat": { "S": isoString },
            "dateTime": { "S": dateTimeString }
        })

# Get the item from dynamo
def get_existing_object(country: str):
    return client.get_item(
        TableName = TABLE_NAME,
        Key = {
            'country': { 'S': country}
        }
    )["Item"]

# Change item name (appent -old) and PUT the item back in dynamo
def update_existing_item_as_old(item: object):
    item["country"]["S"] = item["country"]["S"] + "-old"

    client.put_item(
        TableName = TABLE_NAME,
        Item = item
    )