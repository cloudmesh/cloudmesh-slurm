#!/usr/bin/env python
##
# This programm is based from
#
# * https://github.com/cloudmesh/get/blob/main/pi/slurm/index.html
#
# if you use the get command you can do similar things just by saying
#
#   curl -Ls http://cloudmesh.github.io/get/pi/slurm | python
#

from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.util import banner
from cloudmesh.common.parameter import Parameter
from cloudmesh.common.Host import Host
from cloudmesh.common.Printer import Printer
from cloudmesh.common.Shell import Shell
from cloudmesh.pi.nfs.Nfs import Nfs
import os
import sys
import textwrap
import time

#
# This can be used as cloudmesh.slurm.slurm.install()
#

# hosts = "red,red0[1-3]"
# workers = "red0[1-3]"
# manager = "red"


class Slurm:
    """
    """

    step_location = "~/.cloudmesh/slurm"

    @staticmethod
    def script_executor(script, hosts=None, manager=None, workers=None, dryrun=False):
        """
        The script executor takes a script and executes line by line.
        It executes it on the

        script = '''
        workers: sudo cp /nfs/slurm.conf /usr/local/etc/slurm.conf
        hosts:   sudo mkdir /var/spool/slurmd
        manager: cd ~/slurm/etc/ && sudo cp slurmctld.service /etc/systemd/system
        '''
        """

        _script = textwrap.dedent(script).strip().splitlines()
        for line in _script:
            if not line.startswith("#") or ":" not in line:
                where, command = line.split(":",1)
                where = where.strip()
                command = command.strip()
                if not dryrun:
                    if where == "workers":
                      where = workers
                    elif where == "hosts":
                      where = hosts
                    elif where == "manager":
                      where = manager
                    else:
                      where = None
                    results = Host.ssh(hosts=where, command=command)
                    print(Printer.write(results))
                else:
                    print(f"[{where}]", f"<{command}>")

    # TODO: invert parameters rename hmanager to host: host=None, script=None
    @staticmethod
    def hostexecute(host=None, script=None):
        """

        :param host:
        :type host:
        :param script:
        :type script:
        :return:
        :rtype:
        """
        for command in script.splitlines():
            print(command)
            results = Host.ssh(hosts=host, command=command)
            print(Printer.write(results))

    @staticmethod
    def get_manager_name():
        """

        :return:
        :rtype:
        """
        return Shell.run("hostname").strip()

    # defining function which formulates hosts variable
    # the hosts variable has manager and workers

    @staticmethod
    def get_hosts(manager, workers):
        """

        :param manager:
        :type manager:
        :param workers:
        :type workers:
        :return:
        :rtype:
        """
        return f'{manager},{workers}'

    # read the file user_input_workers
    @staticmethod
    def read_user_input_workers(manager):
        """

        :param manager:
        :type manager:
        :return:
        :rtype:
        """
        results = Host.ssh(hosts=manager, command='cat user_input_workers')
        print(Printer.write(results))
        for entry in results:
            print(str(entry["stdout"]))
            workers = str(entry["stdout"])
            return workers

    @staticmethod
    def tell_user_rebooting(hosts):
        """
        tell user to ssh back to manager on reboot and reboot

        :param hosts:
        :type hosts:
        :return:
        :rtype:
        """
        banner('The cluster is rebooting.')
        os.system("cms host reboot " + hosts)

    # function that returns ip of pi
    @staticmethod
    def get_IP(manager):
        """

        :param manager:
        :type manager:
        :return:
        :rtype:
        """
        results = Host.ssh(hosts=manager, command="/sbin/ifconfig eth0 | grep 'inet' | cut -d: -f2")
        print(Printer.write(results))
        for entry in results:
            print(str(entry["stdout"]))
            ipaddress = str(entry["stdout"])
        ipaddress2 = ipaddress.replace('inet ', '')
        ipaddress3 = ipaddress2.split(' ')
        ipaddress4 = [x for x in ipaddress3 if x]
        trueIP = ipaddress4[0]
        return trueIP

    # function that checks to see if a step has been run

    @staticmethod
    def check_step(step_number, device):
        """

        :param step_number:
        :type step_number:
        :param device:
        :type device:
        :return:
        :rtype:
        """
        step = f"step{step_number}"
        changed_command = f"ls {Slurm.step_location}/{step}"
        results = Host.ssh(hosts=device, command=changed_command)
        print(Printer.write(results))
        step_done = True
        error_code = "255"
        sleeping = True
        while sleeping:
            results = Host.ssh(hosts=device, command=changed_command)
            print(Printer.write(results))
            for entry in results:
                if error_code in str(entry["returncode"]):
                    time.sleep(15)
                    break
                else:
                    sleeping = False
        if (step in str(entry["stdout"]) and 'cannot access' in str(entry["stdout"])) or \
                (step in str(entry["stderr"]) and 'cannot access' in str(entry["stderr"])):
            step_done = False
            entry["success"] = "False"
        return step_done

    @staticmethod
    def try_installing_package(command_for_package, listOfWorkers):
        """

        :param command_for_package:
        :type command_for_package:
        :param listOfWorkers:
        :type listOfWorkers:
        :return:
        :rtype:
        """
        for worker in listOfWorkers:
            success = False
            while not success:
                success = True
                results = Host.ssh(hosts=worker,
                                   command=command_for_package)
                print(Printer.write(results))
                for entry in results:
                    if ('Could not connect to' in str(entry["stdout"])) or ('Failed to fetch' in str(entry["stdout"])):
                        msg = f"The SLURM script could not install needed packages, but will try again. " \
                              f"This is expected behavior and it should fix itself within a few minutes. " \
                              f"Currently fixing {worker}."
                        banner(msg)
                        # return msg
                        success = False
                    else:
                        banner(f"Package installation has succeeded for {worker}.")
                time.sleep(5)

    @staticmethod
    def try_downloading_from_github(command_for_download, listOfWorkers):
        """

        :param command_for_download:
        :type command_for_download:
        :param listOfWorkers:
        :type listOfWorkers:
        :return:
        :rtype:
        """
        for worker in listOfWorkers:
            success = False
            while not success:
                success = True
                results = Host.ssh(hosts=worker,
                                   command=command_for_download)
                print(Printer.write(results))
                for entry in results:
                    if 'Failed to connect to' in str(entry["stderr"]):
                        msg = f"The SLURM script could not download needed packages, but will try again. " \
                              f"This is expected behavior and it should fix itself within a few minutes. " \
                              f"Currently fixing {worker}."
                        banner(msg)
                        # return msg
                        success = False
                    else:
                        banner(f"Package download has succeeded for {worker}.")
                time.sleep(5)

    # Beginning to define SLURM installation

    # input
    #  basename = "red"
    #  no workers = "03" # "3" "01000" 00001-01000
    # output
    #  red000  -> red, red001, red002, red003
    @staticmethod
    def step0_identify_workers(workers=None,
                               is_host_install=False,
                               input_manager=None,
                               partition='pis',
                               **kwargs):
        """
        step0_identify_workers

        :param workers:
        :type workers:
        :param is_host_install:
        :type is_host_install:
        :param input_manager:
        :type input_manager:
        :param partition:
        :type partition:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        StopWatch.start("Current section time")
        banner("Welcome to SLURM Installation. Initializing preliminary steps.")
        print("We assume that you run this script on the manager Pi and that your worker naming schema is \n"
              "incremental in nature. \n")
        if is_host_install:
            manager = input_manager
        else:
            manager = Slurm.get_manager_name()
        if not workers:
            user_input_workers = input(str('''Please enter the naming schema of your workers. For example, if you have 3
                workers then enter "red0[1-3]". Another example for 7 workers is "worker[1-7]" (do not include
                quotation marks): \n'''))
        else:
            user_input_workers = workers
        results = Host.ssh(hosts=manager, command=f"mkdir -p {Slurm.step_location} && touch {Slurm.step_location}/user_input_workers")
        print(Printer.write(results))
        results = Host.ssh(hosts=manager, command=f"echo '{user_input_workers}' >> {Slurm.step_location}/user_input_workers")
        print(Printer.write(results))

        # intro and asking for workers from user
        workers = Slurm.read_user_input_workers(manager)

        hosts = Slurm.get_hosts(manager, workers)

        results = Host.ssh(hosts=hosts, command=f"mkdir -p {Slurm.step_location} && touch {Slurm.step_location}/step0")
        print(Printer.write(results))
        StopWatch.stop("Current section time")
        StopWatch.benchmark()

    @staticmethod
    def step1_os_update(workers=None,
                        is_host_install=False,
                        input_manager=None,
                        hosts=None,
                        partition='pis',
                        **kwargs):
        """
        step1_os_update

        :param workers:
        :type workers:
        :param is_host_install:
        :type is_host_install:
        :param input_manager:
        :type input_manager:
        :param hosts:
        :type hosts:
        :param partition:
        :type partition:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        StopWatch.start("Current section time")
        # intro and asking for workers from user
        banner("Initializing Step 1 now.")
        if is_host_install:
            manager = input_manager
        else:
            manager = Slurm.get_manager_name()
        if not workers:
            workers = Slurm.read_user_input_workers(manager)

        if not hosts:
            hosts = Slurm.get_hosts(manager, workers)

        banner("Now updating packages. This may take a while.")

        results = Host.ssh(hosts=hosts, command="sudo apt-get update")
        print(Printer.write(results))
        # parallel_execute(hosts,"sudo apt install ntpdate -y")
        # results2 = Host.ssh(hosts=hosts, command="sudo apt install ntpdate -y")
        # print(Printer.write(results2))

        # make array with list of workers
        listOfWorkers = Parameter.expand(workers)

        print(listOfWorkers)
        listOfManager = [manager]
        Slurm.try_installing_package("sudo apt install ntpdate -y", listOfManager)
        Slurm.try_installing_package("sudo apt install ntpdate -y", listOfWorkers)
        results = Host.ssh(hosts=hosts, command=f"mkdir -p {Slurm.step_location} && touch {Slurm.step_location}/step1")
        print(Printer.write(results))
        StopWatch.stop("Current section time")
        StopWatch.benchmark()
        Slurm.tell_user_rebooting(hosts)

    @staticmethod
    def step2_setup_shared_file_system(workers=None,
                                       is_host_install=False,
                                       input_manager=None,
                                       hosts=None,
                                       partition='pis',
                                       **kwargs):
        """
        step2_setup_shared_file_system

        :param workers:
        :type workers:
        :param is_host_install:
        :type is_host_install:
        :param input_manager:
        :type input_manager:
        :param hosts:
        :type hosts:
        :param partition:
        :type partition:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        StopWatch.start("Current section time")
        banner("Initializing Step 2 now.")
        sys.stdin.reconfigure(encoding='utf-8')
        sys.stdout.reconfigure(encoding='utf-8')
        if is_host_install:
            manager = input_manager
        else:
            manager = Slurm.get_manager_name()
            workers = Slurm.read_user_input_workers(manager)

        # executing reading of workers

        if not hosts:
            hosts = Slurm.get_hosts(manager, workers)
        nfs = Nfs()
        nfs.install(manager)
        nfs.share("/nfs,/nfs", hosts)
        results = Host.ssh(hosts=hosts, command=f"mkdir -p {Slurm.step_location} && touch {Slurm.step_location}/step2")
        print(Printer.write(results))
        StopWatch.stop("Current section time")
        StopWatch.benchmark()
        Slurm.tell_user_rebooting(hosts)

    @staticmethod
    def step3_install_openmpi(workers=None,
                              is_host_install=False,
                              input_manager=None,
                              hosts=None,
                              partition='pis', **kwargs):
        """
        step3_install_openmpi

        :param workers:
        :type workers:
        :param is_host_install:
        :type is_host_install:
        :param input_manager:
        :type input_manager:
        :param hosts:
        :type hosts:
        :param partition:
        :type partition:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        StopWatch.start("Current section time")
        banner("Initializing Step 3 now.")

        if is_host_install:
            manager = input_manager
        else:
            manager = Slurm.get_manager_name()
            workers = Slurm.read_user_input_workers(manager)
        # getting ip in case step 2 has not run
        trueIP = Slurm.get_IP(manager)

        if not hosts:
            hosts = Slurm.get_hosts(manager, workers)

        listOfWorkers = Parameter.expand(workers)
        listOfManager = [manager]
        trueIP = Slurm.get_IP(manager)
        Slurm.try_installing_package(
            "sudo apt-get install python3-venv python3-wheel python3-dev build-essential libopenmpi-dev "
            "-y",
            listOfWorkers)
        Slurm.try_installing_package(
            "sudo apt-get install python3-venv python3-wheel python3-dev build-essential libopenmpi-dev "
            "-y",
            listOfManager)
        results = Host.ssh(hosts=workers, command='python3 -m venv ~/ENV3')
        print(Printer.write(results))
        Slurm.try_installing_package("sudo apt-get install openmpi-bin -y", listOfWorkers)
        Slurm.try_installing_package("sudo apt-get install openmpi-bin -y", listOfManager)
        results = Host.ssh(hosts=hosts, command='sudo ldconfig')
        print(Printer.write(results))
        results = Host.ssh(hosts=hosts, command='ENV3/bin/pip install mpi4py')
        print(Printer.write(results))
        sys.stdin.reconfigure(encoding='utf-8')
        sys.stdout.reconfigure(encoding='utf-8')
        Slurm.try_installing_package("sudo apt install libevent-dev autoconf git libtool flex libmunge-dev munge -y",
                                     listOfManager)
        Slurm.try_installing_package("sudo apt install libevent-dev autoconf git libtool flex libmunge-dev munge -y",
                                     listOfWorkers)
        results = Host.ssh(hosts=hosts, command='sudo mkdir -p /usr/lib/pmix/build/2.1 /usr/lib/pmix/install/2.1')
        print(Printer.write(results))
        Slurm.try_downloading_from_github(
            "cd /usr/lib/pmix && sudo git clone https://github.com/openpmix/openpmix.git source "
            "&& cd source/ && git branch -a && sudo git checkout v2.1 && "
            "sudo git pull", listOfManager)
        script = f"""
            manager: sudo systemctl status nfs-server.service
            manager: sudo systemctl start nfs-server.service
            manager: sudo mount -a
            hosts:   mkdir -p {Slurm.step_location} && touch {Slurm.step_location}/step3
            """
        Slurm.script_executor(script, manager=manager, hosts=hosts)
        StopWatch.stop("Current section time")
        StopWatch.benchmark()
        Slurm.tell_user_rebooting(hosts)

    @staticmethod
    def step4_install_pmix_and_slurm(workers=None,
                                     is_host_install=False,
                                     input_manager=None,
                                     hosts=None,
                                     partition='pis', **kwargs):
        """
        step4_install_pmix_and_slurm

        :param workers:
        :type workers:
        :param is_host_install:
        :type is_host_install:
        :param input_manager:
        :type input_manager:
        :param hosts:
        :type hosts:
        :param partition:
        :type partition:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        StopWatch.start("Current section time")
        banner("Initializing Step 4 now.")
        if is_host_install:
            manager = input_manager
        else:
            manager = Slurm.get_manager_name()
            workers = Slurm.read_user_input_workers(manager)

        if not hosts:
            hosts = Slurm.get_hosts(manager, workers)

        listOfWorkers = Parameter.expand(workers)
        print(listOfWorkers)
        print(hosts)

        trueIP = Slurm.get_IP(manager)

        banner("This will take a while...")

        # see comment on script executor
        #
        script = """
            hosts:   sudo useradd slurm
            manager: sudo cp -R /usr/lib/pmix /nfs
            workers: sudo cp -R /nfs/pmix /usr/lib
            hosts:   cd /usr/lib/pmix/source/ && sudo ./autogen.sh && cd ../build/2.1/ && sudo ../../source/configure --prefix=/usr/local && sudo make -j install >/dev/null
            manager: git clone https://github.com/SchedMD/slurm && sudo cp -R slurm /nfs
            workers: sudo cp -R /nfs/slurm ~
            hosts:   cd slurm && sudo ./configure --enable-debug --with-pmix --with-munge --enable-deprecated
            hosts:   cd slurm && sudo make -j install > /dev/null
            """

        Slurm.script_executor(script, hosts=hosts, manager=manager, workers=workers)


        '''
        results = Host.ssh(hosts=hosts, command='wget '
                                                'https://download.open-mpi.org/release/open-mpi/v4.1/openmpi-4.1.2.tar.gz')
        print(Printer.write(results))
        results = Host.ssh(hosts=hosts, command='gunzip -c openmpi-4.1.2.tar.gz | tar xf -')
        print(Printer.write(results))
        results = Host.ssh(hosts=hosts, command='cd openmpi-4.1.2 && sudo ./configure --prefix=/usr/local --with-slurm && '
                                                'sudo make all install')
        print(Printer.write(results))
        results = Host.ssh(hosts=hosts, command='sudo rm -rf openmpi-4.1.2')
        print(Printer.write(results))
        results = Host.ssh(hosts=hosts, command='sudo rm openmpi-4.1.2.tar.gz')
        print(Printer.write(results))
        '''

        script = f"""
            manager: sudo curl -L https://raw.githubusercontent.com/cloudmesh/cloudmesh-mpi/main/cloudmesh/mpi/etc/slurm.conf > ~/slurm.conf
            manager: sudo mv ~/slurm.conf /usr/local/etc/
            manager: sudo sed -i 's/SlurmctldHost=workstation/SlurmctldHost={manager}({trueIP})/g' /usr/local/etc/slurm.conf
            manager: sudo sed -i "$(( $(wc -l </usr/local/etc/slurm.conf)-2+1 )),$ d" /usr/local/etc/slurm.conf
            """
        Slurm.script_executor(script, manager=manager, workers=workers)
        results = Host.ssh(hosts=workers, command="cat /proc/sys/kernel/hostname")
        print(Printer.write(results))
        hostnames = []
        for entry in results:
            currentHostname = str(entry["stdout"])
            hostnames.append(currentHostname)
        print(hostnames)
        results = Host.ssh(hosts=workers, command="/sbin/ifconfig eth0 | grep 'inet' | cut -d: -f2")
        ipaddresses = []
        trueIPs = []
        print(Printer.write(results))
        for entry in results:
            currentIP = str(entry["stdout"])
            ipaddresses.append(currentIP)
        for x in ipaddresses:
            x2 = x.replace('inet ', '')
            x3 = x2.split(' ')
            x4 = [y for y in x3 if y]
            trueIP = x4[0]
            trueIPs.append(trueIP)
        coreCounts = []
        results = Host.ssh(hosts=workers,
                           command="cat /sys/devices/system/cpu/cpu[0-9]*/topology/core_cpus_list | sort -u | wc -l")
        for entry in results:
            currentCoreCount = str(entry["stdout"])
            coreCounts.append(currentCoreCount)
        for x in range(len(hostnames)):
            command = f'echo "NodeName={hostnames[x]} NodeAddr={trueIPs[x]} CPUs={coreCounts[x]} State=UNKNOWN" ' \
                      '| sudo tee /usr/local/etc/slurm.conf -a'
            results = Host.ssh(hosts=manager,
                               command=command)
            print(Printer.write(results))

        script = f'''
            manager: echo "PartitionName={partition} Nodes={workers} Default=YES MaxTime=INFINITE State=UP" | sudo tee /usr/local/etc/slurm.conf -a
            manager: sudo curl -L https://github.com/cloudmesh/cloudmesh-mpi/raw/main/cloudmesh/mpi/etc/cgroup.conf > ~/cgroup.conf
            manager: sudo cp ~/cgroup.conf /usr/local/etc/cgroup.conf
            manager: sudo rm ~/cgroup.conf
            manager: sudo cp /usr/local/etc/slurm.conf /usr/local/etc/cgroup.conf /nfs
            manager: sudo cp /etc/munge/munge.key /nfs
            manager: sudo systemctl enable munge
            manager: sudo systemctl start munge
            workers: sudo cp /nfs/slurm.conf /usr/local/etc/slurm.conf
            workers: sudo cp /nfs/cgroup.conf /usr/local/etc/cgroup.conf
            hosts:   sudo mkdir /var/spool/slurmd
            hosts:   sudo chown -R slurm:slurm /var/spool/
            workers: cd ~/slurm/etc/ && sudo cp slurmd.service /etc/systemd/system/
            manager: cd ~/slurm/etc/ && sudo cp slurmctld.service /etc/systemd/system/
            workers: sudo cp /nfs/munge.key /etc/munge/munge.key
            workers: sudo systemctl enable munge
            workers: sudo systemctl start munge
            workers: sudo systemctl enable slurmd
            workers: sudo systemctl start slurmd
            manager: sudo systemctl enable slurmctld
            manager: sudo systemctl start slurmctld
            hosts:   mkdir -p {Slurm.step_location} && touch {Slurm.step_location}/step4
            '''
        Slurm.script_executor(script, hosts=hosts, manager=manager, workers=workers)

        print("Rebooting cluster now.")
        banner("After successful reboot, ssh back into manager and test SLURM by issuing $ srun --nodes=3 hostname "
               "(change 3 to number of nodes if necessary). If it does not work right away, wait a minute for the "
               "nodes to come back online.\n")
        os.system("cms host reboot " + hosts)

    # StopWatch.start("Total Runtime")

    # Here begins the script aside from the function definitions. In this part we run the steps by calling functions.
    @staticmethod
    def install(interactive=False,
                workers=None,
                selected_os="raspberry",
                step=None,
                is_host_install=False,
                input_manager=None,
                hosts=None,
                partition="pis"):
        """

        :param interactive:
        :type interactive:
        :param workers:
        :type workers:
        :param selected_os:
        :type selected_os:
        :param step:
        :type step:
        :param is_host_install:
        :type is_host_install:
        :param input_manager:
        :type input_manager:
        :param hosts:
        :type hosts:
        :param partition:
        :type partition:
        :return:
        :rtype:
        """
        banner("SLURM on Raspberry Pi Cluster Installation")

        # executing reading of device names.

        if is_host_install:
            manager = input_manager
        else:
            manager = Slurm.get_manager_name()

        step0done = Slurm.check_step(0, manager)
        if not step0done:
            if is_host_install:
                workers = (hosts.split(",", 1)[1])
            else:
                Slurm.step0_identify_workers(workers)

        if interactive:
            workers = Slurm.read_user_input_workers(manager)

        if not hosts:
            hosts = Slurm.get_hosts(manager, workers)

        if step is None:
            steps = [
                (1, Slurm.step1_os_update),
                (2, Slurm.step2_setup_shared_file_system),
                (3, Slurm.step3_install_openmpi),
                (4, Slurm.step4_install_pmix_and_slurm)
            ]
        elif int(step) == 0:
            steps = [
                (0, Slurm.step0_identify_workers),
            ]
        elif int(step) == 1:
            steps = [
                (1, Slurm.step1_os_update)
            ]
        elif int(step) == 2:
            steps = [
                (2, Slurm.step2_setup_shared_file_system)
            ]
        elif int(step) == 3:
            steps = [
                (3, Slurm.step3_install_openmpi)
            ]
        elif int(step) == 4:
            steps = [
                (4, Slurm.step4_install_pmix_and_slurm)
            ]

        for i, step in steps:
            print(i, step)
            print(Slurm.check_step(i, hosts))
            if not Slurm.check_step(i, hosts):
                banner(f"Step {i} is not done. Performing step {i} now.")
                step(workers=workers, is_host_install=is_host_install, input_manager=input_manager,
                     hosts=hosts, partition=partition)

    '''
    StopWatch.stop("Total Runtime")
    StopWatch.benchmark()
    '''
