#!/usr/bin/python

import optparse
import sys
import os
import time
import datetime
import json
import random

full_stacktrace = '''
[HikariPool-1 connection adder] connect:263 ERROR o.p.Driver - [owner:spring] [type:springLog] [id:] [name:] [flow:] [tracking:] Connection error: 
org.postgresql.util.PSQLException: The connection attempt failed.
	at org.postgresql.core.v3.ConnectionFactoryImpl.openConnectionImpl(ConnectionFactoryImpl.java:259)
	at org.postgresql.core.ConnectionFactory.openConnection(ConnectionFactory.java:49)
	at org.postgresql.jdbc.PgConnection.<init>(PgConnection.java:195)
	at org.postgresql.Driver.makeConnection(Driver.java:452)
	at org.postgresql.Driver.connect(Driver.java:254)
	at com.zaxxer.hikari.util.DriverDataSource.getConnection(DriverDataSource.java:136)
	at com.zaxxer.hikari.pool.PoolBase.newConnection(PoolBase.java:369)
	at com.zaxxer.hikari.pool.PoolBase.newPoolEntry(PoolBase.java:198)
	at com.zaxxer.hikari.pool.HikariPool.createPoolEntry(HikariPool.java:467)
	at com.zaxxer.hikari.pool.HikariPool.access$100(HikariPool.java:71)
	at com.zaxxer.hikari.pool.HikariPool$PoolEntryCreator.call(HikariPool.java:706)
	at com.zaxxer.hikari.pool.HikariPool$PoolEntryCreator.call(HikariPool.java:692)
	at java.base/java.util.concurrent.FutureTask.run(FutureTask.java:264)
	at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1128)
	at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:628)
	at java.base/java.lang.Thread.run(Thread.java:834)
Caused by: java.net.NoRouteToHostException: No route to host (Host unreachable)
	at java.base/java.net.PlainSocketImpl.socketConnect(Native Method)
	at java.base/java.net.AbstractPlainSocketImpl.doConnect(AbstractPlainSocketImpl.java:399)
	at java.base/java.net.AbstractPlainSocketImpl.connectToAddress(AbstractPlainSocketImpl.java:242)
	at java.base/java.net.AbstractPlainSocketImpl.connect(AbstractPlainSocketImpl.java:224)
	at java.base/java.net.SocksSocketImpl.connect(SocksSocketImpl.java:403)
	at java.base/java.net.Socket.connect(Socket.java:591)
	at org.postgresql.core.PGStream.<init>(PGStream.java:69)
	at org.postgresql.core.v3.ConnectionFactoryImpl.openConnectionImpl(ConnectionFactoryImpl.java:158)
	... 15 common frames omitted
'''

simple_message = "I am a simple short message."
EVENT_COUNTER = 0

def format_message(msg, use_json, level="DEBUG", split=False, broken_json=False):
    increase_counter()
    full_msg=""
    if use_json:
        pass
    t = datetime.datetime.now()
    full_msg="%s - [%s] #%s %s" % (t, level, str(EVENT_COUNTER), msg)
    if use_json:
        timestamp=t.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        if split:
            if broken_json:
                full_json=create_json_message(full_msg, timestamp, level)
                json_part_1 = full_json[:len(full_json)//2]
                json_part_2 = full_json[len(full_json)//2:]
                print(json_part_1)
                print(json_part_2)
            else:
                partial_id="p" + ''.join(random.choice('0123456789ABCDEF') for i in range(6))
                msg1 = full_msg[:len(full_msg)//2]
                create_json_message(msg1, timestamp, level, True, 0, partial_id)
                msg2 = full_msg[len(full_msg)//2:]
                create_json_message(msg2, timestamp, level, True, 1, partial_id)
        else:
            print(create_json_message(full_msg, timestamp, level))
    else:
        print(full_msg)

def create_json_message(msg, timestamp, level, partial=False, partial_ord=0, partial_id=None):
    json_obj={}
    json_obj["timestamp"]=timestamp
    json_obj["level"]=level
    json_obj["message"]=msg
    if partial:
        json_obj["partial_id"]=partial_id
        json_obj["partial_message"]=True
        json_obj["partial_ordinal"]=partial_ord
        json_obj["partial_last"]=partial_ord == 1
    return json.dumps(json_obj)

def increase_counter():
    global EVENT_COUNTER
    if (EVENT_COUNTER < 100000000):
        EVENT_COUNTER = EVENT_COUNTER + 1
    else:
        EVENT_COUNTER = 1
    return EVENT_COUNTER

def main():
    parser = optparse.OptionParser("usage: %prog [options]")
    parser.add_option("-j", "--json-format", dest="json_format", default=False, action="store_true", help="Use json format for logging")
    parser.add_option("-b", "--use-broken-json", dest="use_broken_json", default=False, action="store_true", help="Use json format for logging")
    parser.add_option("-s", "--sleep-interval", dest="sleep_interval", type="int", default=10, help="Sleep interval between log generation events")
    parser.add_option("-t", "--times", dest="times", type="int", default=1, help="Repeat messages number between sleeps")
    (options, args) = parser.parse_args()
    while True:
        json_format_env_val = os.getenv("JSON_FORMAT", "false")
        json_format = True if json_format_env_val == "true" else options.json_format
        sleep_interval_env_val = os.getenv("SLEEP_INTERVAL_SEC", None)
        sleep_interval = int(sleep_interval_env_val) if sleep_interval_env_val else options.sleep_interval
        times_env_val = os.getenv("REPEAT_MESSAGES_BETWEEN_SLEEPS", None)
        times = int(times_env_val) if times_env_val else options.times
        broken_json_env_val = os.getenv("BROKEN_JSON", "false")
        broken_json = True if broken_json_env_val == "true" else options.use_broken_json

        env_settings = {}
        env_settings['JSON_FORMAT']=json_format_env_val
        env_settings['SLEEP_INTERVAL_SEC']=sleep_interval_env_val
        env_settings['REPEAT_MESSAGES_BETWEEN_SLEEPS']=times_env_val
        format_message("Env settings: %s" % str(env_settings), json_format)
        
        for x in range(times):
            format_message(simple_message, json_format)
            format_message(full_stacktrace, json_format, "ERROR")
            format_message(simple_message, json_format)
            format_message(full_stacktrace, json_format, "ERROR", True, broken_json)
            format_message(simple_message, json_format)
        time.sleep(sleep_interval)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
