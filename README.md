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
        - [Results](#results)
    - [Skills](#skills)
    - [Major Events](#major-events)
    - [Self-Assesment](#self-assesment)
- [Project](#project)
    - [Introduction](#introduction-1)
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
The PLP algorithm is first presented for tree networks. Then, the authors present the cutting procedure which allows an arbitrary network to be cut into a forest. Both the obtained delay and the runtime heavily depend on the cut.

In the original implementation of the PLP algorithm, the cut is selected in a very simple manner: for each node, keep only the successor that has the smaller number among the successors with a larger number than this node. This approach always constructs a valid forest. However, the resulting forest heavily depends on the indexing of the nodes (servers) within the network. Even if indexing is performed in a favorable manner, this simple cut selection often results in sub-optimal forests depending on the network topology.

The two main challenges that we are aiming to solve are as follows:

1. Understanding the relationship between the cuts (size and shape) and the resulting delay bound and the runtime.
2. Designing efficient and accurate heuristics for picking good cuts for any network size and topology.

Another challenge that we faced was the complicated nature of defining network objects in the original project. Therefore, we want to streamline the process of generating common network topologies.

## Contribution
Our project makes several significant contributions to the field of Network Calculus in FIFO networks. Firstly, we developed a solution that simplifies the generation of common network topologies, saving time and reducing the likelihood of errors. Secondly, we introduced an Analysis class that allows users to analyze the effects of cuts on delay and runtime. Additionally, we created a Stats class to compute correlation statistics based on the analysis results. These insights were then utilized to design a heuristic algorithm, implemented in the ECOWCDB class. The details of our contributions can be found in the following sections.

### Solution
Our solution can be divided into 4 main parts:

1. **Network Generation:** We simplified the generation of common network topologies such as Tandem (interleaved, source-sink, sink-tree), Mesh, and Ring (full, semi, complete-full, complete-semi) networks. Instead of defining arrival curves and paths for each flow, and service curves and shapers for each server, the users can call a single function and pass a few parameters (rate, latency, burst, number of servers, and maximum load) to generate these common network topologies. This saves time as well as avoiding typos that can happen when defining all servers and flows individually.

2. **Cut Analysis:** We created an Analysis class which is used to analyze the effects of cuts on the delay and runtime. The user can compute a delay for any cut, perform exhaustive search on all the valid cuts, and perform partial search on a random subset of valid cuts.    

    Exhaustive search provides more information; however, it is infeasible to perform exhaustive search on medium to large size networks as the number of valid cuts increases exponentially in the number of connections (edges) between servers. Partial search is therefore a valuable tool which can be used to get some ideas about the cut behavior in large networks.

    Additionally, the Analysis class provides several helpful functions used to display, save and load the obtained results. User can also pick the unit of time in which the results should be displayed, a timeout value which limits the time spent solving an individual linear program, and several verbosity options which indicate how much or how little feedback will the user receive regarding the progress/errors/details of computations.

3. **Cut Statistics:** We created a relatively smaller Stats class which is used to compute correlation statistics regarding the results obtained in the Analysis class. This class takes the output of the Analysis class as its input, and can compute the correlation for delay vs. runtime, forest-size vs. delay, and forest-size vs. runtime.

    The results obtained in this class were used in designing our heuristic algorithm which is explained next.

4. **Heuristic Algorithm:** Using all the observations from the Analysis and Stats classes, we created the ECOWCDB class. We designed a heuristic algorithm which attempts to generate the most optimal cut (forest) based on the input restrictions such as max-depth and connectedness.

    The user can use one of three defined delay functions: best-delay, delay, and quick-delay. Depending on the function called, the heuristic algorithm will generate an appropriate cut (forest) and compute the delay for the given network and cut.

    As observed in the analysis part of the project, not every network topology has the same behavior when it comes to cuts. Therefore, the generic heuristic algorithm does not always provide the best result. Nevertheless, it can be observed in the next section that the algorithm provides satisfying results for most topologies.

### Achievments
We designed four tools described in [Solution](#solution). This project, including the modifications done to the existing codebase as well as the ECOWCDB library, exceeds 2500 lines of code, out of which I would classify ~500 lines as high value code.

Our first main contribution is providing a tool for in-depth analysis of the trade-off between accuracy and tractability of Network Calculus in FIFO networks. The second main contribution is the heuristic algorithm. Results obtained with the heuristic algorithm can be seen in [Results](#results).

### Results
In this section, we will display the quality of the cuts obtained by our heuristic algorithm. We will do so by comparing the results obtained with the heuristic algorithm to the results obtained during exhaustive and partial search in the analysis part.

<style>
table {
  margin-left: auto;
  margin-right: auto;
}
</style>

| Network Topology | # Servers | Heuristic Type | Delay Ranking | Runtime Ranking |
|:-:|:-:|:-:|:-:|:-:|
| Semi Ring | 12 | Best Delay<br>Delay<br>Quick Delay | XX%<br>XX%<br>XX% | XX%<br>XX%<br>XX% |
| Full Ring | 12 | Best Delay<br>Delay<br>Quick Delay | XX%<br>XX%<br>XX% | XX%<br>XX%<br>XX% |
| Compete Semi Ring | 11 | Best Delay<br>Delay<br>Quick Delay | XX%<br>XX%<br>XX% | XX%<br>XX%<br>XX% |
| Complete Full Ring | 7 | Best Delay<br>Delay<br>Quick Delay | XX%<br>XX%<br>XX% | XX%<br>XX%<br>XX% |
| Mesh | 9 | Best Delay<br>Delay<br>Quick Delay | XX%<br>XX%<br>XX% | XX%<br>XX%<br>XX% |
| Interleaved Tandem | 12 | Best Delay<br>Delay<br>Quick Delay | XX%<br>XX%<br>XX% | XX%<br>XX%<br>XX% |
| Sink-Tree Tandem | 12 | Best Delay<br>Delay<br>Quick Delay | XX%<br>XX%<br>XX% | XX%<br>XX%<br>XX% |
| Source-Sink Tandem | 12 | Best Delay<br>Delay<br>Quick Delay | XX%<br>XX%<br>XX% | XX%<br>XX%<br>XX% |

*Based on the resutls above...*

## Skills
Skills that I have exercised throughout the project:
- **Research:**  I utilized research skills to explore the field of Network Calculus in FIFO networks. I identified existing challenges and gaps in the literature and used that knowledge to develop innovative solutions and contributions.
- **Software Engineering:** I employed software engineering skills to design, develop, and maintain a comprehensive solution. This involved writing code, organizing the project structure, and implementing various modules and classes. I followed software engineering best practices to ensure the codebase's scalability, maintainability, and robustness.
- **Graph Theory:** Graph theory played a crucial role in this project, specifically in the analysis of network topologies and cuts. I applied graph theory concepts to model and represent the network structures, connections between servers, and paths of flows. By leveraging graph theory algorithms and techniques, I was able to analyze the effects of cuts on delay and runtime.
- **Algorithm Design:** Algorithm design was a fundamental skill demonstrated in this project. I formulated and implemented algorithms for various tasks, such as generating network topologies, performing cut analysis, and designing the heuristic algorithm. I leveraged algorithmic techniques to efficiently solve complex problems and make informed decisions based on the analysis results.
- **Version Control:** I utilized version control throughout the project. Version control skills involve using tools like Git to manage changes to the codebase, track different versions of the project, and ensure proper code organization and documentation. This skill helps maintain a coherent and organized code history and facilitates collaboration and integration of contributions of future collaborators.

Skills I had to acquire for the project:
- **Understanding the Basics of Network Calculus:** In order to contribute effectively to the project, I needed to acquire a solid understanding of the fundamentals of network calculus. I immersed myself in studying the key concepts, principles, and mathematical models used in network calculus. This included comprehending the concepts of arrival curves, service curves, and their relationship in analyzing the performance of network systems. By learning about the foundations of network calculus, I was able to apply this knowledge to design and implement accurate and efficient algorithms within the project.
- **Project Setup and Extension with GitHub:** One of the skills I had to acquire was the ability to clone an existing GitHub project and set it up on my local machine. Additionally, I learned how to run the project and configure any required dependencies. Furthermore, I acquired the skills to extend and modify the existing project to incorporate my contributions effectively.
- **Advanced Knowledge of Graph Theory, Flow Networks, and Cuts:** To make significant contributions to the project, I dedicated time to expand my knowledge of graph theory, with a specific focus on flow networks and cuts. I delved deeper into the theory and algorithms related to directed graphs, understanding how flows can be modeled and represented. Moreover, I acquired the skills to cut a directed graph into a forest, which involves partitioning the graph into subgraphs without any cycles. I explored various algorithms and techniques to obtain the set of all possible forests given a directed graph. By mastering these concepts, I was able to develop efficient algorithms and implement the necessary functionalities to analyze cuts within the project.
- **Documentation:** To ensure the clarity and comprehensibility of the project, I developed skills in documentation. This involved creating detailed and organized documentation for various components, algorithms, and functionalities within the project. By honing these skills, I contributed to the overall usability and maintainability of the project, facilitating its future development and understanding.

## Major Events
Report on the major events of the project, including unexpected difficulties.

## Self-Assesment
Provide a self-assessment (where did you succeed most, where did you fail)





# Project

## Introduction
This project is an extension of the panco project [[3]](#references).

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

[3] https://github.com/Huawei-Paris-Research-Center/panco


