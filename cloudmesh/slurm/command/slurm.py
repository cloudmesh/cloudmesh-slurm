from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import map_parameters
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.systeminfo import os_is_windows
from cloudmesh.common.util import banner
from cloudmesh.common.Shell import Shell
from cloudmesh.common.Printer import Printer
from cloudmesh.common.Host import Host
from cloudmesh.common.console import Console
from cloudmesh.slurm.slurm import Slurm
import subprocess


class SlurmCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_slurm(self, args, arguments):
        """
        ::

          Usage:
                slurm pi install [--workers=WORKERS] [--partition=pis]
                slurm pi install as host [--os=OS] [--hosts=HOSTS] [--partition=pis]
                slurm pi example --n=NUMBER
                slurm pi sbatch initialize [--hosts=HOSTS]

          This command installs slurm on the current PI and also worker nodes if you specify them.

          The manager can also be a worker by using the single-node method. For example, red can be
          a manager and worker, simultaneously, by issuing
          cms slurm pi install as host --hosts=red,red

          Arguments:
              COMMAND         the slurm command to be executed [default: salloc]

          Options:
              --partition=pis     specifies the name of the slurm partition to be created [default: pis]

          Description:

            Install:

              pip install cloudmesh-slurm
              cms help
              cms slurm pi install

            Example:
              cms slurm pi example --n=4 [COMMAND]

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
                       "hosts", "workers", "partition")

        VERBOSE(arguments)

        if arguments["as"] and arguments.host and arguments.pi and arguments.install:
            "                slurm pi install as host [--workers=WORKERS] [--partition=PARTITION]"
            from cloudmesh.slurm.workflow import Workflow

            VERBOSE(arguments)

            thelambdafunction = lambda: Slurm.install(workers=workers, is_host_install=True,
                                                      input_manager=manager, hosts=arguments.hosts,
                                                      partition=arguments.partition)
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
            # slurm pi install [--interactive] [--os=OS] [--workers=WORKERS]
            # arguments.workers = Parameter.expand(arguments.workers)
            Slurm.install(workers=arguments.workers, partition=arguments.partition)
        elif arguments.pi and arguments.example:
            # slurm pi example --n=NUMBER [COMMAND]
            # salloc -N 4 mpiexec python -m mpi4py.bench helloworld
            number_nodes = arguments["--n"]
            command = f"salloc -N {number_nodes} mpiexec python -m mpi4py.bench helloworld"
            try:
                r = Shell.run(command)
                print(r)
            except subprocess.CalledProcessError as e:
                if os_is_windows():
                    banner('You may have run the command on host by mistake. Please run '
                           'this command on the Pi.')

        elif arguments.sbatch and arguments.initialize:
            if not arguments.hosts:
                Console.error("Please supply the hostnames of the Pis to initialize sbatch on.")
                return ""
            manager = arguments.hosts[:arguments.hosts.index(",")]
            workers = (arguments.hosts.split(",", 1)[1])
            results = Host.ssh(hosts=arguments.hosts,
                               command="mkdir ~/cm")
            print(Printer.write(results))
            results = Host.ssh(hosts=arguments.hosts,
                               command="cd ~/cm ; git clone https://github.com/cloudmesh/cloudmesh-mpi.git")
            print(Printer.write(results))
            results = Host.ssh(hosts=manager,
                               command="cd ~/cm/cloudmesh-mpi/doc/chapters/slurm/configs ; sbatch helloworld.slurm")
            print(Printer.write(results))
        return ""
