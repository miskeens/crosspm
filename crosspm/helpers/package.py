# -*- coding: utf-8 -*-
import os

from crosspm.helpers.archive import Archive
from crosspm.helpers.exceptions import *


class Package(object):
    _packed_path = ''
    _unpacked_path = ''
    _packages = {}
    _raw = []
    _root = False

    def __init__(self, name, pkg, params, downloader, adapter, parser):
        if type(pkg) is int:
            if pkg == 0:
                self._root = True
        self._name = name
        self._pkg = pkg
        self._params = params
        self._adapter = adapter
        self._parser = parser
        self._downloader = downloader

    def download(self, dest_path, force=False):
        if force or not self._unpacked_path:
            dest_path = os.path.realpath(os.path.join(dest_path, self._name))
            self._packed_path = self._adapter.download_package(self._pkg, dest_path)
        return self._packed_path

    def get_file(self, file_name, temp_path=None):
        if not temp_path:
            temp_path = self._downloader.temp_path
        temp_path = os.path.realpath(os.path.join(temp_path, self._name))

        _dest_file = Archive.extract_file(self._packed_path, file_name, temp_path)

        return _dest_file

    def find_dependencies(self, depslock_file_path):
        self._raw = [x for x in self._parser.iter_packages_params(depslock_file_path)]
        self._packages = self._downloader.get_packages(self._raw)

    def unpack(self, dest_path=''):
        Archive.extract(self._packed_path, dest_path)

    def pack(self, src_path):
        Archive.create(self._packed_path, src_path)

    def print(self, level=0):
        _sign = ' '
        if not self._root:
            _sign = '+' if self._unpacked_path else '-'
        _left = '{}{}'.format(' ' * 4 * level, _sign)
        print_stderr('{}{}'.format(_left, self._name))
        for _pkg_name, _pkg in self._packages.items():
            if not _pkg:
                _left = '{}-'.format(' ' * 4 * (level + 1))
                print_stderr('{}{}'.format(_left, _pkg_name))
            else:
                _pkg.print(level + 1)
        if self._root:
            print_stderr('')

    def get_name_and_path(self):
        return self._name, self._unpacked_path
