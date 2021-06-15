#
# Copyright (c) 2014-2016 - Adjacent Link LLC, Bridgewater, New Jersey
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
from otestpoint.interface.measurementtable_pb2 import MeasurementTable

def fromMeasurement(measurement):
    if measurement.type == MeasurementTable.Measurement.TYPE_SINTEGER:
        return measurement.iValue
    elif measurement.type == MeasurementTable.Measurement.TYPE_UINTEGER:
        return measurement.uValue
    elif measurement.type == MeasurementTable.Measurement.TYPE_DOUBLE:
        return measurement.dValue
    else:
        return measurement.sValue

def output(msg):
    buf = ""

    for item in sorted(msg.DESCRIPTOR.fields_by_name.keys()):
        if item != 'description':
            messageType = type(getattr(msg,item)).__name__

            if messageType == 'MeasurementTable':
                buf += '[] '+ item + "\n"

                table = getattr(msg,item)

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

            elif messageType == 'PhysicalLayerReceivePowerTable':
                buf += '[] '+ item + "\n"

                table = getattr(msg,item)

                buf += "| %-5s | %-12s | %-12s | %-16s |\n" % ('NEM',
                                                               'Frequency Hz',
                                                               'Rx Power dBm',
                                                               'Last Packet Time')


                for entry in table.entries:
                    buf += "| %-5s | %-12s | %-12s | %-16s |\n" % (entry.nem,
                                                                   entry.frequency,
                                                                   entry.receive_power_dBm,
                                                                   entry.last_packet_time)
                buf += "--\n"

            elif messageType == 'EventReceptionTable':
                buf += '[] '+ item + "\n"

                table = getattr(msg,item)

                buf += "| %-5s | %-15s |\n" % ('Event',
                                               'Count')


                for entry in table.entries:
                    buf += "| %-5s | %-15s |\n" % (entry.event,
                                                   entry.count)

                buf += "--\n"

            elif messageType == 'PathlossEventTable':
                buf += '[] '+ item + "\n"

                table = getattr(msg,item)

                buf += "| %-5s | %-11s | %-18s |\n" % ('NEM',
                                                       'Pathloss dB',
                                                       'Reverse Pathoss dB')


                for entry in table.entries:
                    buf += "| %-5s | %-11s | %-18s |\n" % (entry.nem,
                                                           entry.pathloss_dB,
                                                           entry.reverse_pathloss_dB)

                buf += "--\n"

            else:
                counter = getattr(msg,item)
                buf += item + " = " + str(counter) + "\n"

    return buf
