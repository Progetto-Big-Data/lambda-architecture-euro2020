import threading
import time
import kafka
import os




class StoreHDFS(threading.Thread):
    def __init__(self, hdfs_filepath, filename, local_path, sleep_time=5):
        threading.Thread.__init__(self)
        self.hdfs_path = hdfs_filepath
        self.sleep_time = sleep_time
        self.filename = filename
        self.local_path = local_path

    def run(self):
        time.sleep(self.sleep_time)
        filepath = os.path.join(self.hdfs_path, self.filename)
        hdfs_command = f'hdfs dfs -put {self.local_path} {filepath}'
        os.system(hdfs_command)
        print('file saved to HDFS')
            


topic_name = 'final_fixtures'

consumer = kafka.KafkaConsumer(
    topic_name,
    bootstrap_servers=['localhost:9092']
)


local_path = 'kafka'
filename = 'new_fixtures.csv'
local_path = os.path.join(local_path, filename)
hdfs_path = 'historical_euro_fixtures'

hdfs_write_daemon = StoreHDFS(hdfs_path, filename, local_path)
hdfs_write_daemon.start()

with open(local_path, 'a') as file:
    for msg in consumer:
        fixture = msg.value
        fixture = bytes.decode(fixture)
        file.write(fixture.strip('!"') + '\n')
        file.flush()
        print(f'read data: {fixture}')

    consumer.close()

hdfs_write_daemon.join()