from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
from cloudmesh.shell.command import map_parameters
from cloudmesh.slurm.slurm import Slurm
from cloudmesh.common.parameter import Parameter

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
            steps = [
                Slurm.step0_identify_workers,
                Slurm.step1_os_update,
                Slurm.step2_setup_shared_file_system,
                Slurm.step3_install_openmpi,
                Slurm.step4_install_pmix_and_slurm
            ]
            workers = Parameter.expand(arguments.hosts)[1:]
            manager = Parameter.expand(arguments.hosts)[0]
            step0 = Slurm.install(workers=workers, is_host_install=True, input_manager=manager)
            step1 = Slurm.install(workers=workers, is_host_install=True, input_manager=manager)
            step2 = Slurm.install(workers=workers, is_host_install=True, input_manager=manager,
                                  mount=arguments.mount)
            step3 = Slurm.install(workers=workers, is_host_install=True, input_manager=manager)
            step4 = Slurm.install(workers=workers, is_host_install=True, input_manager=manager)
            w = Workflow(arguments.hosts,trials=10,delay=10)
            w.run(steps=steps)
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
