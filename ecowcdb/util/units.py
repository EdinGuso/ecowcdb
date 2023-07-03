"""
 File containing the unit related utility functions. Streamlines displaying results in different units.
"""

# Standard Library Imports
from typing import List, Tuple

# Local Imports - ecowcdb libraries
from ecowcdb.options import DisplayUnit



def __unit_str(unit: DisplayUnit) -> str:
    """
     Convert a DisplayUnit to a string. This is used to display units in human readable form.
     This is a helper function for generate_header.
     
     Args:
     	 unit (DisplayUnit, required): The unit to convert.
     
     Raises:
         ValueError: If the unit is not recognised.
     
     Returns: 
     	 str: The string representation of the unit.
    """
    match unit:
        case DisplayUnit.MicroSecond:
            return 'µs'
        case DisplayUnit.MilliSecond:
            return 'ms'
        case DisplayUnit.Second:
            return 's'
        case DisplayUnit.Minute:
            return 'min'
        case DisplayUnit.Hour:
            return 'h'
        case _:
            raise ValueError(f'Unhandled unit type: {unit}')

def __unit_factor(unit: DisplayUnit) -> int | float:
    """
     Converts a DisplayUnit to a scaling factor. This is used to correctly scale the time value.
     This is a helper function for convert_result_units.
     
     Args:
     	 unit (DisplayUnit, required): The unit to convert.
    
     Raises:
         ValueError: If the unit is not recognised.
     
     Returns: 
     	 int | float: The scaling factor for the unit.
    """
    match unit:
        case DisplayUnit.MicroSecond:
            return 10**6
        case DisplayUnit.MilliSecond:
            return 10**3
        case DisplayUnit.Second:
            return 1
        case DisplayUnit.Minute:
            return 1/60
        case DisplayUnit.Hour:
            return 1/3600
        case _:
            raise ValueError(f'Unhandled unit type: {unit}')

def generate_header(delay_unit: DisplayUnit, runtime_unit: DisplayUnit) -> List[Tuple[str, str, str, str]]:
    """
     Generates the header for the results table.
     
     Args:
     	 delay_unit (DisplayUnit, required): Delay unit to use for delay.
     	 runtime_unit (DisplayUnit, required): Runtime unit to use for runtime.
     
     Returns: 
     	 List[Tuple[str, str, str]]: List of tuples where each tuple consists of 4 strings.
    """
    return [('# of Edges', 'Edges Kept', f'Delay ({__unit_str(delay_unit)})', f'Elapsed Time ({__unit_str(runtime_unit)})')]

def convert_result_units(results: List[Tuple[List[Tuple[int, int]], float, float]],
                         delay_unit: DisplayUnit, runtime_unit: DisplayUnit
                         ) -> List[Tuple[str, str, str, str]]:
    """
     Scales the results by the correct factor according to the display unit.
     Then, turns all the results into strings.
    
     Args:
         results (List[Tuple[List[Tuple[int, int]], float, float]], required): List of tuples which holds the delay
         and runtime values for each forest.
         delay_unit (DisplayUnit, required): Delay unit to use for delay.
     	 runtime_unit (DisplayUnit, required): Runtime unit to use for runtime.

     Returns: 
     	 List[Tuple[str, str, str, str]]: List of tuples where each tuple consists of 4 strings. First string is number
         of edges, second string is the list of edges, third one is the delay, and the last one is the runtime.
    """
    table = []
    for entry in results:
        table.append((len(entry[0]).__str__(),
                      entry[0].__str__(),
                      (entry[1] * __unit_factor(delay_unit)).__str__(),
                      (entry[2] * __unit_factor(runtime_unit)).__str__()))
    return table
