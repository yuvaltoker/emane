
#for i in {START..END..INCREMENT}
# in this case, i stands for $NODE_NO
for i in {1..10..1}
    do 
        sudo chmod a+w platform$i.xml
        # changing eth1 to eth0 in platform$i.xml
        sed -i 's/eth1/eth0/g' platform$i.xml
        # changing <param name="address"... lines to <param name="address" value="10.100.0.$i"/> in platform$i.xml
        sed -i '/<param name="address".*/c\      <param name="address" value="10.100.0.'$[i+1]'"/>/' platform$i.xml

        # changing eth1 to eth0 in eventdaemon$i.xml
        sed -i 's/eth1/eth0/g' eventdaemon$i.xml

        # changing node-$i into 10.100.0.$[i+1] in otestpoint-broker.xml
        sed -i 's/node-'$i'/10.100.0.'$[i+1]'/g' otestpoint-broker.xml

        # changing node-$i into 10.100.0.$[i+1] in otestpoint-recorder$i.xml
        sed -i 's/node-'$i'/10.100.0.'$[i+1]'/g' otestpoint-recorder$i.xml

        # changing node-$i into 10.100.0.$[i+1] in otestpointd$i.xml
        sed -i 's/node-'$i'/10.100.0.'$[i+1]'/g' otestpointd$i.xml
 done