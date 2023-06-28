# Local Imports - ecowcdb libraries
from ecowcdb.stats import Stats



def main():
    filename = 'exhaustive_full_ring_12'
    stats = Stats('results/', filename)
    
    flow_of_interest = 0

    print('Correlation results:')

    stats.delay_runtime_correlation(flow_of_interest)
    stats.forestsize_delay_correlation(flow_of_interest)
    stats.forestsize_runtime_correlation(flow_of_interest)

    max_depth = 5

    print('\nHeuristic algorithm performance:')

    stats.best_forest_ranking(flow_of_interest)
    stats.forest_ranking(flow_of_interest, max_depth)
    stats.quick_forest_ranking(flow_of_interest, max_depth)


if __name__ == '__main__':
    main()
