from diamond import *
import diamond.collector

import subprocess

class UPSCollector(diamond.collector.Collector):
    """
    This class collects data from NUT, a UPS interface for linux.

    Requires: nut/upsc to be installed, configured and running.
    """

    def get_default_config(self):
        """
        Returns default collector settings.
        """

        return {
            'path': 'ups',
            'ups_name': 'cyberpower',
            'bin': '/bin/upsc'
        }

    def collect(self):
        if not os.access(self.config['bin'], os.X_OK):
            self.log.error(self.config['bin']+" is not executable")
            return False
        
        p = subprocess.Popen([self.config['bin'], self.config['ups_name']], stdout=subprocess.PIPE)

        for ln in p.communicate()[0].splitlines():
            datapoint = ln.split(": ")

            try:
                val = float(datapoint[1])
            except:
                continue

            if len(datapoint[0].split(".")) == 2:
                # If the metric name is the same as the subfolder
                # double it so it's visible.
                name = ".".join([datapoint[0], datapoint[0].split(".")[1]])
            else:
                name = datapoint[0]

            self.publish(name, val)
