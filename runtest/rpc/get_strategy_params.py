from django.http import JsonResponse

from runtest.models import ValueSet, ValueSetMember
from .return_record import ReturnRecord

def get_strategy_params(request, strategy_code):
    # handles get only 
    ret = ReturnRecord()
    data = {}
    try:
        vs = ValueSet.objects.get(value_set_code='STRATEGIES')
        # Get strategy
        st = ValueSetMember.objects.get(value_set=vs, value_code=strategy_code)
        data['indicator_count'] = st.param_1.default_value
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

