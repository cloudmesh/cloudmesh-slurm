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
  - [6.0 Interactive Job](#60-interactive-job)
  - [7.0 Using sbatch](#70-using-sbatch)
  - [8.0 Manual Pages](#80-manual-pages)
    - [8.1 Manual Page for the `slurm` command](#81-manual-page-for-the-slurm-command)

<!--TOC-->

## 1.0 Installation

The installation takes around an hour on a cluster of four Raspberry
Pi 4 Model B computers.

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
(ENV3) you@yourlaptop $ cms slurm pi install as host --hosts=red,red0[1-4]
```

The `--hosts` parameter needs to include the hostnames of your
cluster, including manager and workers, separated by comma using a
parameterized naming scheme.

The user can also specify a `--partition` parameter, as in
`--partition=mycluster`, to personalize the name of the partition.

The command will take a long time to finish. It may appear to not
progress at certain points, but please be patient. However they will
last hopefully not longer than 45 minutes. The reason this takes such
a long time is that at time of writing of this tutorial, the prebuilt
SLURM packages did not work, so we compile it from source.

Once the script completes, you can check if SLURM is installed by
issuing on the manager:

`(ENV3) pi@red:~ $ srun --nodes=4 hostname`

and replacing the `--nodes` parameter with the number of workers.

You will see an output similar to

```bash
(ENV3) you@yourlaptop $ ssh red
(ENV3) pi@red:~ $ srun --nodes=4 hostname
red01
red02
red03
red04
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
pi@red:~/cm/cloudmesh-slurm $ cms slurm pi install --workers=red0[1-4]
```

The user can also specify a `--partition` parameter, as in
`--partition=mycluster`, to personalize the name of the partition.

The user must `ssh` back into the manager after the cluster reboots
and perform the last command (cms slurm pi install...) 3 more
times. The script will inform the user when this is no longer
necessary and SLURM is fully installed.

You can check if SLURM is installed by issuing on the manager:

`srun --nodes=4 hostname`

and replacing the `--nodes` parameter with the number of workers.

You will see an output similar to

```bash
(ENV3) pi@red:~ $ srun --nodes=4 hostname
red01
red02
red03
red04
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
cms slurm pi install as host --hosts=red,red
```

## 5.0 MPI Example

To run a test MPI example, `ssh` into the manager and then use the
`example` command. This is only possible if `cms` is installed on the
Pi; if you have not done this because you installed SLURM via the host
method, then refer to section 3.1 to install cloudmesh on Pi.  Then
run the following (change the number after `--n` to the number of
nodes):

```bash
(ENV3) you@yourhostcomputer $ ssh red
pi@red:~ $ cms slurm pi example --n=4
```

This `cms slurm` command runs `salloc -N 4 mpiexec python -m
mpi4py.bench helloworld` but the number after `-N` is altered to
whatever is input for the `--n` parameter.  Do not run the `salloc`
command. It is unnecessary when we have already implemented it within
the aforementioned `cms slurm pi example` command. It is just listed
here for reference.  The output will be similar to:

```bash
pi@red:~ $ cms slurm pi example --n=4
salloc: Granted job allocation 17
Hello, World! I am process 0 of 4 on red01.
Hello, World! I am process 1 of 4 on red02.
Hello, World! I am process 2 of 4 on red03.
Hello, World! I am process 3 of 4 on red04.
salloc: Relinquishing job allocation 17
```

## 6.0 Interactive Job

You can start an interactive job by issuing the following:

```bash
(ENV3) pi@red:~ $ srun --nodes=1 --ntasks-per-node=1 --time=01:00:00 --pty bash -i
pi@red01:~ $
```

This works in home dir, but not if you stand in other dir.

## 7.0 Using sbatch

The cloudmesh-mpi repository contains a Python file that automatically
creates job submissions using the `sbatch` command. `sbatch` allows
for easy customization of job parameters, such as where the output
of the commands should reside, how much time should be allotted for
the job, how much memory should be allotted per CPU, and others.

The Python program, `100jobs.py`, is located at
<https://github.com/cloudmesh/cloudmesh-mpi/blob/main/examples/slurm/100jobs.py>

To use the cloudmesh-mpi Python program, named 100 jobs for its
creation of 100 jobs that execute the `sleep` command for a short
amount of time, execute the following commands.

In the case that cloudmesh-mpi is not downloaded:

```bash
(ENV3) pi@red:~ $ cd cm
(ENV3) pi@red:~/cm $ git clone https://github.com/cloudmesh/cloudmesh-mpi.git
(ENV3) pi@red:~/cm $ cd cloudmesh-mpi/examples/slurm
(ENV3) pi@red:~/cm/cloudmesh-mpi/examples/slurm $ cp 100jobs.py ~
(ENV3) pi@red:~/cm/cloudmesh-mpi/examples/slurm $ cd
(ENV3) pi@red:~ $ python 100jobs.py
```

This program only works if the `nfs` shared file system is installed
on the cluster. The shared file system should already be installed if
the SLURM installation has been run successfully.

The output files of the 100 jobs can be found inside `/nfs/tmp/`:

```bash
(ENV3) pi@red:~ $ cat job-0.slurm
#!/bin/bash
#SBATCH -o job-0.out
#SBATCH -e job-0.err

hostname
echo $SLURM_JOB_NAME
NAME="${SLURM_JOB_NAME%%.*}"
echo $NAME
sleep 5.473056730256757

cp ${NAME}.out /nfs/tmp/
cp ${NAME}.err /nfs/tmp/
(ENV3) pi@red:~ $ cd /nfs/tmp
(ENV3) pi@red:/nfs/tmp $ cat job-0.out
red01
job-0.slurm
job-0
```

## Using Slurm on local PI file space

Often it is time consuming during a slurm run to copy all the files
and data to a remote host. This is valid also for accessing
NFS. Furthermore, if you have a lareg number of nodes this could be
problematic as the nodes compeet with each other. In such cases its is
useful to be able to copy the data and potentially programs before you
run sbatch. However, you must dod this for all nodes that you expect
to be using for the batch job. As we are in full control of the
Raspberry Pi cluster, we simply copy it to all of them.

Let us assume we hafe a clutsre burned for red,red0[1-2]. Let us
create a simple program and distribute it to the workers.


```bash
red$ mkdir ~/tmp

red$ echo "#! /usr/bin/env python" > tmp/hello.py
red$ echo "import os" > tmp/hello.py
red$ echo "os.system('hostname')" > tmp/hello.py

red$ chmod a+x ~/tmp/hello.py
red$ rsync -a ~/tmp red01:tmp
red$ rsync -a ~/tmp red02:tmp
```

Now we can run it with

```bash
red$ srun -n 8 /home/pi/tmp/hello.py
```

As the PI4 has four threads and we copied the program to each pi, we
will see an outut where each thread will execute the hostname command.
We will see the following output. Please note that the order can be
different.

```
red02
red02
red02
red02
red01
red01
red01
red01
```


## 8.0 Manual Page for the `slurm` command

Note to execute the command on the command line you have to type in
`cms slurm` and not just `slurm`.

<!--MANUAL-SLURM-->
```
      slurm pi install [--workers=WORKERS] [--mount=MOUNT]
      slurm pi install as host [--os=OS] [--hosts=HOSTS] [--mount=MOUNT]
      slurm pi example --n=NUMBER

This command installs slurm on the current PI and also worker nodes if you specify them.

The manager can also be a worker by using the single-node method. For example, red can be
a manager and worker, simultaneously, by issuing
cms slurm pi install as host --hosts=red,red --mount=//dev//sda

Arguments:
  COMMAND  the slurm command to be executed [default: salloc]

Options:

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


```
<!--MANUAL-SLURM-->
