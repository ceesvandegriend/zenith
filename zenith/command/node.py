import logging
import uuid

from zenith.chain import Command, Context

class NodeUUIDCommand(Command):
    # __node_uuid: str = None
    #
    # def get_node_UUID(self) -> str:
    #     if self.__node_uuid:
    #         return self.__node_uuid
    #
    #     if sys.platform == "linux" or sys.platform == "linux2":
    #         # linux
    #         with open("/sys/class/dmi/id/product_uuid", "rt") as tmp:
    #             self.__node_uuid = tmp.readlines()[1].strip()
    #         return self.__node_uuid
    #     elif sys.platform == "darwin":
    #         # MAC OS X
    #         output = subprocess.check_output("ioreg -rd1 -c IOPlatformExpertDevice | grep IOPlatformUUID", shell=True).decode("UTF-8")
    #         self.__node_uuid = output.split("\"")[-2]
    #         return self.__node_uuid
    #     elif sys.platform == "win32":
    #         # Windows
    #         raise NotImplemented()
    #     elif sys.platform == "win64":
    #         # Windows 64-bit
    #         raise NotImplemented()
    #     else:
    #         raise RuntimeError()

    def execute(self, context: Context) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("uuid.execute() - Start")

        context["node_uuid"] = str(uuid.UUID(int=uuid.getnode()))

        logger.info(f"Node UUID: {context['node_uuid']}")
        logger.debug("uuid.execute() - Finish")
        return Command.SUCCESS

if __name__ == "__main__":
    context = Context()
    command = NodeUUIDCommand()
    command.execute(context)

    print(f"Node UUID: {context['node_uuid']}")
