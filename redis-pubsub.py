#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2012 Maykel Moya <mmoya [at] mmoya.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from __future__ import print_function

import redis
import threading
import time

class Consumer(threading.Thread):
    def __init__(self, name, topic):
        super(Consumer, self).__init__()
        self.name = name
        self.topic = topic
        self.rd = redis.Redis()

    def run(self):
        print('%s: Subscribing to topic %s' % (self.name, self.topic))
        self.rd.subscribe(self.topic)
        for item in self.rd.listen():
            if item['type'] == 'message':
                if item['data'] == 'SHUTDOWN':
                    print('%s: Shutting down' % self.name)
                    break
                print('%s: received <%s>' % (self.name, item['data']))

class Producer(threading.Thread):
    def __init__(self, name, topic):
        super(Producer, self).__init__()
        self.name = name
        self.topic = topic
        self.rd = redis.Redis()

    def run(self):
        print('%s: Publishing to topic %s' % (self.name, self.topic))
        for i in range(5):
            message = 'Hello world %d!' % i
            print('%s: sending <%s>' % (self.name, message))
            self.rd.publish(self.topic, message)
            time.sleep(1)
        print('%s: Sending %s' % (self.name, 'SHUTDOWN'))
        self.rd.publish(self.topic, 'SHUTDOWN')

def main():
    topic = 'fooTopic'

    producer = Producer('Producer', topic)
    consumers = []

    for i in range(3):
        consumer = Consumer('Consumer%d' % (i+1), topic)
        consumers.append(consumer)
        consumer.start()

    producer.start()

    producer.join()
    for consumer in consumers:
        consumer.join()

if __name__ == '__main__':
    main()
