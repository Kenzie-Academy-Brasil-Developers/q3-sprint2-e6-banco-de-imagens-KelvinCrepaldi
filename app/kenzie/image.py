from flask import send_file

from cgi import FieldStorage


from werkzeug.datastructures import FileStorage
import os

from app.kenzie import FILES_DIRECTORY

files_directory = os.getenv("FILES_DIRECTORY")
allowed_extensions = os.getenv("ALLOWED_EXTENSIONS").split(',')
max_content_length = os.getenv("MAX_CONTENT_LENGTH")

def file_already_exists(filename: str, extension: str) -> bool:

    extension_path = os.path.join(FILES_DIRECTORY, extension)

    return filename in os.listdir(extension_path)


def upload_image(file: FileStorage) -> None:
    
    filename: str = file.filename

    _, extension = os.path.splitext(filename)
    extension = extension.replace(".", "")

    if file_already_exists(filename, extension):
        raise FileExistsError

    saving_path = os.path.join(FILES_DIRECTORY, extension, filename)
    print(saving_path)
    file.save(saving_path)


def download_zip(file_type: str, compression_ratio: str):
    output_file = f"{file_type}.zip"
    input_path = os.path.join(FILES_DIRECTORY, file_type)
    output_path_file = os.path.join('/tmp', output_file)

    if os.path.isfile(output_path_file):
        os.remove(output_path_file)

    command = f"zip -r -j -{compression_ratio} {output_path_file} {input_path}"

    os.system(command)
    print('ziped')

    return send_file(output_path_file, as_attachment=True)

def list_files_presents():
    list_files = []
    for extension in allowed_extensions:
        if len(os.listdir(f"./files/{extension}")) != 0:
            list_files.append(' '.join(os.listdir(f"./files/{extension}")))
    if len(list_files) == 0:
        raise FileNotFoundError
    else:
        return ' '.join(list_files).split()

def list_files_per_extension(extension):
    list_files = []
    extension = extension.lower()
    if extension == "jpeg":
        extension = "jpg"
    try:
        list_files = os.listdir(f"./files/{extension}")
        if len(list_files) == 0:
            return {"message": f"Nenhum arquivo {extension} existe no servidor!"}
    except TypeError:
        raise FileNotFoundError
    
    return list_files