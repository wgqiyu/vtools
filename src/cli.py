import typer
from rich.console import Console
from rich.table import Table

from vtools import ESXi
import re

app = typer.Typer()
console = Console()


def filter_by_name(vim_obj, rule):
    return re.search(rule, vim_obj.vim_obj.name)


@app.command()
def list_vm():
    table = Table(show_header=True, header_style="bold magenta")
    vm_list = esxi.list_vm()
    table.add_column("Vm Name", style="dim", width=12)
    table.add_column("Path", style="dim", width=25)
    table.add_column("Power State", style="dim", width=12)
    for vm in vm_list:
        table.add_row(vm.name, vm.path, vm.state)
    console.print(table)


@app.command()
def list_datastore():
    table = Table(show_header=True, header_style="bold magenta")
    ds_list = esxi.list_datastore()
    table.add_column("Datastore Name", style="dim", width=40)
    table.add_column("Type", style="dim", width=8)
    for ds in ds_list:
        table.add_row(ds.name, ds.type)
    console.print(table)


@app.command()
def create_vm(name: str, func: str, datastore_name: str):
    console.print(esxi.create_vm(name=name, datastore=esxi.get_datastore(eval(func), datastore_name)))


@app.command()
def destroy_vm(func: str, rule: str):
    esxi.delete_vm(vm=esxi.get_vm(eval(func), rule))


if __name__ == "__main__":
    esxi = ESXi(ip="10.161.162.8", user="root", pwd="CSEQz4d+r8jeM*lS")
    print("+++++++++++++++++++++ Connected to ESXi ++++++++++++++++++++++++++++++++")
    app()

    # esxi.import_ovf(name='win11_vm',
    #                 datastore=esxi.get_datastore(
    #                     lambda datastore: datastore.name == 'local-0'),
    #                 ovf_url='http://sftp-eng.eng.vmware.com/vmstorage/qe/windows/windows11/64/111538-Windows-11-v21H2-64-Enterprise-NVMe-Tools/111538-Windows-11-v21H2-64-Enterprise-NVMe-Tools.ovf')
