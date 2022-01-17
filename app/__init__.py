# Desenvolva suas rotas aqui
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.datastructures import ImmutableMultiDict, FileStorage
from app.kenzie import image
from os import getenv

MAX_CONTENT_LENGTH = int(getenv("MAX_CONTENT_LENGTH"))

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH * 1024 * 1024

@app.post("/upload")
def upload():
    files: ImmutableMultiDict[str, FileStorage] = request.files

    for file in files.values():
        try:
            image.upload_image(file)
        except FileExistsError:
            return {"msg": "Arquivo já existe."}, 409
        except FileNotFoundError:
            return {"msg": "Extensão não suportada."}, 415
    return {"message" : "Upload realizado com sucesso!"}, 201

@app.get("/download-zip")
def download_dir_as_zip():
    try:
        file_type = request.args.get("file_extension")
        compression_ratio = request.args.get("compression_ratio", 6)

        if not file_type:
            return {"msg" : "Query param `file_extension` é obrigatório."}, 400
        
        return image.download_zip(file_type, compression_ratio)
    except(FileNotFoundError):
        return {"message": "Arquivos não foram encontrados."}, 404
    

@app.errorhandler(413)
def too_big(error):
    return {'msg': f"O arquivo ultrapassa o limite permitido de {MAX_CONTENT_LENGTH}MB"}, 413


@app.get("/files/")
def list_files():
    try:
        files = image.list_files_presents()
    except (FileNotFoundError):
        return {"message": "Ainda não existem arquivos armazenados!"}, 404
    return jsonify(files), 200

@app.get("/files/<extension>")
def extension_list_files(extension):
    try:
        files = image.list_files_per_extension(extension)
        return jsonify(files), 200
    except FileNotFoundError:
        return {"message": "Tipo de arquivo não permitido pelo sistema."}, 404


@app.get("/download/<file_name>")
def download(file_name):
    extension = file_name.split(".")[1]
    try:
        return send_from_directory(
            directory=f"../files/{extension}",
            path=f"{file_name}",
            as_attachment=True
        )
    except:
        return {"message": "Arquivo não encontrado"}, 404