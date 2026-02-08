# run/start_client.py

import argparse
from client.client import ClientUI


def main():
    parser = argparse.ArgumentParser(description="Exchange Simulator Client")
    parser.add_argument("--user", required=True, help="Username")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=9000)

    args = parser.parse_args()

    client = ClientUI(
        user=args.user,
        host=args.host,
        port=args.port
    )

    try:
        client.start()
    except KeyboardInterrupt:
        print("\n[CLIENT] Interrupted by user")
    finally:
        client.shutdown()


if __name__ == "__main__":
    main()
