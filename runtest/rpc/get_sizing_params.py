from django.http import JsonResponse
from django.forms.models import model_to_dict

from runtest.models import ValueSet, ValueSetMember
from .return_record import ReturnRecord

def get_sizing_params(request, sizing_code):
    # handles get only 
    ret = ReturnRecord()
    data = []
    fld =['param_label', 'default_value', 'min_value', 'max_value', 'mult_by']
    try:
        vs = ValueSet.objects.get(value_set_code='SIZING-METHODS')
        # Get sizing Method
        sm = ValueSetMember.objects.get(value_set=vs, value_code=sizing_code)
        if sm.param_1:
            data.append(model_to_dict(sm.param_1, fields=fld)) 
        if sm.param_2:
            data.append(model_to_dict(sm.param_2, fields=fld)) 
        if sm.param_3:
            data.append(model_to_dict(sm.param_3, fields=fld)) 
        # Prepare data to be returned
        ret.set_data(data)
    # No exceptions expected if fixtures has been loaded
    except ValueSet.DoesNotExist as err:
        ret.set_error(str(err))
    except ValueSetMember.DoesNotExist as err:
        ret.set_error(str(err))
    except AttributeError as err:
        # In case some params not set
        ret.set_error(str(err))
    # Return json
    return JsonResponse(ret.to_dict())

