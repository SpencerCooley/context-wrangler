#!/usr/bin/env python3
import argparse
import os
import redis
import json
from dotenv import load_dotenv

def main():
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Construct the path to the .env file
    dotenv_path = os.path.join(script_dir, '.env')
    # Load environment variables from the .env file
    load_dotenv(dotenv_path=dotenv_path)

    # Set up the argument parser
    parser = argparse.ArgumentParser(description="A CLI tool to wrangle context with Redis.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- Write Command ---
    parser_write = subparsers.add_parser("write", help="Write data to a Redis key.")
    parser_write.add_argument("--key", required=True, help="The key to write to.")
    parser_write.add_argument("--data", required=True, help="The JSON data string to write.")

    # --- Read Command ---
    parser_read = subparsers.add_parser("read", help="Read data from a Redis key.")
    parser_read.add_argument("--key", required=True, help="The key to read from.")

    # --- List Command ---
    parser_list = subparsers.add_parser("list", help="List keys matching a pattern.")
    parser_list.add_argument("--pattern", default="*", help="The pattern to match keys (e.g., 'gemini-context:*').")

    # --- Delete Command ---
    parser_delete = subparsers.add_parser("delete", help="Delete a key from Redis.")
    parser_delete.add_argument("--key", required=True, help="The key to delete.")

    args = parser.parse_args()

    # Get Redis connection details from environment variables
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    redis_password = os.getenv("REDIS_PASSWORD", None)

    # Connect to Redis
    try:
        r = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            decode_responses=True # Decode responses to UTF-8
        )
        r.ping()
    except redis.exceptions.ConnectionError as e:
        print(f"Error connecting to Redis: {e}")
        return

    # --- Command Logic ---
    if args.command == "write":
        try:
            # Ensure data is valid JSON
            json.loads(args.data)
            r.set(args.key, args.data)
            print(f"Successfully wrote to key: {args.key}")
        except json.JSONDecodeError:
            print("Error: Provided data is not valid JSON.")
        except Exception as e:
            print(f"An error occurred during write: {e}")

    elif args.command == "read":
        try:
            data = r.get(args.key)
            if data:
                print(data)
            else:
                print(f"No data found for key: {args.key}")
        except Exception as e:
            print(f"An error occurred during read: {e}")

    elif args.command == "list":
        try:
            keys = [key for key in r.scan_iter(match=args.pattern)]
            if keys:
                for key in keys:
                    print(key)
            else:
                print(f"No keys found matching pattern: {args.pattern}")
        except Exception as e:
            print(f"An error occurred during list: {e}")

    elif args.command == "delete":
        try:
            result = r.delete(args.key)
            if result > 0:
                print(f"Successfully deleted key: {args.key}")
            else:
                print(f"No key found to delete: {args.key}")
        except Exception as e:
            print(f"An error occurred during delete: {e}")

if __name__ == "__main__":
    main()
