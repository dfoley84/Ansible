from datetime import datetime
import sys

currentDT = datetime.now()

vcenter = str(sys.argv[1])
cluster = str(sys.argv[2])
hostname = str(sys.argv[3])
fqdn = str(sys.argv[4])
ip = str(sys.argv[5])

f = open("virtualmachines.csv", "a")
f.write("{},{},{},{}\n".format(vcenter, cluster, hostname, fqdn, ip, currentDT))
f.close()
