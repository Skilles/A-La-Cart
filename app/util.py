
def calculate_calories(weight: int, height: int, age: int, sex: bool) -> int:
    if sex == 'M':
        bmr = (weight / 2.20462262) + 6.25 * (height * 2.54) - (5 * age) + 5
    elif sex == 'F':
        bmr = (weight / 2.20462262) + 6.25 * (height * 2.54) - (5 * age) - 161
    else:
        raise Exception(f"Unknown sex: {sex}")
    return int(bmr)



