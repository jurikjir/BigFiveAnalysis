"""
Dataset conversion maps
"""

maps = {
    "race": {
        1: "Mixed",
        2: "Arctic",
        3: "European",
        4: "Indian",
        5: "Middle East",
        6: "North Arfican",
        7: "Australian",
        8: "American",
        9: "North East Asian",
        10: "Pacific",
        11: "South East Asian",
        12: "West African",
        13: "Other"
    },

    "engnat": {
        0: "Missed",
        1: "Yes",
        2: "No"
    },

    "gender": {
        0: "Missed",
        1: "Male",
        2: "Female",
        3: "Other"
    },

    "hand": {
        0: "Missed",
        1: "Right",
        2: "Left",
        3: "Both"
    },
    
    "source": {
        1: "Web",
        2: "Google",
        3: "Facebook",
        4: "Edu",
        5: "Other"
    },
}

ans_map = {
    "E1": "strfwd",
    "E2": "reversed",
    "E3": "strfwd",
    "E4": "reversed",
    "E5": "strfwd",
    "E6": "reversed",
    "E7": "strfwd",
    "E8": "reversed",
    "E9": "strfwd",
    "E10": "reversed",
    "N1": "strfwd",
    "N2": "reversed",
    "N3": "strfwd",
    "N4": "reversed",
    "N5": "strfwd",
    "N6": "strfwd",
    "N7": "strfwd",
    "N8": "strfwd",
    "N9": "strfwd",
    "N10": "strfwd",
    "A1": "reversed",
    "A2": "strfwd",
    "A3": "reversed",
    "A4": "strfwd",
    "A5": "reversed",
    "A6": "strfwd",
    "A7": "reversed",
    "A8": "strfwd",
    "A9": "strfwd",
    "A10": "strfwd",
    "C1": "strfwd",
    "C2": "reversed",
    "C3": "strfwd",
    "C4": "reversed",
    "C5": "strfwd",
    "C6": "reversed",
    "C7": "strfwd",
    "C8": "reversed",
    "C9": "strfwd",
    "C10": "strfwd",
    "O1": "strfwd",
    "O2": "reversed",
    "O3": "strfwd",
    "O4": "reversed",
    "O5": "strfwd",
    "O6": "reversed",
    "O7": "strfwd",
    "O8": "strfwd",
    "O9": "strfwd",
    "O10": "strfwd"
}

strfwd_score_map = {
    1: -5,
    2: -2.5,
    3: 0,
    4: 2.5,
    5: 5   
}
