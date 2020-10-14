import os
import sys
import json
import classify
import tensorflow as tf
from flask import Flask, request, abort, jsonify, send_from_directory, Response


UPLOAD_DIRECTORY = "/tmp/image_classification_files"

IMAGE_DIRECTORY = "/home/rupam/dev/image_classification_server/images"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

api = Flask(__name__)


@api.route("/healthcheck", methods=["GET"])
def healthcheck():
    return jsonify({"status": "healthy"}), 200

@api.route("/capture/<prediction>/<filename>", methods=["POST"])
def capture_file(filename, prediction):
    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "no subdirectories directories allowed")
    print('File:', filename, ' prediction:', prediction)
    if prediction == 'eating':
        fullFileName = os.path.join('/home/rupam/dev/eating_verification/classes/stg_eating/', filename)
    elif prediction == 'other':
        fullFileName = os.path.join('/home/rupam/dev/eating_verification/classes/stg_other/', filename)
    else:
        fullFileName = os.path.join('/home/rupam/dev/eating_verification/classes/stg_eating_doubtful/', filename)
        
    with open(fullFileName, "wb") as fp:
        fp.write(request.data)
    return Response(status=200)



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
        return "Success",classify.predict(fullFileName)
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
