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
from .ieee80211abg_pb2 import Measurement_emane_ieee80211abg_counters_general
from .ieee80211abg_pb2 import Measurement_emane_ieee80211abg_counters_queue0
from .ieee80211abg_pb2 import Measurement_emane_ieee80211abg_counters_queue1
from .ieee80211abg_pb2 import Measurement_emane_ieee80211abg_counters_queue2
from .ieee80211abg_pb2 import Measurement_emane_ieee80211abg_counters_queue3
from .ieee80211abg_pb2 import Measurement_emane_ieee80211abg_tables_events
from .ieee80211abg_pb2 import Measurement_emane_ieee80211abg_tables_neighbor
from .ieee80211abg_pb2 import Measurement_emane_ieee80211abg_tables_status_queue0
from .ieee80211abg_pb2 import Measurement_emane_ieee80211abg_tables_status_queue1
from .ieee80211abg_pb2 import Measurement_emane_ieee80211abg_tables_status_queue2
from .ieee80211abg_pb2 import Measurement_emane_ieee80211abg_tables_status_queue3
from .probeprinter import output

class IEEE80211abg(ProbeBase):
    def __init__(self):
        ProbeBase.__init__(self,
                           'IEEE80211abg',
                           'ieee80211abgmaclayer',
                           'otestpoint.emane',
                           'probe-emane-ieee80211abg.xsd')

    def build(self,probe):
        c = globals()[probe]
        p = c()
        return p

def default_method_format(self,measurement):
    return output(measurement)
