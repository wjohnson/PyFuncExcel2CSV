import json
import logging
import os

from azure.storage.blob import BlobServiceClient, BlobClient
import pandas as pd

import azure.functions as func


def main(event: func.EventGridEvent):
    result = json.dumps({
        'id': event.id,
        'data': event.get_json(),
        'topic': event.topic,
        'subject': event.subject,
        'event_type': event.event_type,
    })
    connect_str = os.getenv('STORAGE_CONNECTION')
    input_container = os.getenv('INPUT_CONTAINER')
    output_container = os.getenv('OUTPUT_CONTAINER')
    
    url_of_blob = None
    blob_name = None
    try:
        data_of_event = event.get_json()
        url_of_blob = data_of_event.get('url', None)

        split_url = url_of_blob.split('/')
        # https://storageaccount.blob.core.windows.net/container/blobname/test.xlsx
        blob_name = '/'.join(split_url[4:])
        container_name = split_url[3]
    except Exception as e:

        logging.info('Python EventGrid Failed to process this event: %s', result)
        logging.info('%s', e)
        return None
    
    if url_of_blob is None:
        logging.info('There was no blob url in this event: %s', result)
        return None
    
    if container_name != input_container:
        logging.info("Triggered for an irrelevant event on the {} container".format(container_name))
        return None

    # Download the blob
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    input_excel = blob_service_client.get_blob_client(container= container_name, blob = blob_name)

    original_file_name, _ = os.path.splitext(blob_name)
    new_file_name = "{}.csv".format(original_file_name)
    
    # Define a temporary location to store the csv
    upload_file_path = "./{}".format(new_file_name)
    df = pd.read_excel(input_excel.download_blob().readall())

    # Save the excel as a dataframe (and omit the auto-generated index)
    df.to_csv(upload_file_path, index=False)

    output_csv = blob_service_client.get_blob_client(
        container=output_container, 
        blob = new_file_name
    )

    # Upload the created file
    with open(upload_file_path, "rb") as data:
        output_csv.upload_blob(data)

    logging.info("Success!")

    logging.info('Python EventGrid trigger processed an event: %s', result)
