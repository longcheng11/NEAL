# NEAL
test and source code for Network-Aware Locality Scheduling

## Workload Generation

The TPC-H benchmark can be downloaded from http://www.tpc.org/tpch/. The following two commonads are used to generate the two used tables, each of which includes 600 data partitions.

> ./dbgen -vf -s 600 -T c <br/>
 ./dbgen -vf -s 600 -T o

The `GenKey.java` is used to extracted the keys from the generated tables. The `VariousNode.java`, `VariousZipf.java` and `VariousSkew.java` ace used to generated the workloads used in the paper.  The `code.jar` is the extracted jar file to generate the used workloads. Some example commands are shown as below.
>java -cp code.jar VariousNode 200  <br/>
java -cp code.jar VariousSkew 40  <br/>
java -cp code.jar VariousZipf 1

## Simulations using Matlab 

The `main.m` is the script to run the simulation experiments.

The `Join.m` contains the implementations of the Hash and Min scheduling approaches listed in the Table 3 in the paper. 

The `NEAL.m` in the folder func/ is the WOA-based implementation of NEAL. 

The `mininet.m` is used to output the communication and bandwidth matrices for the Mininet experiments.

Detailed explanations of the implementation have been given in the code step by step. Just make sure that the workloads generated in the first step located at the right path.

The folder result/ includes the randomly generated bandwidth for each experiments.  


## Emulations using Mininet
We make SDN networks based on Mininet emulator. Please install and setup miniet emulator from http://mininet.org/.

There are three source code files in this emulation. 
 - setup-mininet-opt.py
- setup-mininet-eql.py
- setup-dataprocess.py

>`setup-mininet-opt.py` is for emulating the networking based on coFlow algorithm.   <br/>
`setup-mininet-eql.py` does not use coFlow algorithm, which is used as a benchmark networking.   <br/>
`setup-dataprocess.py` is used for final data processing.  <br/>
Plesae refer to our paper for more detail about the parameters of the experiment setup. 

Please follow the steps below for running the emulation code. 
1. Change the file names of workload and bandwidth in setup-mininet-opt.py. For example, 
    workload_file = './settings/1/NEAL_V'
    bandwidth_file = './settings/1/NEAL_B'
NEAL_V is the file for setting the communication load between hosts.
NEAL_B is the file for setting the communication bandwidth between hosts.
2. Change the file name in setup-mininet-eql.py. For example, 
	bw_file = './settings/bw/bw_1_1_1'
bw_1_1_1 is the bandwidth of physical link between hosts and switch. 
3. Change the networking topology in the setupNetwork() function according to your own requirement. In this function, we use iperf3 to setup the commmunication load and bandwidth. 
4. The communication statistics results are written in txt files. We use independent txt file for each flow. For example, file "h1-s2.txt" has the result of flow from host2 to host1. 
5. Run setup-dataprocess.py to produce the final result. Please change the destination file name for outputting the result. For example, 
    result_file = "./results/1/Result_NEAL_C"
Result_NEAL_C is the name of the result file. 

If you have any questions, please email to long.cheng (at) ucd (dot)ie

