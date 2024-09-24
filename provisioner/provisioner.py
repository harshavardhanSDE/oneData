# @provisioner

# This CLI is built for development grade, big data tools for learning purpose only. and 
# strictly NOT FOR PROVISIONING PRODUCTION ENVIRONMENT.


# For command line interface: @https://click.palletsprojects.com/en/8.1.x/
import click

# Templating engine: @https://jinja.palletsprojects.com/en/3.1.x/api/#basics
from jinja2 import Environment, FileSystemLoader

# Process init: @https://python101.pythonlibrary.org/chapter19_subprocess.html
import subprocess

# @https://docs.python.org/3/library/pathlib.html
from pathlib import Path

# Terminal UI: @https://tqdm.github.io/
import tqdm
import time
import sys
import itertools
import threading
import os

TEMPLATES_DIRECTORY = Path(__file__).parent / "templates"

DIST = Path("dist")
DIST.mkdir(exist_ok=True)

VAGRANT_FILE = DIST / "Vagrantfile"
INVENTORY = DIST / "inventory"
PLAYBOOK = DIST / "playbook.yml"
CONFIG = DIST / "cluster_config.yml"
env = Environment(loader=FileSystemLoader(TEMPLATES_DIRECTORY))

# @Terminal UI

# @Spinner: 
class t_ui:
    loading_cycle = itertools.cycle(["|", "/", "-", "\\"])
    def __init__(self, base_msg = "Provisioning", message = " resources"):
        self.stop_running = False
        self.info = base_msg + message

    # to star the cycle
    def start(self):
        def cycle():
            while not self.stop_running:
                sys.stdout.write(f"\r{self.info} {next(self.loading_cycle)}")
                sys.stdout.flush()
                time.sleep(0.1)

            sys.stdout.write('\r' + ' '*(len(self.info) + 2) + '\r' )

        self.cycle_thread = threading.Thread(target=cycle)
        self.cycle_thread.start()
    
    # to stop the cycle
    def stop(self):
        self.stop_running = True
        self.cycle_thread.join()

    # @Progress Bar
    def progress_bar():
        pass




        
def engine():
    @click.command()
    @click.option("--num-nodes", prompt = "Number of Nodes ( VMs )  to provision for the cluster.", default = 2, type = int)
    @click.option('--memory', prompt="Memory per node (MB)", default= 2048, type=int)
    @click.option('--cpus', prompt="CPUs per node", default= 2, type=int)
    @click.option('--services', prompt="Services to install (comma-separated, e.g., hadoop,cassandra,spark)", default= ["hadoop", "spark"] )
    @click.option('--box-name', default= "virtual_box", help="Vagrant box name")
    @click.option('--host-prefix', default= "default_cluster", help="Host IP prefix for the VMs")
    
    def template_gen(num_nodes, memory, cpus, services, box_name, host_prefix):
        try:
            if num_nodes < 1 :
                raise ValueError("Number of nodes must be atleast one!")
        except ValueError as err:
            click.secho(f"Error {err}", fg="red", bold=True)
        
        try:
            if cpus > os.cpu_count():
                raise ValueError("Number of VM cores should be less than the available physical cores!")
        except ValueError as err:
            click.secho(f"Error {err}", fg="green", bold= True)

        services_list = services.split(",")

        service_flags = {
        "hadoop": "hadoop" in services_list,
        "cassandra": "cassandra" in services_list,
        "spark": "spark" in services_list,
        "hive": "hive" in services_list,
        "flink": "flink" in services_list,
        "kafka": "kafka" in services_list,
        "storm": "storm" in services_list,
        "airflow": "airflow" in services_list,
        "drill": "drill" in services_list,
        "hudi": "hudi" in services_list,
        "presto": "presto" in services_list,
        "samza": "samza" in services_list,}
        
        template = env.get_template("Vagrantfile.j2")
        vagrantfile_content = template.render(num_nodes=num_nodes, memory=memory, cpus=cpus, box_name=box_name)
        VAGRANT_FILE.write_text(vagrantfile_content)
        print("Generated Vagrantfile")

        template = env.get_template("inventory.j2")
        inventory_content = template.render(num_nodes=num_nodes, host_prefix=host_prefix)
        INVENTORY.write_text(inventory_content)
        print("Generated Ansible inventory")

        template = env.get_template("playbook.yml.j2")
        playbook_content = template.render(services=service_flags)
        PLAYBOOK.write_text(playbook_content)
        print("Generated Ansible playbook")

        ui = t_ui()

        ui.start()
        subprocess.run(["vagrant", "up"], cwd=DIST)
        ui.stop()

        ui.start()
        subprocess.run(["vagrant", "provision"], cwd=DIST)
        ui.stop()

    # After the cluster is up, generate the configuration file
        node_ips = [f"{host_prefix}.{i+10}" for i in range(num_nodes)]  # Example IPs for nodes
        master_node_ip = node_ips[0]

    # Prepare configuration details
        config_data = {
            # "cluster_name": cluster_name,
            "num_nodes": num_nodes,
            "node_ips": node_ips,
            "master_node_ip": master_node_ip,
            "service_ips": {
                "hadoop": master_node_ip if service_flags["hadoop"] else None,
                "spark": master_node_ip if service_flags["spark"] else None,
                "hive": master_node_ip if service_flags["hive"] else None,
                "cassandra": node_ips if service_flags["cassandra"] else None,
                "kafka": node_ips if service_flags["kafka"] else None,
                "flink": master_node_ip if service_flags["flink"] else None,
                "storm": master_node_ip if service_flags["storm"] else None,
                "airflow": master_node_ip if service_flags["airflow"] else None,
                "drill": master_node_ip if service_flags["drill"] else None,
                "presto": master_node_ip if service_flags["presto"] else None,
                "samza": master_node_ip if service_flags["samza"] else None,
        },
    }

    # Generate YAML configuration file
        config_template = env.get_template("cluster_config.yml.j2")
        config_content = config_template.render(**config_data)
        CONFIG.write_text(config_content)
        print(f"Generated cluster configuration file: {CONFIG}")


    template_gen()

        

        

if __name__ == "__main__":
    engine()
       
            
        



