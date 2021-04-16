from django.http import JsonResponse
from django.forms.models import model_to_dict

from runtest.models import ValueSet, ValueSetMember
from .return_record import ReturnRecord

def get_indicator_params(request, indicator_code):
    # handles get only 
    ret = ReturnRecord()
    data = []
    # Fields from param we want to return
    fld =['param_label', 'default_value', 'min_value', 'max_value', 'mult_by']
    try:
        # Get Indicator
        vs = ValueSet.objects.get(value_set_code='INDICATORS')
        ic = ValueSetMember.objects.get(value_set=vs, value_code=indicator_code)
        # Prepare data to be returned
        if ic.param_1:
            data.append(model_to_dict(ic.param_1, fields=fld))
        if ic.param_2:
            data.append(model_to_dict(ic.param_2, fields=fld))
        if ic.param_3:
            data.append(model_to_dict(ic.param_3, fields=fld))
        ret.set_data(data)
    # No exceptions expected if fixtures has been loaded
    except ValueSet.DoesNotExist as err:
        ret.set_error(str(err))
    except ValueSetMember.DoesNotExist as err:
        ret.set_error(str(err))
    # Return json
    return JsonResponse(ret.to_dict())

