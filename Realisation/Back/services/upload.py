import os
import shutil
from fastapi import UploadFile

UPLOAD_DIR = "uploads"

EXTENSIONS = {".pdf", ".docx", ".txt", ".doc", ".md"}


