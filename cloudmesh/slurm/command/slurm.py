from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
from cloudmesh.shell.command import map_parameters

class SlurmCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_slurm(self, args, arguments):
        """
        ::

          Usage:
                slurm pi install [-i] [--os=OS] [--workers=WORKERS] [--mount=MOUNT] [--step=STEP]
                slurm pi install as worker
                slurm pi example

          This command installs slurm on the current PI and also worker nodes if you specify them.

          TODO: how can the master be made also a worker, e.g. The slurm without worker nodes example
                we want a new command for that "install as worker"

          Arguments:
              FILE   a file name

          Options:
              -f        specify the file
              -i        asks questions
              --os=OS   The operating system. SO far only RaspberryPiOS [default: RaspberryPiOS]

          Description:

            pip install cloudmesh-slurm
            cms help
            cms slurm pi install -i
        

        """


        map_parameters(arguments, "file")

        VERBOSE(arguments)

        if arguments.file:
            print("option a")

        elif arguments.list:
            print("option b")

        return ""
