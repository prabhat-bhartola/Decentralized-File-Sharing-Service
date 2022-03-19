"""
Contains usefull functions like finding the next name for a file etc.
"""
import os

def parse_type(fileName):
    """
    Returns the file type from string

    Parameters
    ----------
    fileName : str -> 
    """
    return fileName.split(".")[-1]


def parse_path(fileName):
    """
    Returns the file path from string

    Parameters
    ----------
    fileName : str ->
    """
    pathList = fileName.split("/")
    del pathList[-1]

    pathStr = "\\".join(pathList)

    return pathStr

def parse_name(fileName):
    """
    Returns the file name from full path

    Parameters
    ----------
    fileName : str ->
    """
    pathList = fileName.split("/")
    name = pathList[-1]

    return name

def get_type_from_ext(file_name):
    """
    Determines and returns file type from file name
    """
    file_type = ""

    if file_type.lower() in ("png", "jpg", "jpeg"):
        file_type = "Image"
    elif file_type.lower() in ("mp4", "avi", "mpeg", "mov", "wmv"):
        file_type = "Video"
    elif file_type.lower() in ("wav", "mp3", "flac"):
        file_type = "Audio"
    elif file_type.lower() in ("rar", "tar.lz"):
        file_type = "Compressed"
    else:
        file_type = "."+parse_type(file_name)
    
    return file_type
