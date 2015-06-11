# wa_worker


Worker for send whatsapp messages


wa_worker is a service that "listen" through rabbitmq queue (https://www.rabbitmq.com/)
and send a message using configured whatsapp credentials (through yowsup implementation
https://github.com/tgalal/yowsup), created because need a tool for deliver gerential
report every hour using whatsapp, premise is dispatch every request in order, service
always available and always must deliver. The product was developed with etcd and
docker ecosystem in mind, so it was deployed in coreos.


###Notice:
* The directory wa_worker/scheduler will be separated to a different project with a web client
interface because are not related with wa_worker/message_receiver at all
* Using Python 2.7
* Image base for deployment at https://registry.hub.docker.com/u/ivandavid77/centos7dockerfile/dockerfile/



###Steps for using (based on coreos deployment):


###1) Configure rabbitmq


In coreos create a service file like this:
```
File: rabbitmq@.service
[Unit]
Description=RabbitMq
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=0
Restart=always
RestartSec=60
ExecStartPre=-/usr/bin/docker kill cred_mq
ExecStartPre=-/usr/bin/docker rm cred_mq
ExecStartPre=/usr/bin/docker pull rabbitmq
ExecStart=/usr/bin/docker run --name cred_mq  -e RABBITMQ_NODENAME=cred-mq -p 8672:5672 rabbitmq
ExecStop=/usr/bin/docker stop cred_mq

[X-Fleet]
Conflicts=rabbitmq@*.service
```

* Use the official image of rabbitmq at https://registry.hub.docker.com/_/rabbitmq/


Additional we need a discovery unit that announce the location of this service to the cluster:
```
File: rabbitmq-discovery@.service
[Unit]
Description=Announce RabbitMQ
BindsTo=rabbitmq@%i.service
After=rabbitmq@%i.service

[Service]
Restart=always
RestartSec=60
ExecStart=/usr/bin/bash -c "while true; do echo '{\"host\": \"'$(hostname -i|sed 's/\ $//')'\", \"port\": \"8672\"}' | tr -d '\n' | etcdctl set /services/rabbitmq@%i --ttl 60;sleep 45;done"
ExecStop=/usr/bin/etcdctl rm /services/rabbitmq@%i

[X-Fleet]
MachineOf=rabbitmq@%i.service
```

This service will create a resouce into etcd's clusted service that "announce" our
rabbitmq@1 service, the resource created looks like
```/services/rabbitmq@1 {"host":"172.16.200.201", "port":"8672"}```


* Its critical that before start the discovery service, the shell command ```$ hostname -i```
return the correct ip address, maybe you will need edit your /etc/hosts file:
```
File: /etc/hosts
172.16.200.202   coreos-node02.crediland.mx
your-ip-addr     your-hostname
```

Check that command gives correct information:
```
$ hostname
coreos-node02.crediland.mx
$ hostname -i
172.16.200.202
```

Ok, after that install/start service:
```
$ fleetctl submit rabbitmq@.service
$ fleetctl submit rabbitmq-discovery@.service
$ fleetctl start rabbitmq@1
$ fleetctl start rabbitmq-discovery@1
```

Check if loaded
```
$ fleetctl list-units
UNIT                            MACHINE                         ACTIVE  SUB
rabbitmq-discovery@1.service    337c3825.../172.16.200.201      active  running
rabbitmq@1.service              337c3825.../172.16.200.201      active  running
```

We are ready for next step.




###2) Load wa_worker.


UPDATE: before going further clone the project and edit the file start.sh and
comment out every line inside, only leave untouched the lines:
```
echo -e ' [*] Loading requirements...\n';
pip install -r $MOUNT_POINT/wa_worker/requirements.txt
```

and

```
while true; do
    echo ' [*] running...';
    sleep 10;
done
```


Because coreos uses docker, take a look at the image base for this project in:
https://registry.hub.docker.com/u/ivandavid77/centos7dockerfile/dockerfile/,
the wa_worker service will load github project and mount it into instance created by docker:
```
File: wa_worker@.service
[Unit]
Description=WhatsAppWorker
After=docker.service
Requires=docker.service

[Service]
TimeoutStartSec=0
Restart=always
RestartSec=60
ExecStartPre=-/usr/bin/docker kill wa_worker
ExecStartPre=-/usr/bin/docker rm wa_worker
ExecStartPre=/usr/bin/docker pull ivandavid77/centos7dockerfile
ExecStartPre=-/bin/rm -fR /home/administrador/tmp/wa_worker
ExecStartPre=/usr/bin/git clone https://github.com/ivandavid77/wa_worker.git /home/administrador/tmp/wa_worker
ExecStart=/bin/sh -c '/usr/bin/docker run --name wa_worker -e SYSLOG_REMOTE=172.16.202.15:514 -e ETCD_ENDPOINT=$(hostname -i) -e ETCD_PORT=4001 -e MQ_INSTANCE=%i -e MQ_SEND_MESSAGE_QUEUE=WA_MESSAGE_QUEUE -e MQ_TASK_MANAGEMENT_QUEUE=WA_MANAGEMENT_QUEUE -e SECRET_KEY=MjAxNTA1MTMxNTE3 -e MOUNT_POINT=/mnt -v /home/administrador/tmp/wa_worker:/mnt/wa_worker ivandavid77/centos7dockerfile /mnt/wa_worker/start.sh'
ExecStop=/usr/bin/docker stop wa_worker
ExecStopPost=/bin/rm -fR /home/administrador/tmp/wa_worker

[X-Fleet]
Conflicts=wa_worker@*.service
```


Load and install/start the service, verify that its running:
```
$ fleetctl submit wa_worker@.service
$ fleetctl start wa_worker@1
$ fleetctl list-units
UNIT                            MACHINE                         ACTIVE  SUB
rabbitmq-discovery@1.service    337c3825.../172.16.200.201      active  running
rabbitmq@1.service              337c3825.../172.16.200.201      active  running
wa_worker@1.service             8e179c12.../172.16.200.202      active  running
```


Several environment vars are defined inside docker instance in ExecStart line:
```
SYSLOG_REMOTE             ::  because i don't want track were are located the instance, better specify where redirect syslog messages
ETCD_ENDPOINT             ::  wa_worker need know where is their "local" etcd server for ask the location of rabbitmq@ service inside cluster
ETCD_PORT                 ::  same but port number
MQ_INSTANCE               ::  what instance must be located in "/services/rabbitmq@*" on etcd cluster service? R = instance 1 (rabbitmq@1)
MQ_SEND_MESSAGE_QUEUE     ::  what queue will be used for listen request for sending messages?
MQ_TASK_MANAGEMENT_QUEUE  ::  what queue will be used for scheduler service (wa_worker/scheduler will be removed to another github proyect)
SECRET_KEY                ::  secret that will be used for encrypt/decrypt sensitive config information (whatsapp key/password configuration, email config for fail over, etc.)
MOUNT_POINT               ::  where was mounted the github project inside docker instance? (check the flag -v /home/administrador/tmp/wa_worker:/mnt/wa_worker ... is in "/mnt", wa_worker need know that!)
```



###3) Configure wa_worker


Login into wa_worker instance for configuration (according with output from command ```$ fleetctl list-units```)
```
$ docker exec -it wa_worker bash
[root@8f35d4e0aeef /]#
```


Next add your whatsapp credentials (you must use the yowsup library for registration: https://github.com/tgalal/yowsup/wiki/yowsup-cli-2.0#yowsup-cli-registration):
```
[root@8f35d4e0aeef /]# python $MOUNT_POINT/wa_worker/wa_worker/message_receiver/keystore.py
Usage:
            python keystore.py wa_account wa_password
            python keystore.py wa_account wa_password encrypt_key

            Example
                python keystore.py 5212288227733 ExamPlE/Wq+i/KEy912qwWqabJJ=
                (Encrypt key will be taken from environment)
                python keystore.py 5212288227733 ExamPlE/Wq+i/KEy912qwWqabJJ= MyEncrYptKey
                (Encrypt key taken from param)
```
So you must add your whatsapp credentials, if SECRET_KEY environment var was defined you
not need specify secret for encrypt this data.


* You can add more credentials for use it in case of banned whatsapp account, so you ensure that
whatsapp message will always be delivered.


Specify email for support fail over email message sending:
```
[root@8f35d4e0aeef /]# python $MOUNT_POINT/wa_worker/wa_worker/message_receiver/mail.py
Usage:
            python mail.py host user password admin
            python mail.py host user password admin encrypt_key

            Example:
                python mail.py 172.16.16.16 fallout@mydomain.com xFGt3Swq support@devops.mydomain.com
                (Encrypt key will be taken from environment)
                python mail.py 172.16.16.16 fallout@mydomain.com xFGt3Swq support@devops.mydomain.com MyEncrYptKey
                (Encrypt key taken from param)
```
This email account will be used only in case of failure delivering whatsapp message
(because account banned or requested for new password by Whats App and no more whatsapp accounts configured)




###4) Send a message


You need a rabbitmq client that use the queue defined in MQ_SEND_MESSAGE_QUEUE environment var,
the format of "body" is a json message:
```
{
    "phones": ["5212287779788", "5212287779789"],
    "mails": ["ivandavid77@gmail.com","dbarron@crediland.com.mx"],
    "msg": "some message#13with new lines#13replaced"
}
```
If message has newlines it must be replaced for "#13" string.


You can use python "send_message.py" script for sending test messages:
```
[root@8f35d4e0aeef /]# python $MOUNT_POINT/wa_worker/wa_worker/message_receiver/utilities/send_message.py -h
usage: send_message.py [-h] [--phones PHONES [PHONES ...]]
                       [--mails MAILS [MAILS ...]] --msg MSG

optional arguments:
  -h, --help            show this help message and exit
  --phones PHONES [PHONES ...]
                        phone list
  --mails MAILS [MAILS ...]
                        mail list
  --msg MSG             "message to send"
```
