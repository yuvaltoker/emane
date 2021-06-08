import zmq
import uuid
import otestpoint.interface.probereport_pb2 as probereport_pb2

context = zmq.Context()

subscriber = context.socket(zmq.SUB)

subscriber.connect('tcp://10.101.0.2:8882')

# subscriber.setsockopt_string(zmq.SUBSCRIBE,'EMANE.VirtualTransport.Counters.General')
subscriber.setsockopt_string(zmq.SUBSCRIBE,'EMANE.VirtualTransport.Tables.Status')

while True:
    msgs = subscriber.recv_multipart()

    report = probereport_pb2.ProbeReport()

    report.ParseFromString(msgs[1])
    
    print('probe name:',msgs[0])
    print('timestamp:',report.timestamp)
    print('tag:',report.tag)
    print('index:',report.index)
    print('uuid:',uuid.UUID(bytes=report.uuid))
    print('data name:',report.data.name)
    print('data module:',report.data.module)
    print('data version:',report.data.version)
    print('data length:',len(report.data.blob))
    print('type:',report.type)
    print('')