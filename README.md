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
    - [3.1 Install cloudmesh](#31-install-cloudmesh)
    - [3.2 Install SLURM Directly on Pi](#32-install-slurm-directly-on-pi)
  - [4.0 Install Single-Node](#40-install-single-node)
  - [5.0 MPI Example](#50-mpi-example)
  - [6.0 Manual Pages](#60-manual-pages)
    - [6.1 Manual Page for the `slurm` command](#61-manual-page-for-the-slurm-command)

<!--TOC-->

## 1.0 Installation

The installation takes around an hour on a
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
burned your SD Cards and is referred to as `you@yourlaptop`. This 
machine can be used to `ssh` into each of the Pis.


To install it, use the command:

```bash
cms slurm pi install as host --hosts=red,red0[1-3] --mount=//dev//sda
```

The mount parameter is meant to have double slashes no matter the OS of the host.

The `--hosts` parameter needs to include the hostnames of your cluster, including
manager and workers, separated by comma using a parameterized naming scheme.

The `--mount` parameter points to the mount place of your USB,
inserted in the top-most blue USB3.0 port (on Pi 4's) on your manager PI. 

WARNING: This USB drive ***will be formatted*** and all data on it will be erased.

The command will take a long time to finish. It may appear to not progress 
at certain points, but please be patient. However they will last hopefully not longer 
than 45 minutes. The reason this takes such a long time is that at time of writing 
of this tutorial, the prebuilt SLURM
packages did not work, so we compile it from source.

Once the script completes, you can check if SLURM is installed by issuing
on the manager:

`srun --nodes=3 hostname`

and replacing the `--nodes` parameter with the number of workers.

You will see an output similar to

```bash
(ENV3) pi@red:~ $ srun --nodes=3 hostname
red01
red02
red03
(ENV3) pi@red:~ $
```

The nodes may be out of order. That is okay and normal.

## 3.0 Method 2 - Install on Manager

### 3.1 Install cloudmesh

This method involves the user logging into the manager via `ssh` and 
first installing cloudmesh in the manager with:

```bash
(ENV3) you@yourhostcomputer $ ssh red
pi@red $ curl -Ls http://cloudmesh.github.io/get/pi | sh -
```

This output is printed upon successful installation.

```bash
Please activate with

    source ~/ENV3/bin/activate

Followed by a reboot
```

After activating venv with the source command and rebooting 
via `sudo reboot`, issue the commands:

```bash
(ENV3) you@yourhostcomputer $ ssh red
pi@red:~ $ cd ~/cm
pi@red:~/cm $ git clone https://github.com/cloudmesh/cloudmesh-slurm.git
pi@red:~/cm $ cd cloudmesh-slurm
pi@red:~/cm/cloudmesh-slurm $ pip install -e .
pi@red:~/cm/cloudmesh-slurm $ cms help
```

The slurm command should appear in the list.

### 3.2 Install SLURM Directly on Pi

Run this command to begin SLURM installation:

```bash
pi@red:~/cm/cloudmesh-slurm $ cms slurm pi install --workers=red0[1-3] --mount=/dev/sda
```

The user must `ssh` back into the manager after the cluster reboots
and perform the last command (cms slurm pi install...)  3 more
times. The script will inform the user when this is no longer
necessary and SLURM is fully installed.

Notice this method does not need two forward slashes in `--mount`
because it is done on Raspberry Pi OS and not Windows. It can only
be done on Raspberry Pi OS because the method is purposefully
done on the manager Pi, to begin with.

You can check if SLURM is installed by issuing on the manager:

`srun --nodes=3 hostname`

and replacing the `--nodes` parameter with the number of workers.

You will see an output similar to

```bash
(ENV3) pi@red:~ $ srun --nodes=3 hostname
red01
red02
red03
(ENV3) pi@red:~ $
```

The nodes may be out of order. That is okay and normal.

## 4.0 Install Single-Node

To make job management simple, we can install SLURM on one computer.
This one computer has no workers and is a manager to its own self.
The user can make and automate jobs for simplicity's sake, and the
same computer will carry out those jobs.

Single-node installation, which is a SLURM cluster with only one node,
can be easily configured by using the host command with the manager
and workers listed as the same hostname. In the following example,
`red` is the single-node.

```bash
cms slurm pi install as host --hosts=red,red --mount=//dev//sda
```

## 5.0 MPI Example

To run a test MPI example, `ssh` into the manager and then use
the `example` command. This is only possible if `cms` is installed
on the Pi; if you have not done this because you installed SLURM
via the host method, then refer to section 3.1 to install cloudmesh on Pi.
Then run the following (change the number
after `--n` to the number of nodes):

```bash
(ENV3) you@yourhostcomputer $ ssh red
pi@red:~ $ cms slurm pi example --n=3
```

This `cms slurm` command runs `salloc -N 3 mpiexec python -m mpi4py.bench helloworld`
but the number after `-N` is altered to whatever is input for the `--n` parameter.
Do not run the `salloc` command. It is unnecessary when we have already implemented
it within the aforementioned `cms slurm pi example` command. It is just listed here
for reference.
The output will be similar to:

```bash
pi@red:~ $ cms slurm pi example --n=3
salloc: Granted job allocation 17
Hello, World! I am process 0 of 3 on red01.
Hello, World! I am process 1 of 3 on red02.
Hello, World! I am process 2 of 3 on red03.
salloc: Relinquishing job allocation 17
```

## 6.0 Manual Pages

### 6.1 Manual Page for the `slurm` command

Note to execute the command on the command line you have to type in
`cms slurm` and not just `slurm`.

TODO: there is a todo in the manpage

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
