"""Functionality related to DynamoDB."""

import boto3

TABLE_NAME = 'TechForUkraine-CIG'

def save(country: str, general: list, reception: list, source: str):
    """
    Write the data to DynamoDB.

    Args:
        country (str): The name of the country.
        general (list[str]): More general information.
        reception (list): Border crossing points.
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)

    reception_list = []
    for rec in reception:
        reception_list.append({
        "name": { "S": rec.name },
        "lat": { "S": rec.lat },
        "lon": { "S": rec.lon },
        "address": { "S": rec.address },
        "qr": { "S": rec.qr },
        })

    table.put_item(Item={
        "country": { "S": country },
        "general": { "SS": general },
        "reception": reception_list,
        "source": { "S": source }
    })
