#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sVolume import K8sVolume
from kubernetes.models.v1.BaseModel import BaseModel
from kubernetes.models.v1.ContainerPort import ContainerPort
from kubernetes.models.v1.Probe import Probe
from kubernetes.models.v1.ResourceRequirements import ResourceRequirements


class Container(BaseModel):

    def __init__(self, name=None, image=None, model=None):
        super(Container, self).__init__()

        self._args = []
        self._command = []
        self._ports = []

        self.name = name
        self.image = image
        self.liveness_probe = None
        self.readiness_probe = None
        self.working_dir = None
        self.resources = None
        self.volume_mounts = None

    # ------------------------------------------------------------------------------------- args

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, args=None):
        msg = 'Container: args: [ {0} ] is invalid.'.format(args)
        if not isinstance(args, list):
            raise SyntaxError(msg)
        for x in args:
            if not isinstance(x, str):
                raise SyntaxError(msg)
        self._args = args

    # ------------------------------------------------------------------------------------- command

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, command=None):
        msg = 'Container: command: [ {0} ] is invalid.'.format(command)
        if not isinstance(command, list):
            raise SyntaxError(msg)
        for x in command:
            if not isinstance(x, str):
                raise SyntaxError(msg)
        self._command = command

    # ------------------------------------------------------------------------------------- ports

    @property
    def ports(self):
        return self._ports

    @ports.setter
    def ports(self, ports=None):
        msg = 'Container: ports: [ {0} ] is invalid.'.format(ports)
        if not isinstance(ports, list):
            raise SyntaxError(msg)
        for x in ports:
            if not isinstance(x, ContainerPort):
                raise SyntaxError(msg)
        self._ports = ports
















        if model is not None:
            assert isinstance(model, dict)
            self.model = model
            if 'status' in self.model:
                self.model.pop('status', None)
            if 'livenessProbe' in self.model:
                self.liveness_probe = Probe(model=self.model['livenessProbe'])
            if 'readinessProbe' in self.model:
                self.readiness_probe = Probe(model=self.model['readinessProbe'])
            if 'privileged' not in self.model:
                self.model['privileged'] = False
            if 'hostNetwork' not in self.model:
                self.model['hostNetwork'] = False

        else:
            if name is None or image is None:
                raise SyntaxError("name: [ {0} ] and image: [ {1} ] cannot be None.".format(name, image))

            self.model = {
                "name": name,
                "image": image,
                "imagePullPolicy": 'IfNotPresent',
                "privileged": False,
                "hostNetwork": False,
                "terminationMessagePath": "/dev/termination-log",
                "resources": {
                    "requests": {
                        "cpu": "100m",
                        "memory": "32M"
                    }
                }
            }

    def _update_model(self):
        if self.liveness_probe is not None:
            self.model['livenessProbe'] = self.liveness_probe.get()
        if self.readiness_probe is not None:
            self.model['readinessProbe'] = self.readiness_probe.get()
        return self

    def add_port(self, container_port, host_port=None, protocol=None, name=None, host_ip=None):
        portdef = dict()
        if 0 < container_port < 65536:
            portdef['containerPort'] = int(container_port)
            if name is not None:
                portdef['name'] = name
            if host_port is not None and (0 < host_port < 65536):
                portdef['hostPort'] = int(host_port)
            if host_ip is not None:
                portdef['hostIP'] = host_ip
            if protocol is not None and protocol in ['TCP', 'UDP']:
                portdef['protocol'] = protocol
            # Now assign the newly defined port.
            if 'ports' not in self.model.keys():
                self.model['ports'] = []
            self.model['ports'].append(portdef)
        else:
            raise SyntaxError('container_port should be: 0 < container_port < 65536.')
        return self

    def add_env(self, name=None, value=None):
        if name is None or value is None:
            raise SyntaxError('name and value should be strings.')
        else:
            if 'env' not in self.model.keys():
                self.model['env'] = []
            self.model['env'].append({"name": name, "value": value})
        return self

    def add_volume_mount(self, volume=None):
        if not isinstance(volume, K8sVolume):
            raise SyntaxError('Container: volume: [ {0} ] must be a K8sVolume.'.format(volume.__class__.__name__))
        vol = volume.model.model['volumeMount']
        if 'volumeMounts' not in self.model:
            self.model['volumeMounts'] = []
        self.model['volumeMounts'].append(vol)
        return self

    def get_liveness_probe(self):
        return self.liveness_probe

    def get_name(self):
        return self.model['name']

    def get_image(self):
        return self.model['image']

    def get_readiness_probe(self):
        return self.readiness_probe

    def set_arguments(self, args=None):
        if args is None:
            args = []
        else:
            if not isinstance(args, list):
                raise SyntaxError('args should be a list.')
        if 'args' not in self.model.keys():
            self.model['args'] = []
        self.model['args'] = args
        return self

    def set_command(self, cmd=None):
        if cmd is None:
            cmd = []
        else:
            if not isinstance(cmd, list):
                raise SyntaxError('cmd should be a list.')
        if 'command' not in self.model.keys():
            self.model['command'] = []
        self.model['command'] = cmd
        return self

    def set_host_network(self, mode=True):
        if not isinstance(mode, bool):
            raise SyntaxError('mode should be True or False')
        self.model['hostNetwork'] = mode
        return self

    def set_image(self, image=None):
        self.model['image'] = image
        return self

    def set_liveness_probe(self, **kwargs):
        self.liveness_probe = Probe(**kwargs)
        return self

    def set_name(self, name=None):
        if name is None:
            raise SyntaxError('name should be a string.')
        else:
            self.model['name'] = name
        return self

    def set_pull_policy(self, policy='IfNotPresent'):
        if not isinstance(policy, str):
            raise SyntaxError('Policy should be one of: Always, Never, IfNotPresent')
        if policy in ['Always', 'Never', 'IfNotPresent']:
            self.model['imagePullPolicy'] = policy
        else:
            raise SyntaxError
        return self

    def set_privileged(self, mode=True):
        if not isinstance(mode, bool):
            raise SyntaxError('mode should be True or False')
        self.model['privileged'] = mode
        return self

    def set_readiness_probe(self, **kwargs):
        self.readiness_probe = Probe(**kwargs)
        return self

    def set_requested_resources(self, cpu='100m', mem='32M'):
        if not isinstance(cpu, str) or not isinstance(mem, str):
            raise SyntaxError('cpu should be a string like 100m for 0.1 CPU and mem should be a string like 32M, 1G')
        self.model['resources']['requests']['cpu'] = cpu
        self.model['resources']['requests']['memory'] = mem
        return self

    def set_limit_resources(self, cpu='100m', mem='32M'):
        if not isinstance(cpu, str) or not isinstance(mem, str):
            raise SyntaxError('cpu should be a string like 100m for 0.1 CPU and mem should be a string like 32M, 1G')
        assert isinstance(self.model['resources'], dict)
        if 'limits' not in self.model['resources'].keys():
            self.model['resources']['limits'] = dict()
        self.model['resources']['limits']['cpu'] = cpu
        self.model['resources']['limits']['memory'] = mem
        return self
