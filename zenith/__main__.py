import argparse

from zenith.process.init import InitProcessor
from zenith.process.client import ClientProcessor
from zenith.process.project import ProjectProcessor

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="zenith")
    subparser = parser.add_subparsers(dest="process")

    init = subparser.add_parser("init", help="Initialize Zenith")
    init.add_argument("dir", nargs="?", help="Directory, default current directory")

    client = subparser.add_parser("client", help="Client commands")
    client_subparser = client.add_subparsers(dest="command")
    client_activate = client_subparser.add_parser("activate", help="Activates a client")
    client_activate.add_argument("name", help="Name of the client")
    client_create = client_subparser.add_parser("create", help="Creates a client")
    client_create.add_argument("name", help="Name of the client")
    client_read = client_subparser.add_parser("read", help="Reads a client")
    client_read.add_argument("name", help="Name of the client")
    client_update = client_subparser.add_parser("update", help="Updates a client")
    client_update.add_argument("name", help="Name of the client")
    client_delete = client_subparser.add_parser("delete", help="Deletes a client")
    client_delete.add_argument("name", help="Name of the client")
    client_list = client_subparser.add_parser("list", help="Lists all clients")

    project = subparser.add_parser("project", help="Project commands")
    project_subparser = project.add_subparsers(dest="command")
    project_activate = project_subparser.add_parser("activate", help="Activates a project")
    project_activate.add_argument("name", help="Name of the project")
    project_create = project_subparser.add_parser("create", help="Creates a project")
    project_create.add_argument("name", help="Name of the project")
    project_read = project_subparser.add_parser("read", help="Reads a project")
    project_read.add_argument("name", help="Name of the project")
    project_update = project_subparser.add_parser("update", help="Updates a project")
    project_update.add_argument("name", help="Name of the project")
    project_delete = project_subparser.add_parser("delete", help="Deletes a project")
    project_delete.add_argument("name", help="Name of the project")
    project_list = project_subparser.add_parser("list", help="Lists all projects")
    args = parser.parse_args()

    if "init" == args.process:
        processor = InitProcessor()
        processor.init(args.dir)
    elif "client" == args.process:
        processor = ClientProcessor()

        if args.command == "activate":
            processor.activate(args.name)
        elif args.command == "create":
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
    elif "project" == args.process:
        processor = ProjectProcessor()

        if args.command == "activate":
            processor.activate(args.name)
        elif args.command == "create":
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
            project.print_help()
    else:
        parser.print_help()
