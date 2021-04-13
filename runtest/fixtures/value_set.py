from collections import namedtuple

from runtest.models import ValueSet, ValueSetMember

SetMemberTuple = namedtuple('SetMemberTuple',
"""
    value_code, value_description, sort_order,
    param_1, param_2, param_3
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
        try:
            sm = ValueSetMember.objects.get(value_set=value_set, value_code = tp.value_code)
            sm.sort_order = tp.sort_order
            sm.param_1 = tp.param_1
            sm.param_2 = tp.param_2
            sm.param_3 = tp.param_3
            upd += 1
        except ValueSetMember.DoesNotExist:
            sm = ValueSetMember(value_set=value_set, value_code=tp.value_code, 
                    value_description=tp.value_description, sort_order=tp.sort_order,
                    param_1=tp.param_1, param_2=tp.param_2, param_3=tp.param_3)
            ins += 1
        sm.save()
    return (ins, upd)

def load_value_set(value_set_list):
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
