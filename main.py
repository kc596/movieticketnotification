import os

from controller import app
from log import logger

if __name__ == "__main__":
    logger().info("env variables: %s", str(os.environ))
    app.run(port=5000, threaded=True)
