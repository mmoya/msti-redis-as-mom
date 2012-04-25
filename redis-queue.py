#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import redis
import threading
import time

class Consumer(threading.Thread):
    def __init__(self, name, queue):
        super(Consumer, self).__init__()
        self.name = name
        self.queue = queue
        self.rd = redis.Redis()

    def run(self):
        print('%s: Listening to queue %s' % (self.name, self.queue))
        while True:
            item = self.rd.blpop(self.queue)
            data = item[1]
            if data == 'SHUTDOWN':
                print('%s: Shutting down and resending' % self.name)
                self.rd.rpush(self.queue, data)
                break
            print('%s: received <%s>' % (self.name, data))

class Producer(threading.Thread):
    def __init__(self, name, queue):
        super(Producer, self).__init__()
        self.name = name
        self.queue = queue
        self.rd = redis.Redis()
        self.rd.delete(queue)

    def run(self):
        print('%s: Pushing to queue %s' % (self.name, self.queue))
        for i in range(5):
            message = 'Hello world %d!' % i
            print('%s: sending <%s>' % (self.name, message))
            self.rd.rpush(self.queue, message)
            time.sleep(1)
        print('%s: Sending %s' % (self.name, 'SHUTDOWN'))
        self.rd.rpush(self.queue, 'SHUTDOWN')

def main():
    queue = 'fooQueue'

    producer = Producer('Producer', queue)
    consumers = []

    for i in range(3):
        consumer = Consumer('Consumer%d' % (i+1), queue)
        consumers.append(consumer)
        consumer.start()

    producer.start()

    producer.join()
    for consumer in consumers:
        consumer.join()

if __name__ == '__main__':
    main()
