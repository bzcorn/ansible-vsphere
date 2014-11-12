#!/usr/bin/python

import pysphere

vCenterServer = pysphere.VIServer()
vCenterServer.connect('{{ vcenter_hostname }}', '{{ vcenter_username }}', '{{ vcenter_password }}')

vm1 = vCenterServer.get_vm_by_name('{{ vm_guest_name }}')


print vm1.get_property('ip_address', from_cache=False)
