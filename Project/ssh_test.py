import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("<RPI IP>", username="pi", password="PASSWORD")

# sftp = ssh.open_sftp()
# sftp.get("/home/pi/sensor_data.json", "./sensor_data.json")
# sftp.close()
ssh.close()
