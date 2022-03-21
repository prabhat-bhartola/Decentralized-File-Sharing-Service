"""
Contains usefull functions like finding the next name for a file etc.
"""
import os

def parse_type(fileName):
    """
    Returns the filetype in lower from string

    Parameters
    ----------
    fileName : str -> 
    """
    return fileName.split(".")[-1].lower()


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
    try:
        file_type = ""

        if parse_type(file_name) in ("png", "jpg", "jpeg", "svg"):
            file_type = "Image"
        elif parse_type(file_name) in ("mp4", "avi", "mpeg", "mov", "wmv"):
            file_type = "Video"
        elif parse_type(file_name) in ("wav", "mp3", "flac"):
            file_type = "Audio"
        elif parse_type(file_name) in ("rar", "tar.lz", "zip"):
            file_type = "Compressed"
        elif parse_type(file_name) in ("pdf"):
            file_type = "PDF"
        elif parse_type(file_name) in ("exe"):
            file_type = "Executable"
        else:
            file_type = "."+parse_type(file_name)
        
        return file_type
    except Exception as e:
        print(e)
