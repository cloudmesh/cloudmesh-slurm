# Documentation for cms SLURM installation

[![image](https://travis-ci.com/cloudmesh/cloudmesh-slurm.svg?branch=main)](https://travis-ci.com/github/cloudmesh/cloudmesh-slurm)
[![image](https://img.shields.io/pypi/pyversions/cloudmesh-slurm.svg)](https://pypi.org/project/cloudmesh-slurm)
[![image](https://img.shields.io/pypi/v/cloudmesh-slurm.svg)](https://pypi.org/project/cloudmesh-slurm/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


## Abstract


<!--TOC-->

- [Documentation for cms SLURM installation](#documentation-for-cms-slurm-installation)
  - [Abstract](#abstract)
  - [1.0 Installation](#10-installation)
  - [2.0 Method 1 - Install from Host](#20-method-1---install-from-host)
  - [3.0 Method 2 - Install on Manager](#30-method-2---install-on-manager)
  - [4.0 Install Single-Node](#40-install-single-node)
  - [5.0 Manual Pages](#50-manual-pages)
    - [5.1 Manual Page for the `slurm` command](#51-manual-page-for-the-slurm-command)

<!--TOC-->

## 1.0 Installation

The installation takes around an hour to two hours, for example, on a
cluster of five Raspberry Pi 4 Model B computers.

To use the cloudmesh SLURM command, one must have cloudmesh installed
by using the following commands.

We assume you are in a venv Python environment. Ours is called (ENV3)

```bash
(ENV3) you@yourlaptop $ mkdir ~/cm
(ENV3) you@yourlaptop $ cd ~/cm
(ENV3) you@yourlaptop $ pip install cloudmesh-installer
(ENV3) you@yourlaptop $ cloudmesh-installer get pi
```

Initialize the cms command:

```bash
(ENV3) you@yourlaptop $ cms help
```

Then clone the cloudmesh-slurm repository:

```bash
(ENV3) you@yourlaptop $ cd ~/cm
(ENV3) you@yourlaptop $ cloudmesh-installer get cmd5
(ENV3) you@yourlaptop $ git clone https://github.com/cloudmesh/cloudmesh-slurm.git
(ENV3) you@yourlaptop $ cd cloudmesh-slurm
(ENV3) you@yourlaptop $ pip install -e .
(ENV3) you@yourlaptop $ cms help
```

You may proceed if `slurm` shows in the documented commands.

After following [the burn
tutorial](https://cloudmesh.github.io/pi/tutorial/raspberry-burn-windows/)
and ensuring that the cluster is online, you have two methods of
installing SLURM.

## 2.0 Method 1 - Install from Host

You can install SLURM on a cluster by executing commands from the host
computer. The host computer is the same computer that is previously
referred to as `you@yourlaptop` and it is used to `ssh` into the Pis.

Use this command:
```bash
cms slurm pi install as host --hosts=red,red0[1-4] --mount=//dev//sda
```

The `--hosts` parameter should be edited to have the hostnames of your
manager and workers, separated by comma.

The `--mount` parameter should point to the mount place of your USB,
inserted in the top-most blue USB3.0 port (on Pi 4's), and ***it will
be formatted.***

The command may seem to hang at certain points, but these points
should not last more than 45 minutes and are likely simply building
from source.

Once the script ends, you can check if SLURM is installed by issuing
on the manager:

`srun --nodes=3 hostname`

and replacing the `--nodes` parameter with the number of workers.

## 3.0 Method 2 - Install on Manager

This method involves the user logging into the manager via `ssh`,
installing cloudmesh via:

```bash
(ENV3) you@yourhostcomputer $ ssh red
pi@red $ curl -Ls http://cloudmesh.github.io/get/pi | sh -
```

and then, after activating venv and rebooting (as instructed in
console output), issue the commands:

```bash
(ENV3) you@yourhostcomputer $ ssh red
pi@red:~ $ cd ~/cm
pi@red:~/cm $ git clone https://github.com/cloudmesh/cloudmesh-slurm.git
pi@red:~/cm $ cd cloudmesh-slurm
pi@red:~/cm/cloudmesh-slurm $ pip install -e .
pi@red:~/cm/cloudmesh-slurm $ cms help
pi@red:~/cm/cloudmesh-slurm $ cms slurm pi install --workers=red0[1-4] --mount=/dev/sda
```

The user must `ssh` back into the manager after the cluster reboots
and perform the last command (cms slurm pi install...)  3 more
times. The script will inform the user when this is no longer
necessary and SLURM is fully installed.

Notice this method does not need two forward slashes in `--mount`
because it is done on Raspberry Pi OS and not Windows.

You can check if SLURM is installed by issuing on the manager:

`srun --nodes=3 hostname`

and replacing the `--nodes` parameter with the number of workers.

## 4.0 Install Single-Node

Single-node installation, which is a SLURM cluster with only one node,
can be easily configured by using the host command with the manager
and workers listed as the same hostname. In the following example,
`red` is the single-node.

```bash
cms slurm pi install as host --hosts=red,red --mount=//dev//sda
```

## 5.0 Manual Pages

### 5.1 Manual Page for the `slurm` command

Note to execute the command on the command line you have to type in
`cms slurm` and not just `slurm`.

<!--MANUAL-SLURM-->
```
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

```
<!--MANUAL-SLURM-->