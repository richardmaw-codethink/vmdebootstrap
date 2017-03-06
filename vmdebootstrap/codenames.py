"""
  Wrapper for distro information
"""
# -*- coding: utf-8 -*-
#
#  codenames.py
#
#  Copyright 2015 Neil Williams <codehelp@debian.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime
from distro_info import DebianDistroInfo, UbuntuDistroInfo
from vmdebootstrap.base import Base

# pylint: disable=missing-docstring


class Codenames(Base):

    name = 'codenames'

    def __init__(self):
        super(Codenames, self).__init__()
        self.debian_info = DebianDistroInfo()
        self.ubuntu_info = UbuntuDistroInfo()
        self.settings = None

    def define_settings(self, settings):
        self.settings = settings

    def suite_to_codename(self, distro):
        suite = self.debian_info.codename(distro, datetime.date.today())
        if not suite:
            return distro
        return suite

    def distributor_of(self, distro):
        distro = self.suite_to_codename(distro)
        if self.ubuntu_info.valid(distro):
            return 'ubuntu'
        return 'debian'

    def was_oldstable(self, limit):
        suite = self.suite_to_codename(self.settings['distribution'])
        # this check is only for debian
        if not self.debian_info.valid(suite):
            return False
        return suite == self.debian_info.old(limit)

    def was_stable(self, limit):
        suite = self.suite_to_codename(self.settings['distribution'])
        # this check is only for debian
        if not self.debian_info.valid(suite):
            return False
        return suite == self.debian_info.stable(limit)

    def kernel_package(self):
        packages = []
        if self.settings['no-kernel'] or self.settings['kernel-package']:
            return packages
        if self.settings['arch'] == 'i386':
            # wheezy (which became oldstable on 04/25/2015) used '486'
            if self.was_oldstable(datetime.date(2015, 4, 26)):
                kernel_arch = '486'
            else:
                kernel_arch = '586'
        elif self.settings['arch'] == 'armhf':
            kernel_arch = 'armmp'
        elif self.settings['arch'] == 'ppc64el':
            kernel_arch = 'powerpc64le'
        else:
            kernel_arch = self.settings['arch']
        packages.append('linux-image-%s' % kernel_arch)
        return packages
