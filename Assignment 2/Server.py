import random
import string
import threading

import grpc

import scenario_pb2_grpc
import scenario_pb2
import time
from concurrent import futures
import rocksdb
import uuid
import multiprocessing
import atexit



class Scenario(scenario_pb2_grpc.ScenarioServicer):


    def Chat(self, request_iterator, context):
        mdb = rocksdb.DB("Master.db", rocksdb.Options(create_if_missing=True))
        #def masteroperations(key,value):
            #mdb = rocksdb.DB("Master.db", rocksdb.Options(create_if_missing=True))
            #for i in range(1,100):
                #key = uuid.uuid4().hex.encode('utf-8')
                #value=random.choice(string.ascii_letters).encode('utf-8')
            #mdb.put()

        def masteroperations(key,value):
            mdb.put(key, value)
            #stream(key,value)

        def stream():
                while 1:
                    key = uuid.uuid4().hex.encode('utf-8')
                    value = random.choice(string.ascii_letters).encode('utf-8')
                    masteroperations(key,value)
                    data='KEY:'+str(key)+' AND '+'DATA:'+str(value)
                    yield data
                    time.sleep(5)

        output_stream = stream()


        #for i in range(1,2):

            #data = '$$KEY:' + str(key) + ' AND ' + 'DATA:' + str(value)
            #output_stream=data
            #yield data


        def read_incoming():
            while 1:
                received = next(request_iterator)
                print('received: {}'.format(received))

        thread = threading.Thread(target=read_incoming)
        thread.daemon = True
        thread.start()

        while 1:
            yield scenario_pb2.DPong(name=next(output_stream))





if __name__ == '__main__':
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        scenario_pb2.add_ScenarioServicer_to_server(
            Scenario(), server)

        server.add_insecure_port('0.0.0.0:3000')
        server.start()
        print('listening ...')
        while 1:
            time.sleep(1)





