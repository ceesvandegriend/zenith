from zenith.command.client import *
from zenith.command.database import DatabaseContext
from zenith.cli.default import DefaultProcessor


class ClientProcessor(DefaultProcessor):
    def activate(self, name: str) -> None:
        context = DatabaseContext()
        context["client_name"] = name

        self.validating.append(ClientExistCommand())

        self.processing.append(ClientActivateCommand())

        self.execute(context)

    def create(self, name: str) -> None:
        context = DatabaseContext()
        context["client_name"] = name

        self.validating.append(ClientNotExistCommand())

        self.processing.append(ClientCreateCommand())

        self.execute(context)

    def read(self, name: str) -> None:
        context = DatabaseContext()
        context["client_name"] = name

        self.validating.append(ClientExistCommand())

        self.processing.append(ClientReadCommand())

        self.execute(context)
        self.display(context)

    def update(self, name: str) -> None:
        context = DatabaseContext()
        context["client_name"] = name

        self.validating.append(ClientExistCommand())

        self.processing.append(ClientReadCommand())

        self.execute(context)

        client = context["client"]
        context["client_description"] = self.input("Description: ", client.client_description)
        context["client_remark"] = self.input("Remark: ", client.client_remark)

        self.processing.commands.clear()
        self.processing.append(ClientUpdateCommand())

        self.execute(context)

        self.display(context)

    def delete(self, name: str) -> None:
        context = DatabaseContext()
        context["client_name"] = name

        self.validating.append(ClientExistCommand())
        self.processing.append(ClientDeleteCommand())
        self.execute(context)

    def list(self) -> None:
        context = DatabaseContext()

        self.processing.append(ClientListCommand())

        self.execute(context)

        self.display(context)

    def display(self, context: DatabaseContext) -> None:
        if "client" in context:
            client = context["client"]
            print(f"""\
ID:          {client.client_id}
UUID:        {client.client_uuid}
Name:        {client.client_name}
Active:      {client.client_active}
Description: {client.client_description or ''}

{client.client_remark or ''}""")
        elif "clients" in context:
            clients = context["clients"]
            for client in clients:
                if client.client_active:
                    msg = f"+ {client.client_id} + {client.client_name} + {client.client_uuid}"
                else:
                    msg = f"- {client.client_id} - {client.client_name} - {client.client_uuid}"
                print(msg)


if __name__ == "__main__":
    processor = ClientProcessor(logging.INFO)
    while True:
        line = processor.input("Test: ", "Een test waarde.")
        print(f"Line: {line}")
        if line == "stop":
            break