import base64
import os
import tempfile

def save_uploaded_files(list_of_contents, list_of_files):

    """
    Description
    -----
        Takes contents and filenames from dcc.Upload decode and save the files 
        temporally.

    Args
    -----
    :param list list_of_contents: from dcc.Upload "contents" property.
    :param list list_of_files: from dcc.Upload "filename" property.
    :return list: filepaths

    """

    if list_of_contents is None:
        return []
    
    filepaths= []

    for content, filename in zip(list_of_contents, list_of_files):
        _, content_string= content.split(",")
        decoded_bytes= base64.b64decode(content_string)

        with tempfile.NamedTemporaryFile(delete=False, suffix=filename) as tmp:
            tmp.write(decoded_bytes)
            filepath= tmp.name
            filepaths.append(filepath)

    return filepaths
