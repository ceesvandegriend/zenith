import logging

from zenith.chain import Processor
from zenith.command.client import ClientActiveCommand
from zenith.command.project import ProjectActiveCommand
from zenith.command.task import TaskNewCommand, TaskStartCommand, TaskActiveCommand, TaskStopCommand, \
    TaskListCommand, TaskReadCommand, TaskUpdateCommand, TaskDeleteCommand
from zenith.factory.default import DefaultFactory


class TaskFactory(DefaultFactory):
    @classmethod
    def create_new(cls, level) -> Processor:
        task = cls.create_default(level)
        task.validating.append(ClientActiveCommand())
        task.validating.append(ProjectActiveCommand())
        task.processing.append(TaskNewCommand())

        return task

    @classmethod
    def create_start(cls, level) -> Processor:
        task = cls.create_default(level)
        task.validating.append(ClientActiveCommand())
        task.validating.append(ProjectActiveCommand())
        task.processing.append(TaskStartCommand())

        return task

    @classmethod
    def create_stop(cls, level) -> Processor:
        task = cls.create_default(level)
        task.validating.append(ClientActiveCommand())
        task.validating.append(ProjectActiveCommand())
        task.validating.append(TaskActiveCommand())
        task.processing.append(TaskStopCommand())

        return task

    @classmethod
    def create_read(cls, level) -> Processor:
        task = cls.create_default(level)
        task.validating.append(ClientActiveCommand())
        task.validating.append(ProjectActiveCommand())
        # task.validating.append(TaskActiveCommand())
        task.processing.append(TaskReadCommand())

        return task

    @classmethod
    def create_update(cls, level) -> Processor:
        task = cls.create_default(level)
        task.validating.append(ClientActiveCommand())
        task.validating.append(ProjectActiveCommand())
        task.processing.append(TaskUpdateCommand())

        return task

    @classmethod
    def create_delete(cls, level) -> Processor:
        task = cls.create_default(level)
        task.validating.append(ClientActiveCommand())
        task.validating.append(ProjectActiveCommand())
        task.processing.append(TaskDeleteCommand())

        return task

    @classmethod
    def create_list(cls, level) -> Processor:
        task = cls.create_default(level)
        task.validating.append(ClientActiveCommand())
        task.validating.append(ProjectActiveCommand())
        task.processing.append(TaskListCommand())

        return task
