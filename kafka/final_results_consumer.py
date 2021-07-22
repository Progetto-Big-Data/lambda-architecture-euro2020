import threading
import time
import kafka
import os




class StoreHDFS(threading.Thread):
    def __init__(self, hdfs_filepath, filename, sleep_time=5):
        threading.Thread.__init__(self)
        self.hdfs_path = hdfs_filepath
        self.sleep_time = sleep_time
        self.filename = filename

    def run(self):
        time.sleep(self.sleep_time)
        filepath = os.path.join(self.hdfs_path, self.filename)
        hdfs_command = f'hdfs dfs -put test.csv {filepath}'
        os.system(hdfs_command)
        print('file saved to HDFS')
            


topic_name = 'final_fixtures'

consumer = kafka.KafkaConsumer(
    topic_name,
    bootstrap_servers=['localhost:9092']
)

hdfs_path = '/user/antonio/historical_euro_fixtures'

hdfs_write_daemon = StoreHDFS(hdfs_path, 'test.csv')
hdfs_write_daemon.start()

with open('test.csv', 'a') as file:
    for msg in consumer:
        fixture = msg.value
        fixture = bytes.decode(fixture)
        file.write(fixture.strip('!"') + '\n')
        file.flush()
        print(f'read data: {fixture}')

    consumer.close()

hdfs_write_daemon.join()