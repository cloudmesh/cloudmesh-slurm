from cloudmesh.common.Host import Host
from cloudmesh.common.Printer import Printer
from cloudmesh.common.parameter import Parameter
from pprint import pprint
from cloudmesh.common.console import Console
import sys
import time
from cloudmesh.common.util import yn_choice
# r = Host.ping("red,red0[1-4]")
# print(r)


class Workflow:

    def __init__(self,names,trials=1,delay=1):
        self.names = names
        self.trials = trials
        self.delay = delay

    def _print(self,results):
        output = 'table'

        if output in ['table', 'yaml']:
            print(Printer.write(results,
                                order=['host', 'success', 'stdout'],
                                output=output))
        else:
            pprint(results)


    def check_if_ping(self):


        for i in range(self.trials):
            results = Host.ping(hosts=self.names)
            self._print(results)
            pprint(results)
            success = True
            for entry in results:
                if not entry["success"]:
                    success = False
                    continue
            print(success)
            if not success:
                time.sleep(self.delay)
        if not success:
            Console.error(f"Too many tries. Failed after {self.trials} trials. ssh failed.")
            sys.exit()
        return success

    def check_if_up(self):

        for i in range(self.trials):
            results = Host.ssh(hosts=self.names, command="hostname")
            self._print(results)
            pprint(results)
            for entry in results:
                success = entry["host"] == entry["stdout"]
                if not success:
                    continue
                print(success)
                if not success:
                    time.sleep(self.delay)
            if not success:
                Console.error("ssh failed.")
        if not success:
            Console.error(f"Too many tries. Failed after {self.trials} trials. ssh failed.")
            sys.exit()
        return success


    def run(self,steps):

        # workflow should have step 1 through 4
        # workflow = [a,b,c,d]

        for step in steps:
            step()
            # self.check_if_ping()
            # self.check_if_up()
            # success = self.check_if_ping() and self.check_if_up()
            # if not success:
                # Console.error("Not succeeded.")
                # sys.exit()

