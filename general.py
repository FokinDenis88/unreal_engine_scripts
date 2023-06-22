def are_list_objects_not_None(objects):
    for object in objects:
        if object is None:
            return False
    return True

def is_not_none_or_empty(list_object):
    #if isinstance(value, NoneType) or value is None:
    if list_object is None:
        return False
    else:
        return len(list_object) > 0

def is_not_none_or_empty_lists(list_objects, is_conjuction = True):
    results = []
    if is_not_none_or_empty(list_objects):
        for list_object in list_objects:
            results.append(is_not_none_or_empty(list_object))
        # conjuction = Logical AND
        if is_conjuction:
            if results.count(True) == len(list_objects):
                return True
            else:
                return False
        else:   # disjunction = Logical OR
            if results.count(True) > 0:
                return True
            else:
                return False
    return False


def is_not_none_lists(list_objects):
    if is_not_none_or_empty(list_objects):
        for object in list_objects:
            if object is None:
                return False
        return True
    else:
        return False


## Checks if all input lists has equal dimension(length)
def are_lists_equal_length(lists, has_log = False):
    if is_not_none_or_empty(lists):
        if len(lists) > 1:  # Not in single if, because len(NonType)
            first_list_len = len(lists[0])
            i = 1
            while i < len(lists):
                if len(lists[i]) != first_list_len:
                    if has_log:
                        print(are_lists_equal_length.__name__ + '() Info: lists len are not equal. ' + lists[i])
                    return False
                i += 1
    if has_log:
        print(are_lists_equal_length.__name__ + '() Info: lists length are equal')
    return True

## @return bool value, indicates if there is one or more False values
def has_false_value(list_object):
    if is_not_none_or_empty(list_object):
        for object in list_object:
            if isinstance(object, bool):
                if object == False:
                    return True
            else:
                print(has_false_value.__name__ + '() Error:values in list must be bool type')
                return None

        return False
    else:
        print(has_false_value.__name__ + '() Error:list_object must not be empty or None')
        return None

## Checks if input object type is in list of types
def is_in_types(object, types_list):
    if object is not None and is_not_none_or_empty(types_list):
        type_is_not_found = True
        i = 0
        while type_is_not_found and i < len(types_list):
            #if isinstance(object, types_list[i]) and (not issubclass(types_list[i], type(object))):
            if type(object) is types_list[i]:
                type_is_not_found = False
            i += 1
        return not type_is_not_found
    else:
        print(is_in_types.__name__ + '() Error: object and types_list must not be None or empty')
        return False

## Checks if input object type is in list of types
def is_in_subclasses(object, types_list):
    if object is not None and types_list is not None:
        type_is_not_found = True
        i = 0
        while type_is_not_found and i < len(types_list):
            if issubclass(type(object), types_list[i]):
                type_is_not_found = False
            i += 1
        return not type_is_not_found
    else:
        print(is_in_types.__name__ + '() Error: object and types_list must not be None or empty')
        return False

## Logical OR
# @param condition_list list of logical conditions
def disjunction_of_conditions(condition_list):
    if is_not_none_or_empty(condition_list):
        if condition_list.count(True) > 0:
            return True
        else:
            return False
    else:
        print(disjunction_of_conditions.__name__ + '() Error: condition_list must not be None or empty')
        return None

## Logical AND
# @param condition_list list of logical conditions
def conjunction_of_conditions(condition_list):
    if is_not_none_or_empty(condition_list):
        if condition_list.count(True) == len(condition_list):
            return True
        else:
            return False
    else:
        print(conjunction_of_conditions.__name__ + '() Error: condition_list must not be None or empty')
        return None