# Benchmarking Corda blockchain framework

Corda is an open source blockchain project, designed for business from the start. Read more about Corda [here](https://github.com/corda/corda). This repository has instructions and some resources to benchmark Corda-3.3 blockchain framework. 

On a high level view, JMeter is used to drive traffic at a node (PartyA) in the form of flow start requests. Each flow issues an IOU from PartyA to PartyC with a value of 1. To find number of transactions are completed per second, assuming all the requests from JMeter reach the server at the same time, the measurements are taken from the time when the RPC request reaches the node to the completion of the flow at the node which indicates the transaction is committed. Since all the measurements are taken in the corda node itself (not at the JMeter), the latency of the requests shouldn't affect the throughput.

## Prerequisites

```shell
mkdir ~/workspace && cd ~/workspace

# Fetch the Corda framework (modified for instrumentation)
git clone https://github.com/Nihhaar/corda.git

# Fetch the example cordapp used in the benchmarking
git clone https://github.com/Nihhaar/cordapp-example.git

# Fetch JMeter
wget https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-5.0.zip

# Fetch the custom sampler for jmeter for firing rpc requests
git clone https://github.com/Nihhaar/jmeter-rpc.git

# Fetch log parser(python3 & numpy) and jmeter-tests from this repo
git clone https://github.com/Nihhaar/Corda-Blockchain-Benchmark.git
```



## Building & Setup

```shell
cd corda
# Build corda and install it to the local maven repo at ~/.m2
./gradlew install
cd ..

cd cordapp-example
# Build cordapp along with corda to deploy nodes
# Configure IP addresses in cordapp-example/kotlin-source/build.gradle
# Generated nodes can be found in cordapp-example/kotlin-source/build/nodes/
./gradlew deployNodes
cd ..

cd jmeter-rpc
# Build jmeter sampler
# Output can be found at build/libs/jmeter-rpc-1.0-SNAPSHOT.jar
./gradlew build
cd ..

# Copy runtime libraries required for JMeter sampler
mkdir libs
cd libs
cp ~/.m2/repository/net/corda/corda/3.3-corda-local/corda-3.3-corda-local.jar .
unzip corda-3.3-corda-local.jar
rm corda-3.3-corda-local.jar
rm groovy-all-1.8.9.jar
cd ..

# Unzip JMeter
unzip apache-jmeter-5.0.zip -d apache-jmeter-5.0
vim apache-jmeter-5.0/bin/user.properties
# Edit user.classpath variable to libs directory created above. For eg,
# user.classpath=/home/nihhaar/workspace/libs/
```



## Running

```shell
cd cordapp-example/kotlin-source/build/nodes/
# Start the nodes
cd Notary
$TERMINAL -e sh -c 'java -jar corda.jar;zsh' &> /dev/null &
cd ..
cd PartyA
$TERMINAL -e sh -c 'java -jar corda.jar;zsh' &> /dev/null &
cd ..
cd PartyB
$TERMINAL -e sh -c 'java -jar corda.jar;zsh' &> /dev/null &
cd ..
cd PartyC
$TERMINAL -e sh -c 'java -jar corda.jar;zsh' &> /dev/null &
cd ..
cd ../../../../
```



## Benchmark

```shell
# Replace i with number of concurrent users. For eg, write_rpc_5.jmx test is for firing 5 rpc requests per sec.
# You can always create your own test in the JMeter using the sampler above.
i=1
./apache-jmeter-5.0/bin/jmeter -n -t Corda-Blockchain-Benchmark/jmeter-tests/write_rpc_$i.jmx

# This will create Initiator.log in your home directory by PartyA
# Log parser to parse the log
# python3 Corda-Blockchain-Benchmark/parse_log_initiator.py <num_iterations>
# For 1 run:
python3 Corda-Blockchain-Benchmark/parse_log_initiator.py 1
# If we run the jmeter-test for 100 iterations:
python3 Corda-Blockchain-Benchmark/parse_log_initiator.py 100
# Remove Initiator.log for each test (not for each iteration)
rm ~/Initiator.log
```



## Results

```spreadsheet
# For write_rpc_1.jmx, if run for 100 iterations, parser reported (for me):

Transactions per second
-----------------------
1 requests, 100 iterations
Total time: 0.4866 sec
Latency: 0.4866 sec
Throughput: 2.0552 tps
```
