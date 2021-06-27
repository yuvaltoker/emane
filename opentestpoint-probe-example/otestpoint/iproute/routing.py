#
# Copyright (c) 2016-2017,2019 - Adjacent Link LLC, Bridgewater,
# New Jersey
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of Adjacent Link LLC nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# See toplevel COPYING for more information.
#

"""
IP Route probe
"""
from __future__ import absolute_import, division, print_function
from otestpoint.interface import Probe
from otestpoint.interface.measurementtable_pb2 import MeasurementTable
import otestpoint.toolkit.logger as Logger
from .routing_pb2 import Measurement_iproute_routing_tables_ipv4
from .routing_pb2 import Measurement_iproute_routing_tables_ipv6
import socket
import fcntl
import struct
import pyroute2
import subprocess
import re

# note: pyroute2.iproute.IPRoute get_links() contains memory leak at
# least in version 0.3.15.
def if_indextoname(index):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return fcntl.ioctl(
        s.fileno(),
        0x8910,  # SIOCGIFNAME
        struct.pack('16si20s', b'',index,b''))[:16].decode('utf-8').rstrip('\0')

def parse_mcast_route(src,group,iface,ofaces,measurement):
    row = measurement.mcastroutingtable.rows.add()

    value = row.values.add()
    value.type = MeasurementTable.Measurement.TYPE_STRING
    value.sValue = src

    value = row.values.add()
    value.type = MeasurementTable.Measurement.TYPE_STRING
    value.sValue = group

    value = row.values.add()
    value.type = MeasurementTable.Measurement.TYPE_STRING
    value.sValue = iface

    value = row.values.add()
    value.type = MeasurementTable.Measurement.TYPE_STRING

    if len(ofaces):
        value.sValue =ofaces
    else:
        value.sValue = 'NA'

def parse_route(route,oifs,measurement):
    row = measurement.routingtable.rows.add()

    value = row.values.add()
    if 'table' in route:
        value.type = MeasurementTable.Measurement.TYPE_UINTEGER
        value.uValue = route['table']
    else:
        value.type = MeasurementTable.Measurement.TYPE_STRING
        value.sValue = 'NA'

    value = row.values.add()
    value.type = MeasurementTable.Measurement.TYPE_STRING
    dst = route.get('dst')
    value.sValue = 'NA' if dst == None else dst

    value = row.values.add()
    value.type = MeasurementTable.Measurement.TYPE_STRING
    prefsrc = route.get('prefsrc')
    value.sValue = 'NA' if prefsrc == None else prefsrc

    value = row.values.add()
    priority = route.get('priority')
    if priority != None:
        value.type = MeasurementTable.Measurement.TYPE_UINTEGER
        value.uValue = priority
    else:
        value.type = MeasurementTable.Measurement.TYPE_STRING
        value.sValue = 'NA'

    value = row.values.add()
    value.type = MeasurementTable.Measurement.TYPE_STRING
    oif = route.get('oif')

    if oif == None:
        value.sValue = 'NA'
    else:
        if oif not in oifs:
            oifs[oif] = if_indextoname(oif)

        value.sValue = oifs[oif]

    value = row.values.add()
    value.type = MeasurementTable.Measurement.TYPE_STRING
    gateway = route.get('gateway')
    value.sValue = 'NA' if gateway == None else gateway

    value = row.values.add()
    value.type = MeasurementTable.Measurement.TYPE_UINTEGER
    value.uValue = route['dst_len']

    value = row.values.add()
    value.type = MeasurementTable.Measurement.TYPE_UINTEGER
    value.uValue = route['proto']

    value = row.values.add()
    value.type = MeasurementTable.Measurement.TYPE_UINTEGER
    value.uValue = route['tos']


class Routing(Probe):
    def initialize(self,configurationFile=None):
        """
        Initialize the probe.

        Returns:
        The probe name list.
        """
        self._logger.log(Logger.DEBUG_LEVEL,
                         "/iproute/routing initialize"
                         " configuration: %s" % configurationFile)


        self._ipdb = pyroute2.IPDB()

        self._mroute_regex = re.compile(r'\(([^,]+), ([^,]+)\)\s+Iif: ([^\s]+)\s+Oifs:(( [^\s]+){0,})')

        labels = ['Table',
                  'Dst',
                  'Pref Src',
                  'Priority',
                  'OIF',
                  'Gateway',
                  'Dst Len',
                  'Proto',
                  'TOS']

        mcast_labels = ['Src',
                        'Group',
                        'IFace',
                        'OFaces']

        self._measurement4 = Measurement_iproute_routing_tables_ipv4()

        self._measurement4.routingtable.labels.extend(labels)

        self._measurement4.mcastroutingtable.labels.extend(mcast_labels)

        self._measurement6 = Measurement_iproute_routing_tables_ipv6()

        self._measurement6.routingtable.labels.extend(labels)

        self._measurement6.mcastroutingtable.labels.extend(mcast_labels)

        return ('IPRoute.Routing.Tables.IPv4',
                'IPRoute.Routing.Tables.IPv6')

    def start(self):
        """
        Starts the probe.

        This method does nothing.
        """
        self._logger.log(Logger.DEBUG_LEVEL,'/iproute/routing start')

    def stop(self):
        """
        Stops the probe.

        This method does nothing.
        """
        self._logger.log(Logger.DEBUG_LEVEL,'/iproute/routing stop')

    def destroy(self):
        """
        Destroys the probe.

        This method does nothing.
        """
        self._logger.log(Logger.DEBUG_LEVEL,'/iproute/routing destroy')

        self._ipdb.release()

    def probe(self):
        """
        Gets the current time of day probe data
        """
        self._logger.log(Logger.DEBUG_LEVEL,'/iproute/routing probe')

        del self._measurement4.routingtable.rows[:]

        del self._measurement4.mcastroutingtable.rows[:]

        del self._measurement6.routingtable.rows[:]

        del self._measurement6.mcastroutingtable.rows[:]

        oifs = {}

        for table in list(self._ipdb.routes.tables.keys()):
            routes = self._ipdb.routes.tables[table]

            # older versions of pyroute2 have dict routes not list
            if isinstance(routes,dict):
                routes = list(routes.values())

            for route in routes:
                if route['family'] == 2:
                    parse_route(route,oifs,self._measurement4)
                elif route['family'] == 10:
                    parse_route(route,oifs,self._measurement6)


        p = subprocess.Popen(['ip','mroute'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)

        stdout, stderr = p.communicate()

        for line in stdout.split(b'\n'):
             m = self._mroute_regex.match(line.decode())

             if m:
                  parse_mcast_route(m.group(1),
                                    m.group(2),
                                    m.group(3),
                                    m.group(4),
                                    self._measurement4)

        p = subprocess.Popen(['ip','-6','mroute'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)

        stdout, stderr = p.communicate()

        for line in stdout.split(b'\n'):
             m = self._mroute_regex.match(line.decode())

             if m:
                  parse_mcast_route(m.group(1),
                                    m.group(2),
                                    m.group(3),
                                    m.group(4),
                                    self._measurement6)

        return (("IPRoute.Routing.Tables.IPv4",
                 self._measurement4.SerializeToString(),
                 self._measurement4.description.name,
                 self._measurement4.description.module,
                 self._measurement4.description.version),
                ("IPRoute.Routing.Tables.IPv6",
                 self._measurement6.SerializeToString(),
                 self._measurement6.description.name,
                 self._measurement6.description.module,
                 self._measurement6.description.version),)

def default_method_format(self,measurement):
    """
    Generates formatted measurement string.
    """
    def fromMeasurement(measurement):
        if measurement.type == MeasurementTable.Measurement.TYPE_SINTEGER:
            return measurement.iValue
        elif measurement.type == MeasurementTable.Measurement.TYPE_UINTEGER:
            return measurement.uValue
        elif measurement.type == MeasurementTable.Measurement.TYPE_DOUBLE:
            return measurement.dValue
        else:
            return measurement.sValue

    def build_table(name,table):
        buf = "[] %s\n" % name

        widths = [];

        for label in table.labels:
            widths.append(len(label))

        for row in table.rows:
            i = 0
            for value in row.values:
                widths[i] = max(widths[i],len(str(fromMeasurement(value))))
                i+=1

        i = 0
        for label in table.labels:
            buf += '|' + label.ljust(widths[i])
            i += 1
        buf += "|\n"

        for row in table.rows:
            i = 0
            for value in row.values:
                val = str(fromMeasurement(value))
                buf += '|' + val.ljust(widths[i])
                i += 1
            buf += "|\n"

        buf += "--\n"

        return buf

    buf= ""
    buf += build_table('routingtable',measurement.routingtable)
    buf += build_table('mcastroutingtable',measurement.mcastroutingtable)
    return buf
