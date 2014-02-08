import string 
import itertools, operator
import types

def extract_number_list(input_string):
    ret = {"ERROR":"", "RESULT":[], "NONE_INPUT":False}
    # Check that the string provided is of the correct format. Example: [1,2,5-10,34,6-7]
    if input_string is None:
        ret["NONE_INPUT"] = True
        ret["ERROR"] += "Received no input!\n"
    else:
        number_list = input_string.replace(" ","")
        if number_list[0] is not '[' or number_list[-1] is not ']':
            ret["ERROR"] += "Incorrect format provided for the list of test cases. Got \'%s\'.\nValid formatting example: [1,2,5-10,34,6-7]<br>" %number_list
        else:
            bad_chars = []
            for c in number_list:
                if c is not '[' and c is not ']' and c is not ',' and c is not '-' and c not in string.digits:
                    bad_chars.append(c)
            for c in bad_chars:
                number_list = number_list.replace(c, "")
        
            # parse string into objects
            try:
                number_list = number_list.replace("[", "").replace("]","").split(",")
                for number in number_list:
                    if len(number) == 0:
                        continue
                    if "-" in number:
                        ret["RESULT"] += range(int(number.split("-")[0]), int(number.split("-")[-1]) + 1)
                    else:
                        ret["RESULT"].append(int(number))
            except Exception as e:
                ret["ERROR"] += "Incorrect format provided for the list of test cases. Got \'%s\'.\nValid formatting example: [1,2,5-10,34,6-7]<br>" %number_list
        
    return ret 

def pack_tc_list(tc_list): # Takes in a list of numbers and combines entries to this format: [10-13,45-45,50-90,100-100]
    if not len(tc_list):
        return "None"

    ranges = []
    for k, g in itertools.groupby(enumerate(sorted(tc_list)), lambda (i,x):i-x):
        ranges.append(map(operator.itemgetter(1), g))

    text = "["
    for i in ranges:
        text += "%d-%d," %(i[0],i[-1])
    text = text[:-1] + "]"
    return text

def get_cgi_multiple_select(form, name):
    value = form.getvalue(name)
    if isinstance(value, types.StringType):
        value = [value]
    elif isinstance(value, types.NoneType):
        value = []
    return value

