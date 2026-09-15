import numpy as np
import inspect
from unittest.mock import patch
import io
import traceback


# simple data used for testing


# Moderate reaction enthalpies (endo + exo magnitudes)
Temp_list_1 = [12]

# Typical hydrogen bond and van der Waals interaction energies
Temp_list_2 = [2.8, 4.3, 6.1, 7.4, 3.6]

# Common bond dissociation energies (scaled kcal/mol versions)
Temp_list_3 = [86, 99, 72, 113, 58, 76]


Temp_array_1 = np.array(Temp_list_1)
Temp_array_2 = np.array(Temp_list_2)
Temp_array_3 = np.array(Temp_list_3)


peak_lists = {
    "Peak_List_1": [3390, 3200, 2990, 2970, 2910, 1650, 1620, 1530, 1350],
    "Peak_List_2": [2961, 2857, 1806, 1748, 1445, 1406],
    "Peak_List_3": [3546, 2963, 2935, 2853, 2260, 1754, 1440, 1250, 1200, 1180, 1020],
    "Peak_List_4": [3416, 2964, 2928, 1717, 1622, 1448, 1439, 1427, 1410, 1400, 1342, 1265, 1000],
    "Peak_List_5": [3538, 3523, 3520, 3477, 3469, 3093, 2968, 1752, 1648, 1493, 1441, 1174, 1162],
    "Peak_List_6": [3504, 3401, 2981, 2972, 1743, 1619, 1480, 1459, 1436, 1186, 1032],
    "Peak_List_7": [3491, 3490, 3488, 3448, 1750, 1746, 1595, 1558, 1516, 1508, 1439, 1200],
    "Peak_List_8": [3486, 3462, 3458, 1623, 1557, 1476, 1464, 1260, 1180, 1005],
    "Peak_List_9": [3522, 3391, 3130, 2912, 1459, 1442, 1394, 1275, 1105],
    "Peak_List_10": [3449, 3444, 3403, 3138, 1637, 1495, 1434, 1135, 1060],
    "Peak_List_11": [3458, 3454, 3440, 3434, 2967, 2959],
    "Peak_List_12": [3521, 3516, 3485, 3171, 3153, 3133, 1574, 1509, 1417],
    "Peak_List_13": [3452, 3436, 3402, 3023, 1631, 1629, 1600, 1300, 1250, 1100, 1020, 985],
    "Peak_List_14": [3505, 3494, 3083, 1520, 1518, 1510, 1350, 1200, 1050],
    "Peak_List_15": [3473, 3442, 3438, 3412, 2963, 1484, 1471, 1443, 1200, 1110],
    "Peak_List_16": [2950, 2845, 1740, 1370, 1270, 1170, 1040]
    
}

# Combine the lists into a list of lists
list_of_peak_lists = [peak_lists[key] for key in peak_lists.keys()]


Atomic_mass_dict_testing = {'H': 1.00782503223, 'He': 4.00260325413, 'Li': 7.0160034366, 'Be': 9.012183065, 'B': 11.00930536, 'C': 12.0, 'N': 14.00307400443, 'O': 15.99491461957, 
            'F': 18.99840316273, 'Ne': 19.9924401762, 'Na': 22.989769282, 'Mg': 23.985041697, 'Al': 26.98153853, 'Si': 27.97692653465, 'P': 30.97376199842, 'S': 31.9720711744, 
            'Cl': 34.968852682, 'Ar': 39.9623831237, 'K': 38.9637064864, 'Ca': 39.962590863, 'Sc': 44.95590828, 'Ti': 47.94794198, 'V': 50.94395704, 'Cr': 51.94050623, 
            'Mn': 54.93804391, 'Fe': 55.93493633, 'Co': 58.93319429, 'Ni': 57.93534241, 'Cu': 62.92959772, 'Zn': 63.92914201, 'Ga': 68.9255735, 'Ge': 73.921177761, 
            'As': 74.92159457, 'Se': 79.9165218, 'Br': 78.9183376, 'Kr': 83.9114977282, 'Rb': 84.9117897379, 'Sr': 87.9056125, 'Y': 88.9058403, 'Zr': 89.9046977, 'Nb': 92.906373, 
            'Mo': 97.90540482, 'Tc': 96.9063667, 'Ru': 101.9043441, 'Rh': 102.905498, 'Pd': 105.9034804, 'Ag': 106.9050916, 'Cd': 113.90336509, 'In': 114.903878776, 'Sn': 119.90220163, 
            'Sb': 120.903812, 'Te': 129.906222748, 'I': 126.9044719, 'Xe': 131.9041550856, 'Cs': 132.905451961, 'Ba': 137.905247, 'La': 138.9063563, 'Ce': 139.9054431, 'Pr': 140.9076576, 
            'Nd': 141.907729, 'Pm': 144.9127559, 'Sm': 151.9197397, 'Eu': 152.921238, 'Gd': 157.9241123, 'Tb': 158.9253547, 'Dy': 163.9291819, 'Ho': 164.9303288, 'Er': 165.9302995, 
            'Tm': 168.9342179, 'Yb': 173.9388664, 'Lu': 174.9407752, 'Hf': 179.946557, 'Ta': 180.9479958, 'W': 183.95093092, 'Re': 186.9557501, 'Os': 191.961477, 'Ir': 192.9629216, 
            'Pt': 194.9647917, 'Au': 196.96656879, 'Hg': 201.9706434, 'Tl': 204.9744278, 'Pb': 207.9766525, 'Bi': 208.9803991, 'Po': 208.9824308, 'At': 209.9871479, 'Rn': 222.0175782, 
            'Fr': 223.019736, 'Ra': 226.0254103, 'Ac': 227.0277523, 'Th': 232.0380558, 'Pa': 231.0358842, 'U': 238.0507884, 'Np': 237.0481736, 'Pu': 244.0642053, 'Am': 243.0613813, 
            'Cm': 247.0703541, 'Bk': 247.0703073, 'Cf': 251.0795886, 'Es': 252.08298, 'Fm': 257.0951061, 'Md': 258.0984315, 'No': 259.10103, 'Lr': 262.10961, 'Rf': 267.12179, 'Db': 268.12567, 
            'Sg': 271.13393, 'Bh': 272.13826, 'Hs': 270.13429, 'Mt': 276.15159, 'Ds': 281.16451, 'Rg': 280.16514, 'Cn': 285.17712, 'Nh': 284.17873, 'Fl': 289.19042, 'Mc': 288.19274, 
            'Lv': 293.20449, 'Ts': 292.20746, 'Og': 294.21392}

# error handling wrapper that catches errors and stops the print out of complex error messages, this is used to make the feedback more user friendly for students who may not be used to seeing error messages in python, it also prevents the feedback from being lost in a long error message.
def error_handling_wrapper(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error in function '{func.__name__}'")
            print(e)
            #traceback.print_exc()
    return wrapper

# checks if a function exists
def function_exists(func_name):
    # Check global scope
    if func_name in globals() and callable(globals()[func_name]):
        return True
    
    # Check local scope
    frame = inspect.currentframe().f_back
    if func_name in frame.f_locals and callable(frame.f_locals[func_name]):
        return True
    
    return False

# performs an initial check for task 1 for the student
@error_handling_wrapper
def quick_check(Calculate_in_kjmol):
    c=4.184
    x=1500
    if function_exists('Calculate_in_kjmol'):
        try:
            assert Calculate_in_kjmol([x]) == [x*c]
            print("This converts a value correctly")
        except AssertionError:
            try:
                np.testing.assert_array_equal(Calculate_in_kjmol([x]), np.array([x*c]))
                print("This converts a value correctly")
            except AssertionError:
                raise AssertionError("your function does not perform the correct conversion")
    else:
        print(f"'{Calculate_in_kjmol.__name__}' does not exist")
    pass

# used in task 1 to do the marking of the conversion function, it checks if the function converts a list of values correctly and outputs either a list or an array, it also provides feedback on if the conversion is correct or not and if the output is in the correct format.
@error_handling_wrapper
def check_conversion(Calculate_in_kjmol,energy_list,marks):
    if function_exists('Calculate_in_kjmol'):
        new_list = Calculate_in_kjmol(energy_list)
        c=4.184   
        values = []
        for i in energy_list:
            values.append(i*c)
    
        values_np = np.array(energy_list)*c

  
    
        if isinstance(new_list, np.ndarray):
            if np.array_equal(new_list,values_np):
                print("This converts the list correctly")
                marks.append(1)
                marks.append(1)
            else:
               print("This does not seem to convert the list correctly")
    
        elif isinstance(new_list, list):
            if new_list == values:
                print("This converts the list correctly")
                marks.append(1)
                marks.append(1)
            else:
                print("This does not seem to convert the list correctly")
        else:
            print(new_list)
            print(type(new_list))
            print("The function does not output either a list or an array")
    else:
        print(f"'{Calculate_in_kjmol.__name__}' does not exist")
    pass


# checks if the nump import command was included only works if import command is included in function but used below for robustness
def uses_numpy(func):
    source = inspect.getsource(func)
    return 'numpy' in source or 'np' in source

# this is an example of checking that a particular package is used in a function
@error_handling_wrapper
def check_numpy(func, energy_list, marks):
    # Save the original np.array method
    old_np_array = np.array
    
    # Create a mock method to replace np.array
    def mock_array(*args, **kwargs):
        raise NameError("Function uses NumPy")
    
    # Replace np.array with the mock method
    np.array = mock_array

    if function_exists('func'):
    
        try:
            func(energy_list)
        except NameError as e:
            print("Well done using numpy is a sensible way to perform this task. For long lists it will be significantly faster than using a for loop")
            marks.append(1)
        else:
            if uses_numpy(func):
                print("Well done using numpy is a sensible way to perform this task. For long lists it will be significantly faster than using a for loop")
                marks.append(1)
            else:
                print("It looks like you didn't use numpy for this task, while this is not essential, numpy is a much faster way to convert lists and arrays of data")
        finally:
            # Restore the original np.array method
            np.array = old_np_array

    else:
        print(f"'{func.__name__}' does not exist")
    pass


@error_handling_wrapper
def mass_check(mass_search,element):
    if function_exists('mass_search'):
        mass = mass_search(element)
        if mass == Atomic_mass_dict_testing[element]:
            print("this retrieves the correct mass")
    else:
        print(f"'{mass_search.__name__}' does not exist")
    pass


@error_handling_wrapper
def mass_check_output(mass_search,element,marks):
    if function_exists('mass_search'):
        mass = mass_search(element)
        if mass == Atomic_mass_dict_testing[element]:
            print("this retrieves the correct mass")
            marks.append(1)
    else:
        print(f"'{mass_search.__name__}' does not exist")
    pass

   

# not in use now but checks if a function prints the correct value
# @error_handling_wrapper
# def mass_check_output(mass_search,element,marks): 

#     if function_exists('mass_search'):

#         with patch('__main__.print') as mock_print:
#             mass_search(element)
#         mock_print.assert_called_once_with("{:.3f}".format(Atomic_mass_dict_testing[element]))
#         print("this retrieves the correct mass in the correct format")
#         marks.append(1)
#     else:
#         print(f"'{mass_search.__name__}' does not exist")
#     pass

# this checks if a function raises a key error when an incorrect element symbol is used.
@error_handling_wrapper
def mass_Key_error(mass_search,element,marks):

    if function_exists('mass_search'):
        try:
            mass_search(element)
        except KeyError:
            print("Successfully raises a Key Error for an incorrect element symbol")
            marks.append(1)
    else:
        print(f"'{mass_search.__name__}' does not exist")
    pass

# handy function that can be used to check if a variable exists in either the local or global scope, this can be used to check if students have defined variables with the correct name
def variable_exists(var_name):
    # Check global scope
    if var_name in globals():
        return True
    
    # Check local scope
    frame = inspect.currentframe().f_back
    if var_name in frame.f_locals:
        return True
    
    return False



# task 4
@error_handling_wrapper        
def peak_check(Ester_lists):
    answer = [peak_lists["Peak_List_6"],peak_lists["Peak_List_16"]]
    answer2 = [peak_lists["Peak_List_16"],peak_lists["Peak_List_6"]]
    

    if isinstance(Ester_lists, list):
        if len(Ester_lists) == 2:
            print("Ester_Lists is the correct length")
            if Ester_lists == answer:
                print("Ester_lists is correct")
            elif Ester_lists == answer2:
                print("You have the correct spectra but oddly they are not in the order of the original list, double check how you looped over the lists of lists")                  
            else:
                print("Ester_lists is incorrect, only two spectra contain all three spectral features")
        else:
            print("Ester_lists is the incorrect length")

    else:
        print("Ester_lists is not a list")

    pass  

# task 4
@error_handling_wrapper        
def peak_check_marks(Ester_lists,marks):
    answer = [peak_lists["Peak_List_6"],peak_lists["Peak_List_16"]]
    answer2 = [peak_lists["Peak_List_16"],peak_lists["Peak_List_6"]]

    if isinstance(Ester_lists, list):
        if len(Ester_lists) == 2:
            marks.append(1)
            if Ester_lists == answer:
                marks.append(1)
                marks.append(1)
                marks.append(1)
                marks.append(1)
            elif Ester_lists == answer2:
                marks.append(1)
                marks.append(1)
                marks.append(1)
            else:
                pass
        else:
            pass
    else:
        pass

    pass 

        
        