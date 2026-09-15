import numpy as np


def check_task4(aspirin_peaks, painkillers):
    if isinstance(aspirin_peaks, list):
        if aspirin_peaks == [
            2966,
            2924,
            2854,
            2701,
            1753,
            1692,
            1606,
            1583,
            1375,
            1188,
        ]:
            out = "You have successfully defined the list of aspirin peaks: {}".format(
                aspirin_peaks
            )
        elif aspirin_peaks == [
            "2966",
            "2924",
            "2854",
            "2701",
            "1753",
            "1692",
            "1606",
            "1583",
            "1375",
            "1188",
        ]:
            out = " Ooops, the aspirin list does not look correct - I think you have provided a list of strings rather than numbers"
        else:
            out = "I dont think you have defined the aspirin list correctly, have you listed the values in the same order?"
    else:
        out = "You dont seem to have defined a list for the aspirin peaks"

    if isinstance(painkillers, list):
        if painkillers == ["aspirin", "paracetamol", "ibuprofen"]:
            out += (
                "\n You have successfully defined the list of painkillers: {}".format(
                    painkillers
                )
            )
        elif len(painkillers) == 1:
            out += "\n Ooops, the painkiller list does not look correct - I dont think you have correctly used '' in the definition"
        else:
            out += "\n I dont think you have defined the painkiller list correctly, have you listed the values in the same order?"
    else:
        out += "\n You dont seem to have defined a list for the painkillers"

    return out


def check_task7(K_to_C, C_to_K):
    assert C_to_K(100) == 373.15
    assert K_to_C(373.15) == 100
    return "Your functions passed the tests!"


def check_task10(week1, week2, lastday):
    if week1 == [10.69685, 19.35502, 28.47649, 39.96519, 10.90958, 14.90519, 23.65269]:
        out = "You have correctly defined week 1: {}".format(week1)
    elif len(week1) == 7:
        out = "You have sliced 7 days but not started on the correct day - assume the week starts on Sunday; {}".format(
            week1
        )
    else:
        out = "You dont seem to have sliced the correct number of days, remember start is included, stop is not:{}".format(
            week1
        )

    if week2 == [45.88064, 28.58437, 43.88897, 55.52792, 53.05492, 28.10893, 18.25083]:
        out += "\nYou have correctly defined week 2: {}".format(week2)
    elif len(week2) == 7:
        out += "\nYou have sliced 7 days but not started on the correct day - assume the week starts on Sunday; {}".format(
            week2
        )
    else:
        out += "\nYou dont seem to have sliced the correct number of days, remember start is included, stop is not:{}".format(
            week2
        )

    if lastday == 27.27495:
        out += "\nYou have correctly identified the last day data as {}. Did you use the -1 index syntax?".format(
            lastday
        )
    else:
        out += "\nYou do not seem to have correctly defined the last day {}. Remember you can index from the end".format(
            lastday
        )
    return out

def check_task13(tanx):
    x = np.linspace(-10, 10, 100)
    if np.array_equal(np.round(tanx, 10), np.round(np.tan(x), 10)):
        return "You have correctly calculated tanx"
    else:
        return "tanx does not apera to be correct"
