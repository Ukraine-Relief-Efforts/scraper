"""Functionality related to DynamoDB."""

import boto3

TABLE_NAME = 'TechForUkraine-CIG'


def save(country: str, general: set, reception: list):
    """
    Write the data to DynamoDB.

    Args:
        country (str): The name of the country.
        general (set[str]): More general information.
        reception (list[str]): Information on locations available to receive
            refugees (I think?  I can't actually read the sample data).
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)

    table.put_item(Item={
        'country': country,
        'general': general,
        'reception': reception
    })
