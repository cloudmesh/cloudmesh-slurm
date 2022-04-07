from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
from cloudmesh.shell.command import map_parameters
from cloudmesh.slurm.slurm import Slurm
from cloudmesh.common.parameter import Parameter
from cloudmesh.burn.util import os_is_windows

class SlurmCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_slurm(self, args, arguments):
        """
        ::

          Usage:
                slurm pi install [--interactive] [--os=OS] [--workers=WORKERS] [--mount=MOUNT] [--step=STEP]
                slurm pi install as worker
                slurm pi example --n=NUMBER [COMMAND]
                slurm pi install as host [--os=OS] [--hosts=HOSTS] [--mount=MOUNT]

          This command installs slurm on the current PI and also worker nodes if you specify them.

          TODO: how can the master be made also a worker, e.g. The slurm without worker nodes example
                we want a new command for that "install as worker"

          Arguments:
              COMMAND  the slurm command to be executed [default: salloc]

          Options:
              -f                   specify the file
              --interactive        asks questions
              --os=OS              The operating system. SO far only RaspberryPiOS [default: RaspberryPiOS]

          Description:

            Install:

              pip install cloudmesh-slurm
              cms help
              cms slurm pi install --interactive

            Example:
              cms slurm example --n=4 [COMMAND]

              MODE is one of salloc, srun, sbatch

              will run the command

                salloc -N 4 mpiexec python -m mpi4py.bench helloworld

              API:

                from cloudmesh.slurm.slurm import Slurm
                from cloudmesh.slurm import Slurm

                Slurm.install()

                in case you use self

                slurm = Slurm()    slef instead of Slurm
                slurm.install

        """


        map_parameters(arguments,
                       "interactive",
                       "os", "mount", "step", "hosts", "workers")

        VERBOSE(arguments)

        if arguments["as"] and arguments.host and arguments.pi and arguments.install:
            "                slurm pi install as host [--os=OS] [--workers=WORKERS] [--mount=MOUNT]"
            from cloudmesh.slurm.workflow import Workflow
            print(arguments.mount)
            print(arguments["--mount"])
            if os_is_windows():
                arguments.mount = arguments.mount.replace("\\", "/")

            VERBOSE(arguments)

            thelambdafunction = lambda: Slurm.install(workers=workers, is_host_install=True,
                                                      input_manager=manager, hosts=arguments.hosts,
                                                      mount=arguments.mount)
            steps = [
                thelambdafunction, thelambdafunction, thelambdafunction, thelambdafunction
            ]
            manager = arguments.hosts[:arguments.hosts.index(",")]
            workers = (arguments.hosts.split(",",1)[1])
            # workers = Parameter.expand(arguments.hosts)[1:]
            # manager = Parameter.expand(arguments.hosts)[0]
            '''
            step0 = Slurm.install(workers=workers, is_host_install=True, input_manager=manager, hosts=arguments.hosts)
            step1 = Slurm.install(workers=workers, is_host_install=True, input_manager=manager, hosts=arguments.hosts)
            step2 = Slurm.install(workers=workers, is_host_install=True, input_manager=manager,
                                  mount=arguments.mount, hosts=arguments.hosts)
            step3 = Slurm.install(workers=workers, is_host_install=True, input_manager=manager, hosts=arguments.hosts)
            step4 = Slurm.install(workers=workers, is_host_install=True, input_manager=manager, hosts=arguments.hosts)

            '''
            w = Workflow(arguments.hosts,trials=1,delay=1)
            w.run(steps=steps)
            '''
            workers = Parameter.expand(arguments.hosts)[1:]
            manager = Parameter.expand(arguments.hosts)[0]
            Slurm.install(is_host_install=True, input_manager=manager, hosts=arguments.hosts)
            '''
        elif arguments.install and arguments.pi and not arguments["as"]:
            # slurm pi install [--interactive] [--os=OS] [--workers=WORKERS] [--mount=MOUNT] [--step=STEP]
            # arguments.workers = Parameter.expand(arguments.workers)
            Slurm.install(workers=arguments.workers, mount=arguments.mount)
        elif arguments.install and arguments["as"] and arguments.worker:
            # slurm pi install as worker
            Console.error("not implemented")
        elif arguments.pi and arguments.example:
            # slurm pi example --n=NUMBER [COMMAND]
            Console.error  ("not implemented")

        return ""
