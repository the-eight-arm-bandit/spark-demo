Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"

  # Add some more memory to the vm
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
  end

  # Enable agent forwarding so that we can get the git repo
  config.ssh.forward_agent = true

  config.vm.provision "shell" do |s|
     s.name = "Do away with the ip v6 madness"
     s.privileged = true

     $script = <<-SCRIPT
        echo "net.ipv6.conf.all.disable_ipv6 = 1" > /etc/sysctl.d/disable-ipv6.conf
        echo "net.ipv6.conf.default.disable_ipv6 = 1" >> /etc/sysctl.d/disable-ipv6.conf
        sysctl -p /etc/sysctl.d/disable-ipv6.conf
     SCRIPT

     s.inline = $script
  end

  config.vm.provision "shell" do |s|
     s.name = "Get the packages we need from yum"
     s.privileged = true

     $script = <<-SCRIPT
        # Update the yum config
        cat /etc/yum.conf | grep -vG "^#" | grep -vG "^$" >> /tmp/yum.conf && \
          echo "ip_resolve=4" >> /tmp/yum.conf && \
          echo "timeout=180" >> /tmp/yum.conf && \
          mv /tmp/yum.conf /etc/yum.conf

        # Get the tools that we need
        yum -y upgrade && \
          yum group install -y 'Development Tools' && \
          sudo yum install -y wget
     SCRIPT

     s.inline = $script
  end

  config.vm.provision "shell" do |s|
     s.name = "Install Java"
     s.privileged = true

     $script = <<-SCRIPT
       # Get the package
       yum install -y java

       # Set up the environment variable
       echo "# Java config" > /etc/profile.d/java-env.sh && \
         echo "export JAVA_HOME=/usr/lib/jvm/jre" >> /etc/profile.d/java-env.sh && \
         source /etc/profile.d/java-env.sh
     SCRIPT

     s.inline = $script

  end

  config.vm.provision "shell" do |s|
     s.name = "Install Scala"
     s.privileged = true

     $script = <<-SCRIPT
       # Download the archive and put it in the right place
       cd /tmp && \
         wget -q http://downloads.typesafe.com/scala/2.11.7/scala-2.11.7.tgz && \
         tar -xvf scala-2.11.7.tgz &> /dev/null && \
         mv scala-2.11.7 /usr/lib && \
         ln -s /usr/lib/scala-2.11.7 /usr/lib/scala && \
         rm -f /tmp/scala-2.11.7.tgz

       # Set up the environment variable
       echo "# Scala config" > /etc/profile.d/scala-env.sh && \
         echo 'export PATH=$PATH:/usr/lib/scala/bin' >> /etc/profile.d/scala-env.sh && \
         source /etc/profile.d/scala-env.sh
     SCRIPT

     s.inline = $script
  end

  config.vm.provision "shell" do |s|
     s.name = "Install HDFS.  For more information, see https://www.edureka.co/blog/install-hadoop-single-node-hadoop-cluster"
     s.privileged = true

     $script = <<-SCRIPT
       # Download the archive and put it in the right place
       cd /tmp && \
         wget -q https://archive.apache.org/dist/hadoop/core/hadoop-2.7.3/hadoop-2.7.3.tar.gz && \
         tar -xvf hadoop-2.7.3.tar.gz &> /dev/null && \
         mv /tmp/hadoop-2.7.3 /usr/lib/hadoop-2.7.3

       # Tell hadoop where java lives
       sed -i '/^export JAVA_HOME=.*/c\ export JAVA_HOME=/usr/lib/jvm/jre' /usr/lib/hadoop-2.7.3/etc/hadoop/hadoop-env.sh

       # Have the log be in the temp directory
       sed -i "/^#export HADOOP_LOG_DIR=.*/c\ export HADOOP_LOG_DIR=/tmp" /usr/lib/hadoop-2.7.3/etc/hadoop/hadoop-env.sh

       # Create the core-site.xml file
       echo '<?xml version="1.0" encoding="UTF-8"?>' > /usr/lib/hadoop-2.7.3/etc/hadoop/core-site.xml && \
         echo '<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>' >> /usr/lib/hadoop-2.7.3/etc/hadoop/core-site.xml && \
         echo "<configuration>" >> /usr/lib/hadoop-2.7.3/etc/hadoop/core-site.xml && \
         echo "<property>" >> /usr/lib/hadoop-2.7.3/etc/hadoop/core-site.xml && \
         echo "<name>fs.default.name</name>" >> /usr/lib/hadoop-2.7.3/etc/hadoop/core-site.xml && \
         echo "<value>hdfs://localhost:9000</value>" >> /usr/lib/hadoop-2.7.3/etc/hadoop/core-site.xml && \
         echo "</property>" >> /usr/lib/hadoop-2.7.3/etc/hadoop/core-site.xml && \
         echo "</configuration>" >> /usr/lib/hadoop-2.7.3/etc/hadoop/core-site.xml

       # Create the hdfs-site.xml file
       echo '<?xml version="1.0" encoding="UTF-8"?>' > /usr/lib/hadoop-2.7.3/etc/hadoop/hdfs-site.xml && \
         echo '<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>' >> /usr/lib/hadoop-2.7.3/etc/hadoop/hdfs-site.xml && \
         echo "<configuration>" >> /usr/lib/hadoop-2.7.3/etc/hadoop/hdfs-site.xml && \
         echo "<property>" >> /usr/lib/hadoop-2.7.3/etc/hadoop/hdfs-site.xml && \
         echo "<name>dfs.replication</name>" >> /usr/lib/hadoop-2.7.3/etc/hadoop/hdfs-site.xml && \
         echo "<value>1</value>" >> /usr/lib/hadoop-2.7.3/etc/hadoop/hdfs-site.xml && \
         echo "</property>" >> /usr/lib/hadoop-2.7.3/etc/hadoop/hdfs-site.xml && \
         echo "<property>" >> /usr/lib/hadoop-2.7.3/etc/hadoop/hdfs-site.xml && \
         echo "<name>dfs.permission</name>" >> /usr/lib/hadoop-2.7.3/etc/hadoop/hdfs-site.xml && \
         echo "<value>false</value>" >> /usr/lib/hadoop-2.7.3/etc/hadoop/hdfs-site.xml && \
         echo "</property>" >> /usr/lib/hadoop-2.7.3/etc/hadoop/hdfs-site.xml && \
         echo "</configuration>" >> /usr/lib/hadoop-2.7.3/etc/hadoop/hdfs-site.xml

       # Create a symlink to make things more generic
       ln -s /usr/lib/hadoop-2.7.3 /usr/lib/hadoop

       # Update the environment variables
       echo "# Hadoop config" > /etc/profile.d/hadoop-env.sh && \
         echo "export HADOOP_HOME=/usr/lib/hadoop" >> /etc/profile.d/hadoop-env.sh && \
         echo "export HADOOP_CONF_DIR=/usr/lib/hadoop/etc/hadoop" >> /etc/profile.d/hadoop-env.sh && \
         echo "export HADOOP_COMMON_HOME=/usr/lib/hadoop" >> /etc/profile.d/hadoop-env.sh && \
         echo "export HADOOP_HDFS_HOME=/usr/lib/hadoop" >> /etc/profile.d/hadoop-env.sh && \
         echo 'export PATH=$PATH:/usr/lib/hadoop/bin' >> /etc/profile.d/hadoop-env.sh && \
         source /etc/profile.d/hadoop-env.sh

       # Start the service
       hadoop namenode -format && \
         /usr/lib/hadoop/sbin/hadoop-daemon.sh start namenode && \
         /usr/lib/hadoop/sbin/hadoop-daemon.sh start datanode

       # Create a location for the vagrant user
       hadoop fs -mkdir -p /users/vagrant && \
         hadoop fs -chown -R vagrant:vagrant /users/vagrant
     SCRIPT

     s.inline = $script
  end

  config.vm.provision "shell" do |s|
     s.name = "Install spark"
     s.privileged = true

     $script = <<-SCRIPT
       # Download the archive and put it in the right place
       cd /tmp && \
         wget -q http://mirrors.advancedhosters.com/apache/spark/spark-2.3.3/spark-2.3.3-bin-hadoop2.7.tgz && \
         tar -xvf spark-2.3.3-bin-hadoop2.7.tgz &> /dev/null && \
         sudo mv spark-2.3.3-bin-hadoop2.7 /usr/lib && \
         rm -f /tmp/spark-2.3.3-bin-hadoop2.7.tgz

      # Disable hive for spark-sql
      echo "# Disable hive for spark-sql" > /usr/lib/spark-2.3.3-bin-hadoop2.7/conf/spark-defaults.conf && \
        echo "spark.sql.catalogImplementation=in-memory" >> /usr/lib/spark-2.3.3-bin-hadoop2.7/conf/spark-defaults.conf

      # Create a symlink to make things more generic
      ln -s /usr/lib/spark-2.3.3-bin-hadoop2.7 /usr/lib/spark

      # Setup the environment variables
      echo "# Spark config" > /etc/profile.d/spark-env.sh && \
        echo "export SPARK_HOME=/usr/lib/spark" >> /etc/profile.d/spark-env.sh && \
        echo 'export PATH=$PATH:$SPARK_HOME/bin' >> /etc/profile.d/spark-env.sh && \
        source /etc/profile.d/spark-env.sh
     SCRIPT

     s.inline = $script
  end

  config.vm.provision "shell" do |s|
     s.name = "Install pip"
     s.privileged = true

     $script = <<-SCRIPT
       yum install -y epel-release &&
       yum install -y python-pip && \
       pip install --upgrade pip && \
       yum install -y python-devel
     SCRIPT

     s.inline = $script
  end

end