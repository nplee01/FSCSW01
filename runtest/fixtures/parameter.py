from collections import namedtuple

from runtest.models import Parameter

ParameterTuple = namedtuple('ParameterTuple',
"""
    param_code, param_label, param_description,
    default_value, min_value, max_value,
    step_by, mult_by
""")

def load_parameters(param_list):
    ins = 0
    upd = 0
    for tp in param_list:
        try:
            pm = Parameter.objects.get(param_code=tp.param_code)
            pm.param_label = tp.param_label
            pm.param_description = tp.param_description
            pm.default_value = tp.default_value
            pm.min_value = tp.min_value
            pm.max_value = tp.max_value
            pm.step_by = tp.step_by
            pm.mult_by = tp.mult_by
            upd += 1
        except Parameter.DoesNotExist:
            pm = Parameter(param_code=tp.param_code, param_label=tp.param_label,
                    param_description=tp.param_description, default_value=tp.default_value,
                    min_value=tp.min_value, max_value=tp.max_value, 
                    step_by=tp.step_by, mult_by=tp.mult_by)
            ins += 1
        pm.save()

    return (ins, upd)

