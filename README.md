# ECOWCDB: Efficient Computation of Worst-Case Delay-Bounds for Time-Sensitive Networks
Author: Edin Guso

Advisors: Seyed Mohammadhossein Tabatabaee, Stéphan Plassart, Jean-Yves Le Boudec

Institute: Computer Communications and Applications Laboratory 2 (LCA2), École Polytechnique Fédérale de Lausane (EPFL)

# Table of Contents
The readme consists of 2 main parts: Report and Project. Report section includes the project discussion, while the Project section is what you would expect from a regular readme.

- [ECOWCDB](#ecowcdb-efficient-computation-of-worst-case-delay-bounds-for-time-sensitive-networks)
- [Table of Contents](#table-of-contents)
- [Report](#report)
    - [Introduction](#introduction)
        - [Background](#background)
        - [Challenges](#challenges)
    - [Contribution](#contribution)
        - [Solution](#solution)
        - [Achievments](#achievments)
    - [Skills](#skills)
    - [Major Events](#major-events)
    - [Self-Assesment](#self-assesment)
- [Project](#project)
    - [Project Structure](#project-structure)
        - [File Description](#file-description)
    - [Installation](#installation)
        - [Requirements](#requirements)
        - [Dependencies](#dependencies)
    - [How to Use](#how-to-use)
    - [Extend This Project](#extend-this-project-future-work)
- [Contact](#contact)
- [References](#references)

# Report

## Introduction
The first goal of this project was to analyze the trade-off between accuracy and tractability of Network Calculus in FIFO networks. Then, using the results of this analysis, we designed efficient heuristics that find the sweet spot of this trade-off.

### Background
**Time-Sensitive Networking (TSN)** is a collection of standards and technologies that enables precise and time-critical communication in Ethernet networks. It provides mechanisms for deterministic data transmission, synchronization, and quality of service (QoS) enhancements, allowing for real-time and reliable delivery of time-sensitive data.

**Network calculus** provides mathematical tools to quantify and predict the behavior of network traffic, including delay, throughput, and packet loss. It helps in understanding the performance limits and guarantees of network systems [[1]](#references).

In the context of TSN, network calculus aids in analyzing and designing networks to meet the timing requirements of time-sensitive applications. By applying network calculus principles, network designers can determine the maximum delay and bounds on end-to-end latency for time-critical traffic flows. They can also evaluate network capacity and ensure that sufficient resources are allocated to meet the real-time demands of the applications.

There has been recent work focusing on the trade-off between accuracy and computational tractability when applying Network Calculus techniques to First-In-First-Out (FIFO) networks [[2]](#references). FIFO networks follow a simple queuing discipline where packets are served in the order of arrival.

[[2]](#references) explores how different assumptions and approaches can affect the accuracy and tractability of Network Calculus analysis in FIFO networks. It delves into various techniques proposed in the literature, which aim to overcome the challenges posed by FIFO scheduling. Additionally, the authors propose a new algorithm (PLP) based on linear programming that presents a trade-off between accuracy and tractability. Striking a balance between accurate performance bounds and manageable computational complexity becomes a crucial objective.

### Challenges
The PLP algorithm is first presented for tree networks. Then, the authors present the cutting procedure which allows an arbitrary network to be cut into a forest. Both the obtained delay and the runtime heavily depends on the cut.

In the original implementation of the PLP algorithm, the cut is selected in a very simple manner: for each node, keep only the successor that has the smaller number among the successors with a larger number than this node. This approach always constructs a valid forest. However, the resulting forest heavily depends on the indexing of the nodes (servers) within the network. Even if indexing is performed in a favorable manner, this simple cut selection often results in sub-optimal forests depending on the network topology. 

The two main challenges that we are aiming to solve are as follows:

1. Understanding the relationship betwewn the cuts (size and shape) and the resulting delay bound and the runtime.
2. Designing efficient and accurate heuristics for picking good cuts for any network size and topology.

Another challenge that we faced was the complicated nature of defining network objects in the original project. Therefore, we want to streamline the process of generating common network topologies.

## Contribution
Summary

### Solution
Our solution can be divided into 4 main sections:

1. **Network Generation:** We simplified the generation of common network topologies such as Tandem (interleaved, source-sink, sink-tree), Mesh, and Ring (full, semi, complete-full, complete-semi) networks. Instead of defining arrival curves and paths for each flow, and service curves and shapers for each server, the users can call a single function and pass a few parameters (rate, latency, burst, number of servers, and maximum load) to generate these common network topologies. This saves time as well as avoiding typos that can happen when defining all servers and flows individually.

2. **Cut Analysis:** We created an Analysis class which is used to analyze the effects of cuts on the delay and runtime. The user can compute a delay for any cut, perform exhaustive search on all the valid cuts, and perform partial search on a random subset of valid cuts.    

    Exhaustive search provides more information, however, it is infeasable to perform exhaustive search on medium to large size networks as the number of valid cuts increases exponentially in the number of connections (edges) between servers. Partial search is therefore a valuable tool which can be used to get some ideas about the cut behaviour in large networks.

    Additionally, the Analysis class provides several helpful function used to display, save and load the obtained results. User can also pick the unit of time in which the results should be displayed, a timeout value which limits the time spent solving an individual linear program, and several verbosity options which indicate how much or how little feedback will the user receive regarding the progress/errors/details of computations.

3. **Cut Statistics:** We created a relatively smaller Stats class which is used to compute correlation statistics regarding the results obtained in the Analysis class. This class takes the output of the Analysis class as its input, and can compute the correlation for delay vs. runtime, forest-size vs. delay, and forest-size vs. runtime.

    The results obtained in this class were used in designing our heuristic algorithm which is explained next.

4. **Heuristic Algorithm:** Using all the observations from the Analysis and Stats classes, we created the ECOWCDB class. We designed a heuristic algorithm which attempts to generate the most optimal cut (forest) based on the input restrictions such as max-depth and connectedness.

    The user can use one of three defined delay functions: best-delay, delay, and quick-delay. Depending on the function called, the heuristic algorithm will generate an appropriate cut (forest) and compute the delay for the given network and cut.

    As observed in the analysis part of the project, not every network topology has the same behaviour when it comes to cuts. Therefore, the generic heuristic algorithm does not always provide the best result. Nevertheless, it can be observed in the next section that the algorithm provides satisfying results for most topologies.

### Achievments
*List your achievements, give their nature, quality and quantity. Distinguish your contribution from what others did before. For example: I designed an ns model of the VP-TFMCC protocol, 2500 lines of simple code, 300 lines of high value code. Debugging took 2 weeks.*

*Numeric results & how much code is there etc.*

## Skills
What skills did you exercise

What skills did you have to acquire for the project

## Major Events
Report on the major events of the project, including unexpected difficulties.

## Self-Assesment
Provide a self-assessment (where did you succeed most, where did you fail)





# Project

## Project Structure
    .
    └- README.md
    └- installation.md
    └- LICENSE
    └- ecowcdb/
    |   └- __init__.py
    |   └- analysis.py
    |   └- ecowcdb.py
    |   └- networks.py
    |   └- options.py
    |   └- stats.py
    |   └- util/
    |   |   └- __init__.py
    |   |   └- errors.py
    |   |   └- network.py
    |   |   └- units.py
    |   |   └- validation.py
    |   └- panco/
    |       └- __init__.py
    |       └- lpSolvePath.py
    |       └- lp_solve
    |       └- ...
    └- example/
    |   └- README.md
    |   └- ...
    └- results/
    |   └- README.md
    |   └- ...
    └- temp/
        └- README.md

### File Description
...



## Installation
...

### Requirements
...

### Dependencies
...

## How to Use
...

## Extend this Project (Future Work)
...

# Contact
...


# References

[1] Boudec, J.-Y. L. and Thiran, P. (2001). Network calculus: A theory of deterministic queuing systems for the internet. Springer. 

[2] Bouillard, A. (2022). Trade-off between accuracy and Tractability of network calculus in FIFO networks. Performance Evaluation, 153, 102250. https://doi.org/10.1016/j.peva.2021.102250 












- `panco`: The tool is implemented in `Python` by [Anne Bouillard](https://ieeexplore.ieee.org/author/38526153500) at Huawei Paris Research Center. Here is the [original repository](https://github.com/Huawei-Paris-Research-Center/panco). The following is the academic reference:
    ```
    @article{BOUILLARD2022102250,
        title    = {Trade-off between accuracy and tractability of Network Calculus in FIFO networks},
        journal  = {Performance Evaluation},
        volume   = {153},
        pages    = {102250},
        year     = {2022},
        issn     = {0166-5316},
        doi      = {https://doi.org/10.1016/j.peva.2021.102250},
        url      = {https://www.sciencedirect.com/science/article/pii/S0166531621000675},
        author   = {Anne Bouillard},
        keywords = {Network Calculus, FIFO systems, Linear programming},
        abstract = {Computing accurate deterministic performance bounds is a strong need for communication technologies having stringent requirements on latency and reliability. Within new scheduling protocols such as TSN, the FIFO policy remains at work inside each class of communication. In this paper, we focus on computing deterministic performance bounds in FIFO networks in the Network Calculus framework. We propose a new algorithm based on linear programming that presents a trade-off between accuracy and tractability. This algorithm is first presented for tree networks. Next, we generalize our approach and present a linear program for computing performance bounds for arbitrary topologies, including cyclic dependencies. Finally, we provide numerical results, both of toy examples and realistic topologies, to assess the interest of our approach.}
    }
    ```