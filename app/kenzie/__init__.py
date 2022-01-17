import os 

FILES_DIRECTORY = os.getenv("FILES_DIRECTORY")
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")

def create_dirs() -> None:
    #['jpg', 'gif, 'png']
    for ext in ALLOWED_EXTENSIONS.split(","):
        path = os.path.join(FILES_DIRECTORY, ext)

        if not os.path.exists(path):
            os.makedirs(path)

create_dirs()