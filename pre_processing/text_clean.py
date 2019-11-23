import logging
import re


def get_cleaned_text(text):
    try:
        text = str(text)
        text = text.replace('\n', ' ')  # First of all get rid of line breaking
        text = text.replace('&nbsp', ' ')  # Some news contains &nbsp, remove them

        text = re.sub(r'\((.*?)\)', ' ', text)  # Remove ('text')
        text = re.sub(r'\[(.*?)\]', ' ', text)  # Remove ['text']
        text = re.sub(r'\{(.*?)\}', ' ', text)  # Remove {'text'}
        text = re.sub(r'</?\w+[^>]*>', ' ', text)  # Remove <'text'>
        text = re.sub(r'\S*@\S*\s?', ' ', text)  # Remove emails
        text = re.sub(r'http\S+', ' ', text)  # Remove URLs

        text = re.sub(r'''[^a-zA-Z0-9,;'":$]+''', ' ', text)

        text = text.replace(' s ', ' ')  # Remove signal 's' after remove signal quotes

    except Exception as e:
        logging.info('Error occurred while pre_processing the text')
        logging.info(e)

    return text
