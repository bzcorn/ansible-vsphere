#!/usr/bin/python

import pysphere
import argparse
import getpass


def build_arg_parser():
    """
    Builds a standard argument parser with arguments for talking to vCenter


    """
    parser = argparse.ArgumentParser(
        description='Standard Arguments for talking to vCenter')

    parser.add_argument('-n', '--name',
                        required=True,
                        action='store',
                        help='Name of the Cloned VM')

    parser.add_argument('-s', '--source',
                        required=True,
                        action='store',
                        help='Name of VM to be Cloned')

    parser.add_argument('-r', '--resourcePool',
                        required=True,
                        action='store',
                        help='Resource Pool that the Cloned VM will land in')

    parser.add_argument('-d', '--datastore',
                        required=True,
                        action='store',
                        help='Datastore that the Cloned VM will write to')

    return parser


def prompt_for_password(args):
    """
    if no password is specified on the command line, prompt for it
    """
    if not args.password:
        args.password = getpass.getpass(
            prompt='Enter password for host %s and user %s: ' %
                   (args.host, args.user))
    return args


def get_args():
    """
    Supports the command-line arguments needed to form a connection to vSphere.
    """
    parser = build_arg_parser()

    args = parser.parse_args()

    return args


def getHostByName(server, name):
    mor = None
    for host_mor, host_name in server.get_hosts().items():
        if host_name == name: mor = host_mor; break
    return mor

def getResourcePoolByName(server, resourcepool):
    mor = None
    for rp_mor, rp_path in server.get_resource_pools().items():
        if resourcepool in rp_path : mor = rp_mor; break
    return mor

def getDatastoreByName(server, name):
    mor = None
    for ds_mor, ds_path in server.get_datastores().items():
        if ds_path == name: mor = ds_mor; break
    return mor

def vmClone(name, vmTemplateName, resourcepool, host, datastore, sync):
    #name: name of cloned VM;
    #vmTemplateName: name of source template;
    #labName: VM''s belong to a training lab;
    #host: to deploy the VM on;
    #labgroup: sequence number of lab system to use;
    #sync: synchronous mode or not

    vm = vCenterServer.get_vm_by_name(name=vmTemplateName)
    host_mor = getHostByName(vCenterServer, host)   #locate destination host MOR
    rp_mor = getResourcePoolByName(vCenterServer,resourcepool)   # locate default resource pool of destination host (the resource pool which parent folder is equal to the parent folder of the host)
    ds_mor = getDatastoreByName(vCenterServer, datastore)   # destination data store
    if sync:  # be careful,  vm.clone returns different objects based on whether sync is true or false
        clonedVM = vm.clone(name, sync_run=True, resourcepool=rp_mor, datastore=ds_mor, host=host_mor, power_on=False) # returns a VM object
        return
    else:
        return vm.clone(name, sync_run=False, resourcepool=rp_mor, datastore=ds_mor, host=host_mor, power_on=False)  # returns a VITask object


def main():
    """
    Simple command-line program for listing the virtual machines on a system.
    """

    args = get_args()

    print vmClone(args.name,args.source,args.resourcePool,"elkvmw03.thoughtworks.com",args.datastore,1)

    return 0

# Start program
vCenterServer = pysphere.VIServer()
# Place in connection strings directly
vCenterServer.connect('', '', '')

if __name__ == "__main__":
    main()
