import paho.mqtt.client as mqtt
import os
import re

def on_connect(client, userdata, flags, rc):
    print("Connected")

def main():
    client = mqtt.Client("ssh-server")
    client.on_connect = on_connect

    hostname = os.environ["MQTT_SERVER"]

    client.connect(hostname, 1883, 60)

    client.subscribe("ssh_connections", 0)
    filename = "/var/log/auth.log"
    logfile = open(filename, "r")
    st_results = os.stat(filename)
    st_size = st_results[6]
    logfile.seek(st_size)
    while(1):
        where = logfile.tell()
        line = logfile.readline()
        print(line)
        if not line:
            logfile.seek(where)
        else:
            if(re.match(".*pam_unix.* authentication failure;.*", line)):
                client.publish("ssh_connections", "connection")
                print("Sent message")
        client.loop()

if __name__ == "__main__":
    main()

