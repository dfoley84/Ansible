import csv
import sys
import os
from datetime import datetime, timedelta


# Getting System Time Delta
Todays_Date = datetime.now()
String_Date = str(Todays_Date)
Today_object = datetime.strptime(String_Date,'%Y-%m-%d %H:%M:%S.%f')

# Get Input from jenkins
vCenter_user = str(sys.argv[1])
vCenter_pass = str(sys.argv[2])
BlueCat_user = str(sys.argv[3])
BlueCat_pass = str(sys.argv[4])

# Open CSV File and Add Contents to a PythonList
with open("/usr2/dfoley/jenkins/workspace/vSphere/Virtual_Machine_Decommissioning/VirtualMachineInfo.csv", 'r') as f:
    reader = csv.reader(f, delimiter=',')
    data = list(reader)
f.close()


#os.remove("virtualmachines.csv")
# Creating Backup of the CSV File in Event of Run Time Error
newname = 'VirtualMachineInfo' + String_Date + '.csv'
os.rename('/usr2/dfoley/jenkins/workspace/vSphere/Virtual_Machine_Decommissioning/VirtualMachineInfo.csv', newname)

# Loop over the Data List if Above Zero
if len(data) > 0:
    for i in data:
        Old_Date = i[5] # Getting the Index Item which holds the Date Variable

        # Using timedelta to Compare System Date agaisnt Date within the Python List
        datetime_object = datetime.strptime(Old_Date, '%Y-%m-%d %H:%M:%S.%f')
        result = abs(Today_object - datetime_object).days

        # Using an IF Statement if the Date within List is Above Seven Days Run the Ansible Script to Remove the Machine
        if result > 6:
            re  = (i)
            s = ",".join(re)

            print("Deleting The Following Machine: {}".format(i[2])) # Print out Which Machine is going to be deleted

            # Call the Ansible Program to Delete the Virtual Machine
            os.system('ansible-playbook Delete_virtual_Machine.yaml --extra-vars "user={} pass={} vcenter_hostname={} cluster_name={} VM_Name={}"'.format(vCenter_user, vCenter_pass, i[0], i[1], i[2]))

            print("Finished Removing: {}".format(i[2])) #Print out Once Job is Finished
            print("Running Python Script to Remove A Record")

            os.system('python RemoveARecord.py {} {}'.format(BlueCat_user, BlueCat_pass, i[3], i[4])) # Run the Python Script to Remove DNS Record From BlueCat
            print("Python Job Finished:")
            #os.system('python email.py {}'.format(i[3]))

             #Keeping Track of Items thaat are Removed from vSphere.
            with open("RemovedMachines.csv", "a") as f:
                f.write("The Following Machine: {} Was Removed From vCenter: {} On the Following Date: {}\n".format(i[2],i[0],Todays_Date))
            f.close()

        else:
                #Any Items that are not Above the Seven Day mark Write back to New CSV File.
            re = (i)
                #Remvoving the Brackets and '' from Items within List & Write to CSV File
            s = ",".join(re)
            print("Vitual Machine: {} Is Not Above the Seven Day Marker\n".format(i[2]))
            with open("/usr2/dfoley/jenkins/workspace/vSphere/Virtual_Machine_Decommissioning/VirtualMachineInfo.csv", "a") as fp:
                fp.write("{}\n".format(s))
            fp.close()

else:
    print("No Infomation was Processed: Data List is Null")
