import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Trust the host and add it
ssh.connect("172.20.10.3", username="pi", password="PeterParker!!00")

# sftp = ssh.open_sftp()
# sftp.get("/home/pi/sensor_data.json", "./sensor_data.json")
# sftp.close()
ssh.close()
