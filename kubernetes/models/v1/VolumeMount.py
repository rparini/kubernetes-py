#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string


class VolumeMount(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_volumemount
    """

    def __init__(self, name=None, mount_path=None, read_only=False, sub_path=None):
        super(VolumeMount, self).__init__()
        self._name = name
        self._mount_path = mount_path
        self._read_only = read_only
        self._sub_path = sub_path

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('VolumeMount: name: [ {0} ] is invalid'.format(name))
        self._name = name

    # ------------------------------------------------------------------------------------- mount_path

    @property
    def mount_path(self):
        return self._mount_path

    @mount_path.setter
    def mount_path(self, path=None):
        if not is_valid_string(path):
            raise SyntaxError('VolumeMount: mount_path: [ {0} ] is invalid.'.format(path))
        self._mount_path = path

    # ------------------------------------------------------------------------------------- read_only

    @property
    def read_only(self):
        return self._read_only

    @read_only.setter
    def read_only(self, ro=False):
        if not isinstance(ro, bool):
            raise SyntaxError('VolumeMount: read_only: [ {0} ] is invalid.'.format(ro))
        self._read_only = ro

    # ------------------------------------------------------------------------------------- sub_path

    @property
    def sub_path(self):
        return self._sub_path

    @sub_path.setter
    def sub_path(self, path=None):
        if path is None:
            path = ""  # default; volume's root
        if not is_valid_string(path):
            raise SyntaxError('VolumeMount: sub_path: [ {0} ] is invalid.'.format(path))
        self._sub_path = path

    # ------------------------------------------------------------------------------------- serialize

    def json(self):
        data = {}
        if self.name:
            data['name'] = self.name
        if self.read_only:
            data['readOnly'] = self.read_only
        if self.mount_path:
            data['mountPath'] = self.mount_path
        if self.sub_path:
            data['subPath'] = self.sub_path
        return data
