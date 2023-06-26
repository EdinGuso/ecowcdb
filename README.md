ECOWCDB: Efficient Computation of Worst-Case Delay-Bounds for Time-Sensitive Networks
=======================
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
The first goal of this project was to analyze the trade-off between accuracy and tractability of worst-case delay-bounds in time-sensitive networks with FIFO scheduling. Then, using the results of this analysis, we designed efficient heuristics that find the sweet spot of the trade-off.

### Background
**Time-Sensitive Networking (TSN)** is a collection of standards and technologies that enables precise and time-critical communication in Ethernet networks. It provides mechanisms for deterministic data transmission, synchronization, and quality of service (QoS) enhancements, allowing for real-time and reliable delivery of time-sensitive data.

**Network calculus** provides mathematical tools to quantify and predict the behavior of network traffic, including delay, throughput, and packet loss. It helps in understanding the performance limits and guarantees of network systems [[1]](#references).

In the context of TSN, network calculus aids in analyzing and designing networks to meet the timing requirements of time-sensitive applications. By applying network calculus principles, network designers can determine the maximum delay and bounds on end-to-end latency for time-critical traffic flows. They can also evaluate network capacity and ensure that sufficient resources are allocated to meet the real-time demands of the applications.

There has been recent work focusing on the trade-off between accuracy and computational tractability when applying Network Calculus techniques to First-In-First-Out (FIFO) networks [[2]](#references). FIFO networks follow a simple queuing discipline where packets are served in the order of arrival.

[[2]](#references) explores how different assumptions and approaches can affect the accuracy and tractability of Network Calculus analysis in FIFO networks. It delves into various techniques proposed in the literature, which aim to overcome the challenges posed by FIFO scheduling. Additionally, the authors propose a new algorithm based on linear programming that presents a trade-off between accuracy and tractability. Striking a balance between accurate performance bounds and manageable computational complexity becomes a crucial objective.

### Challenges
The main challenge we are aiming to solve in this project is finding the balance between accuracy and tractability.

## Contribution
...

### Solution
...

### Achievments
...

## Skills
...

## Major Events
...

## Self-Assesment
...









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
    |       └- ...
    └- example/
    |   └-
    |   └-
    └- results/
    |   └- results.md
    └- temp/
        └- temp.md

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