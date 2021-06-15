#
# Copyright (c) 2014-2016,2019 - Adjacent Link LLC, Bridgewater,
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

from .probebase import ProbeBase
from .physicallayer_pb2 import Measurement_emane_physicallayer_counters_general
from .physicallayer_pb2 import Measurement_emane_physicallayer_tables_events
from .physicallayer_pb2 import Measurement_emane_physicallayer_tables_status
from .probeprinter import output

class PhysicalLayer(ProbeBase):
    def __init__(self):
        ProbeBase.__init__(self,
                           'PhysicalLayer',
                           'emanephy',
                           'otestpoint.emane',
                           'probe-emane-physicallayer.xsd')

    def build(self,probe):
        c = globals()[probe]
        p = c()
        return p


    def loadTable(self,member,table,data):

        if member == 'receivepowertable':

            for e in data:
                entry = table.entries.add()
                entry.nem=e[0][0]
                entry.frequency=e[1][0]
                entry.receive_power_dBm=e[2][0]
                entry.last_packet_time=e[3][0]

            return True

        elif member == 'eventreceptiontable':

            for e in data:
                entry = table.entries.add()
                entry.event=e[0][0]
                entry.count=e[1][0]

            return True


        elif member == 'pathlosseventinfotable':

            for e in data:
                entry = table.entries.add()
                entry.nem=e[0][0]
                entry.pathloss_dB=e[1][0]
                entry.reverse_pathloss_dB=e[2][0]

            return True

        return False

def default_method_format(self,measurement):
    return output(measurement)
