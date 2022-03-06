"""Functionality related to DynamoDB."""
import boto3
from datetime import datetime

TABLE_NAME = "TechForUkraine-CIG"

client = boto3.client("dynamodb", region_name="us-east-1")


class DataLossError(Exception):
    """
    Exception representing catastrophic data loss.

    This would likely stem from the scraped website restructuring.
    """


def _check_for_data_loss(general: list, reception: list, old_item: dict):

    try:
        old_general = old_item["general"]["L"]
    except KeyError:
        old_general = []

    try:
        old_reception = old_item["reception"]["L"]
    except KeyError:
        old_reception = []

    def check_data(new, old):
        new_len = len(new)
        old_len = len(old)
        if old_len > 0 and new_len < 1:
            raise DataLossError()

    check_data(new=general, old=old_general)
    check_data(new=reception, old=old_reception)


def write_to_dynamo(
    country: str, event: object, general: list, reception: list, source: str
):
    """
    Write the data to DynamoDB.

    Args:
        country (str): The name of the country.
        event (str or dict?): The aws event that triggered the lambda?
        general (list[str]): More general information.
        reception (list): Border crossing points.
    """

    #######################################################################################################################################
    # USED FOR TESTING IN LAMBDA. Include 'testSuffix' in your lambda test object so that the dynamo items used in prod are not overwritten
    isTesting = False
    testSuffix = ""

    if event != "":
        if ("testSuffix" in event) and (event["testSuffix"] != ""):
            testSuffix = event["testSuffix"]
            isTesting = True
    #######################################################################################################################################

    # Remove any strings from the general array if they are empty/whitespace only (breaks translator otherwise)
    general = [x for x in general if x.strip()]

    now = datetime.now()
    dateTimeString = now.strftime("%Y-%m-%d  %X  %z")
    isoString = now.isoformat()

    # Remove duplicate strings and create entries into the 'general' attribute of the dynamo item/object
    uniqueGeneralList = []
    general_list = []
    for line in general:
        if line not in uniqueGeneralList:
            uniqueGeneralList.append(line)
            general_list.append({"S": line})

    reception_list = []
    for rec in reception:
        reception_list.append(
            {
                "M": {
                    "name": {"S": rec.name},
                    "lat": {"S": rec.lat},
                    "lon": {"S": rec.lon},
                    "address": {"S": rec.address},
                    "qr": {"S": rec.qr},
                }
            }
        )

    # If we're testing, we don't want to mess with exiting data that is being used by the website
    # So we write whatever we've scraped with a name that has a suffix defined in the lambda event.
    countryName = (country + testSuffix) if isTesting else country
    try:
        client.put_item(
            TableName=TABLE_NAME,
            Item={
                "country": {"S": countryName},
                "general": {"L": general_list},
                "reception": {"L": reception_list},
                "source": {"S": source},
                "isoFormat": {"S": isoString},
                "dateTime": {"S": dateTimeString},
            },
        )
        print("Successfully scraped " + countryName + " and inserted into DyanamoDB")
    except Exception as exception:
        print("An error occurred inserting " + countryName + " into DynamoDB")


# Get the item from dynamo
def get_existing_object(country: str):
    print("Getting dynamo object for country " + country)
    return client.get_item(TableName=TABLE_NAME, Key={"country": {"S": country}})[
        "Item"
    ]
