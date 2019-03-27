# Overview
The goal of this project is to provide a quick demo of spark.
The idea is to set-up an environment where we can go through a development cycle end to end.

This project requires you to use Vagrant.
Please install this first and then do `vagrant up` in order to set-up the environment.
Once the environment is set-up you can log into the box by doing `vagrant ssh`.

The environment does not come with any python dependencies.
In order to install them, you should run `sudo pip install -r requirements.txt` (yes it's a sudo pip)
To run your tests, you will need to install the test dependencies by running `sudo pip install -r test-requirements.txt`.

To check your code, you can run the tests by doing
```commandline
PYTHONPATH=/usr/lib/spark/python:$PYTHONPATH py.test demo_spark_job/tests/test_parse_logs.py
```

To get the job to run, start by generating some mock data by doing
```commandline
hadoop fs -rm -r -f -skipTrash /users/vagrant/events/2019/03/27/12/LOGS;
/usr/lib/spark/bin/spark-submit --master local[1] \
demo_spark_job/lib/generate_data.py \
--o_dummy_logs /users/vagrant/events/2019/03/27/12/LOGS \
--event_count 100
```

and then run the job to parse the logs
```commandline
hadoop fs -rm -r -f -skipTrash /users/vagrant/events/2019/03/27/12/TAGS;
/usr/lib/spark/bin/spark-submit --master local[1] \
demo_spark_job/lib/parse_logs.py \
--i_tag_logs /users/vagrant/events/2019/03/27/12/LOGS \
--o_results /users/vagrant/events/2019/03/27/12/TAGS
```

Note: In order to shuttle code to your vm you can:
* Use git clone/pull directly
* Use `scp` to copy code to the box.  To do this, start by getting the config
```commandline
vagrant ssh-config
Host default
  HostName 127.0.0.1
  User vagrant
  Port 2222
  UserKnownHostsFile /dev/null
  StrictHostKeyChecking no
  PasswordAuthentication no
  IdentityFile /path/to/private_key
  IdentitiesOnly yes
  LogLevel FATAL
  ForwardAgent yes
```
You can then use this config with scp as follows
```commandline
scp \
-o Port=2222 \
-o UserKnownHostsFile=/dev/null \
-o StrictHostKeyChecking=no \
-o PasswordAuthentication=no \
-o IdentityFile=/path/to/private_key \
-o IdentitiesOnly=yes \
-r ../demo_spark_job vagrant@127.0.0.1:/home/vagrant/demo_spark_job
```
