import os
import sys
import json
import classify
import tensorflow as tf
from flask import Flask, request, abort, jsonify, send_from_directory


UPLOAD_DIRECTORY = "/tmp/image_classification_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

api = Flask(__name__)


@api.route("/healthcheck", methods=["GET"])
def healthcheck():
    return jsonify({"status": "healthy"}), 200


@api.route("/predict/<filename>", methods=["POST"])
def post_file(filename):
    """Upload a file."""

    # headers = request.headers
    # auth = headers.get("X-Api-Key")
    # if auth != 'mskib0102':
    #     return jsonify({"message": "ERROR: Unauthorized"}), 401

    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "no subdirectories directories allowed")

    fullFileName = os.path.join(UPLOAD_DIRECTORY, filename)
    with open(fullFileName, "wb") as fp:
        fp.write(request.data)

    try:
        return "",classify.predict(fullFileName)
    except ValueError as e:
        print("Value error \n {0}".format(e))
    except AttributeError as a:
        print("Value error \n {0}".format(a))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        abort(500, "Internal Server Error")

    # Return 201 CREATED
    abort(500, "Internal Server Error")


if __name__ == "__main__":
    # from waitress import serve
    api.run(host="0.0.0.0", port=8080)