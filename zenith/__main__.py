import argparse

from zenith.process.init import InitProcessor
from zenith.process.client import ClientProcessor

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="zenith")
    subparser = parser.add_subparsers(dest="process")

    init = subparser.add_parser("init", help="Initialize Zenith")
    init.add_argument("dir", nargs="?", help="Directory, default current directory")

    client = subparser.add_parser("client", help="Client commands")
    client_subparser = client.add_subparsers(dest="command")
    client_create = client_subparser.add_parser("create", help="Creates a client")
    client_create.add_argument("name", help="Name of the client")
    client_read = client_subparser.add_parser("read", help="Reads a client")
    client_read.add_argument("name", help="Name of the client")
    client_update = client_subparser.add_parser("update", help="Updates a client")
    client_update.add_argument("name", help="Name of the client")
    client_delete = client_subparser.add_parser("delete", help="Deletes a client")
    client_delete.add_argument("name", help="Name of the client")
    client_list = client_subparser.add_parser("list", help="Lists all clients")

    args = parser.parse_args()

    print(f"Args: {args}")

    if "init" == args.process:
        processor = InitProcessor()
        processor.init(args.dir)
    elif "client" == args.process:
        processor = ClientProcessor()

        if args.command == "create":
            processor.create(args.name)
        elif args.command == "read":
            processor.read(args.name)
        elif args.command == "update":
            processor.update(args.name)
        elif args.command == "delete":
            processor.delete(args.name)
        elif args.command == "list":
            processor.list()
        else:
            client.print_help()
    else:
        parser.print_help()
