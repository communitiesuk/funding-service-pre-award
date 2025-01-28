import os
import shutil
import urllib.request
import zipfile


def build_assets():
    # Download zips using "url"
    print("Downloading static file zip.")

    url = "https://github.com/alphagov/govuk-frontend/releases/download/v5.7.1/release-v5.7.1.zip"

    # There is a known problem on Mac where one must manually
    # run the script "Install Certificates.command" found
    # in the python application folder for this to work.
    urllib.request.urlretrieve(url, "./govuk_frontend.zip")  # nosec

    print("Deleting old static")

    # Attempts to delete the old files, states if
    # one doesnt exist.
    try:
        shutil.rmtree("static")
    except FileNotFoundError:
        print("No old static to remove.")

    print("Unzipping file to static...")

    # Extracts the previously downloaded zip to /static/apply
    with zipfile.ZipFile("./govuk_frontend.zip", "r") as zip_ref:
        zip_ref.extractall("./static")

    print("Moving files from static/assets to static/apply")

    for file_to_move in os.listdir("./static/assets"):
        shutil.move("./static/assets/" + file_to_move, "static")

    shutil.copyfile("./proto/static/css/main.css", "./static/main.css")
    shutil.copyfile("./proto/static/prototype.png", "./static/prototype.png")

    print("Deleting temp files")
    os.remove("./govuk_frontend.zip")


if __name__ == "__main__":
    if os.path.exists("static"):
        shutil.rmtree("static")

    build_assets()
