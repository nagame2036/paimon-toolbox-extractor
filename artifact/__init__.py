from artifact.artifact_data import write_artifact_data
from artifact.artifact_i18n import write_artifact_i18n
from artifact.artifact_image import write_artifact_image
from artifact.artifact_meta import *


def write_data():
    write_artifact_data()


def write_i18n():
    write_artifact_i18n()


def write_image():
    write_artifact_image()
