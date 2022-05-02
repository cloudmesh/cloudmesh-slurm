# Documentation for cms SLURM installation

To use the cloudmesh SLURM command, one must have
cloudmesh installed by using the following
commands.

We assume you are in a venv Python
environment. Ours is called (ENV3)

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

You may proceed if `slurm` shows in
the documented commands.

After following [the burn tutorial](https://cloudmesh.github.io/pi/tutorial/raspberry-burn-windows/)
and ensuring that the cluster is online,
you have two methods of installing
SLURM.

## Method 1 - Install from Host

You can install SLURM on a cluster
by executing commands from the
host computer. The host computer
is the same computer that is
previously referred to as
`you@yourlaptop` and it is
used to `ssh` into the Pis.

Use this command:
```bash
cms slurm pi install as host --hosts=red,red0[1-4] --mount=//dev//sda
```

The `--hosts` parameter should
be edited to have the hostnames
of your manager and workers,
separated by comma.

The `--mount` parameter should
point to the mount place of
your USB, inserted in the top-most
blue USB3.0 port (on Pi 4's),
and ***it will be formatted.***

The command may seem to hang
at certain points, but these
points should not last more
than 45 minutes and are likely
simply building from source.

Once the script ends, there is
an expected error saying that
the Pis cannot be pinged. You
can check if SLURM is installed
by issuing on the manager:

`srun --nodes=3 hostname`

and replacing the `--nodes`
parameter with the number
of workers.

## Method 2 - Install on Manager

This method involves the user
logging into the manager via
`ssh`, installing cloudmesh
via:

```bash
(ENV3) you@yourhostcomputer $ ssh red
pi@red $ curl -Ls http://cloudmesh.github.io/get/pi | sh -
```

and then, after activating venv 
and rebooting (as instructed in
console output), issue the
commands:

```bash
(ENV3) you@yourhostcomputer $ ssh red
pi@red:~ $ cd ~/cm
pi@red:~/cm $ git clone https://github.com/cloudmesh/cloudmesh-slurm.git
pi@red:~/cm $ cd cloudmesh-slurm
pi@red:~/cm/cloudmesh-slurm $ pip install -e .
pi@red:~/cm/cloudmesh-slurm $ cms help
pi@red:~/cm/cloudmesh-slurm $ cms slurm pi install --workers=red0[1-4] --mount=/dev/sda
```

The user must `ssh` back into
the manager after the cluster
reboots and perform the last
command (cms slurm pi install...)
3 more times. The script
will inform the user when
this is no longer necessary
and SLURM is fully installed.

Notice this method does not
need two forward slashes in
`--mount` because it is done
on Raspberry Pi OS and not
Windows.

You can check if SLURM is installed
by issuing on the manager:

`srun --nodes=3 hostname`

and replacing the `--nodes`
parameter with the number
of workers.
