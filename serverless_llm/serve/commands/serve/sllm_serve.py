# ---------------------------------------------------------------------------- #
#  serverlessllm                                                               #
#  copyright (c) serverlessllm team 2024                                       #
#                                                                              #
#  licensed under the apache license, version 2.0 (the "license");             #
#  you may not use this file except in compliance with the license.            #
#                                                                              #
#  you may obtain a copy of the license at                                     #
#                                                                              #
#                  http://www.apache.org/licenses/license-2.0                  #
#                                                                              #
#  unless required by applicable law or agreed to in writing, software         #
#  distributed under the license is distributed on an "as is" basis,           #
#  without warranties or conditions of any kind, either express or implied.    #
#  see the license for the specific language governing permissions and         #
#  limitations under the license.                                              #
# ---------------------------------------------------------------------------- #
import argparse
import logging
import sys

import ray
import uvicorn

from serverless_llm.serve.app_lib import create_app
from serverless_llm.serve.controller import SllmController
from serverless_llm.serve.logger import init_logger

logger = init_logger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="ServerlessLLM CLI for model management."
    )
    subparsers = parser.add_subparsers(dest="command")

    start_parser = subparsers.add_parser("start", help="Start the Sllm server.")
    start_parser.add_argument(
        "--host",
        default="0.0.0.0",
        type=str,
        help="Host IP to run the server on.",
    )
    start_parser.add_argument(
        "--port", default=8343, type=int, help="Port to run the server on."
    )
    start_parser.add_argument(
        "--enable-migration",
        action="store_true",
        help="Enable migration of models.",
    )
    args = parser.parse_args()

    try:
        if args.command == "start":
            app = create_app()
            controller = SllmController.options(name="controller").remote(
                {"enable_migration": args.enable_migration}
            )
            ray.get(controller.start.remote())

            uvicorn.run(app, host=args.host, port=args.port)
        else:
            parser.print_help()
            sys.exit(1)
    except KeyboardInterrupt:
        ray.get(controller.shutdown.remote())


if __name__ == "__main__":
    main()
