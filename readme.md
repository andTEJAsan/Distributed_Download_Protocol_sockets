# Computer Networks Assignment 2

1. The objective of this assignment was to implement a distributed file transfer protocol
2. We were supposed to download the file from a server which would randomly send a line from a big document, assemble that file and submit it using multiple systems.
3. To accomplish this, we used two main network topologies
   * Mesh Topology
   * Tree topology with a master

## Mesh Topology
* Each machine would have its own set of lines.
* The machines would synchronise their data after fixed periods of time, in case the entire file has been downloaded
* This approach has overhead of synchronisation, but is fault tolerant

## Tree topology
* One machine would act as the administrator and would have the final copy of the file to be submitted
* All of the machines would report to the administrator
* The overhead of synchronisation is less, but the network has a single point of failure
