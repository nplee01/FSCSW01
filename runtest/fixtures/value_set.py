from collections import namedtuple

from django.core.exceptions import ValidationError
from runtest.models import Parameter, ValueSet, ValueSetMember

SetMemberTuple = namedtuple('SetMemberTuple',
"""
    value_code, value_description, sort_order,
    param_1_code, param_2_code, param_3_code,
    param_4_code, param_5_code
""")

ValueSetTuple = namedtuple('ValueSetTuple',
"""
    value_set_code, value_set_description, set_member_list
""")

def load_set_members(value_set, set_member_list):
    # Load Value Set Member
    ins=0
    upd=0
    for tp in set_member_list:
        # Get the parameters, if any
        if tp.param_1_code is None:
            p1 = None
        else:
            try:
                p1 = Parameter.objects.get(param_code=tp.param_1_code)
            except Parameter.DoesNotExist:
                raise ValidationError("Parameter 1 %s not found for set member %s" % 
                        (tp.param_1_code, tp.value_code), code='param_1')
        if tp.param_2_code is None:
            p2 = None
        else:
            try:
                p2 = Parameter.objects.get(param_code=tp.param_2_code)
            except Parameter.DoesNotExist:
                raise ValidationError("Parameter 2 %s not found for set member %s" % 
                        (tp.param_2_code, tp.value_code), code='param_2')
        if tp.param_3_code is None:
            p3 = None
        else:
            try:
                p3 = Parameter.objects.get(param_code=tp.param_3_code)
            except Parameter.DoesNotExist:
                raise ValidationError("Parameter 3 %s not found for set member %s" % 
                        (tp.param_3_code, tp.value_code), code='param_3')
        if tp.param_4_code is None:
            p4 = None
        else:
            try:
                p4 = Parameter.objects.get(param_code=tp.param_4_code)
            except Parameter.DoesNotExist:
                raise ValidationError("Parameter 4 %s not found for set member %s" % 
                        (tp.param_4_code, tp.value_code), code='param_4')
        if tp.param_5_code is None:
            p5 = None
        else:
            try:
                p5 = Parameter.objects.get(param_code=tp.param_5_code)
            except Parameter.DoesNotExist:
                raise ValidationError("Parameter 5 %s not found for set member %s" % 
                        (tp.param_5_code, tp.value_code), code='param_5')
        try:
            sm = ValueSetMember.objects.get(value_set=value_set, value_code = tp.value_code)
            sm.sort_order = tp.sort_order
            sm.param_1 = p1
            sm.param_2 = p2
            sm.param_3 = p3
            sm.param_4 = p4
            sm.param_5 = p5
            upd += 1
        except ValueSetMember.DoesNotExist:
            sm = ValueSetMember(value_set=value_set, value_code=tp.value_code, 
                    value_description=tp.value_description, sort_order=tp.sort_order,
                    param_1=p1, param_2=p2, param_3=p3, param_4=p4, param_5=p5)
            ins += 1
        sm.save()
    return (ins, upd)

def load_value_sets(value_set_list):
    # Load Value Set data
    ins = 0
    upd = 0
    # Value Set Member counts
    sm_ins = 0
    sm_upd = 0
    for tp in value_set_list:
        try:
            vs = ValueSet.objects.get(value_set_code=tp.value_set_code)
            vs.value_set_description = tp.value_set_description
            upd += 1
        except ValueSet.DoesNotExist:
            vs = ValueSet(value_set_code=tp.value_set_code, value_set_description=tp.value_set_description)
            ins += 1
        vs.save()
        # Load Value Set Members
        (ic, uc) = load_set_members(vs, tp.set_member_list)
        sm_ins += ic
        sm_upd += uc

    return (ins, upd, sm_ins, sm_upd)
