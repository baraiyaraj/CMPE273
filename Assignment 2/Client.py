import threading

import grpc
import time

import scenario_pb2_grpc, scenario_pb2
import rocksdb
import atexit


def run():
    rdb=rocksdb.DB("Slave.db", rocksdb.Options(create_if_missing=True))
    channel = grpc.insecure_channel('0.0.0.0:3000')
    stub = scenario_pb2_grpc.ScenarioStub(channel)
    print('client connected')

    def stream():
        while 1:
            yield scenario_pb2.DPong(name=input(''))

    input_stream = stub.Chat(stream())

    def read_incoming():
        while 1:
            data=format(next(input_stream).name)
            keyindex = data.find("b'")
            andindex = data.find("AND DATA:b'")
            key = data[keyindex + 2:andindex - 2]
            value = data[andindex + 11:-1]
            rdb.put(key.encode('utf-8'), value.encode('utf-8'))
            print('received: ',data)





    thread = threading.Thread(target=read_incoming)
    thread.daemon = True
    thread.start()

    while 1:
        time.sleep(1)

if __name__ == '__main__':
        print('client starting ...')
        run()
