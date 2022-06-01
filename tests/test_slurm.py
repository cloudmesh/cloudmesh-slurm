###############################################################
# pytest -v --capture=no tests/test_slurm.py
# pytest -v  tests/test_slurm.py
# pytest -v --capture=no  tests/test_slurm..py::Test_slurm::<METHODNAME>
###############################################################
import pytest
from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.Shell import Shell
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import HEADING
from cloudmesh.slurm.slurm import Slurm

@pytest.mark.incremental
class TestConfig:

    def test_script_executor(self):
        HEADING()
        script = '''
            workers: sudo cp /nfs/slurm.conf /usr/local/etc/slurm.conf
            hosts:   sudo mkdir /var/spool/slurmd
            manager: cd ~/slurm/etc/ && sudo cp slurmctld.service /etc/systemd/system
            '''
        Benchmark.Start()
        Slurm.script_executor(script, "hosts", "manager", "workers", dryrun=True)
        Benchmark.Stop()

        assert True

class rest:

    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, sysinfo=False, tag="cmd5")
