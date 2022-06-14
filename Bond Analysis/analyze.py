#!/usr/bin/env python3


def present_value_to_face_value(present_value, days_to_maturity, interest_rate):
    return present_value * (1 + interest_rate) ** (days_to_maturity / 365)

def face_value_to_present_value(face_value, days_to_maturity, interest_rate):
    return face_value / (1 + interest_rate) ** (days_to_maturity / 365)


def test1():
    principal = present_value_to_face_value(100, 365, 0.02)
    pv = face_value_to_present_value(principal, 365, 0.02)
    if 100 != int(pv):
        raise Exception("doesn't make sense")

test1()

face_value = present_value_to_face_value(100, 365, 0.02)
pv = face_value_to_present_value(face_value, 305, 0.03)
print(pv)
