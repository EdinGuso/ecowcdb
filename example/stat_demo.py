# Local Imports - ecowcdb libraries
from ecowcdb.stats import Stats



def main():
    filename = 'exhaustive_full_ring_12'
    stats = Stats('results/', filename)
    
    flow_of_interest = 0

    stats.delay_runtime_correlation(flow_of_interest)
    stats.forestsize_delay_correlation(flow_of_interest)
    stats.forestsize_runtime_correlation(flow_of_interest)


if __name__ == '__main__':
    main()
