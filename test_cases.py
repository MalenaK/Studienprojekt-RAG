from evaluation import test_model

#We number the test such that they always begin with a hundred to stay flexible and add tests for a specific document if necessary

#FIBA Rulebook DOCUMENT
test_case_101 = ["A game of Basketball is played by how many teams?", "2"]
test_case_101_complement = ["A game of Basketball is played by how many teams?", "10"]

test_case_102 = ["What dimensions is the playing ground?", "28 m in length by 15 m in width"]
test_case_102_complement = ["What dimensions is the playing ground?", "12 m in length by 5 m in width"]

test_case_103 = ["Can lines be of different colors?", "No"]
test_case_103_complement = ["Can lines be of different colors?", "Yes"]

test_case_104 = ["How can a defensive player establish a legal guarding position?", "Face his opponent and have both feet on the floor"]
test_case_104_complement = ["How can a defensive player establish a legal guarding position?", "Be airborne"]

test_case_105 = ["May a team substitute a player?", "Yes"]
test_case_105_complement = ["May a team substitute a player?", "No"]

test_case_106 = ["How long does a timeout last?", "1 Minute"]
test_case_106_complement = ["How long does a timeout last?", "1 hour"]

test_case_107 = ["Of how many quarters does a game consist?", "4"]
test_case_107_complement = ["Of how many quarters does a game consist?", "2"]

test_case_108 = ["How many minutes does a quarter have?", "10 minutes"]
test_case_108_complement = ["How many minutes does a quarter have?", "15 minutes"]

test_case_109 = ["How many players are allowed for each team on the play court?", "5"]
test_case_109_complement = ["How many minutes does a quarter have?", "15 minutes"]

test_case_110 = ["What is charging?", "Charging is illegal personal contact, with or without the ball, by pushing or moving into an opponent’s torso."]
test_case_110_complement = ["What is charging?", "Pulling yourself up via the rim to score a goal"]


fiba_positive_test_cases = [
    test_case_101,
    test_case_102,
    test_case_103,
    test_case_104,
    test_case_105,
    test_case_106,
    test_case_107,
    test_case_108,
    test_case_109,
    test_case_110
]

fiba_negative_test_cases = [
    test_case_101_complement,
    test_case_102_complement,
    test_case_103_complement,
    test_case_104_complement,
    test_case_105_complement,
    test_case_106_complement,
    test_case_107_complement,
    test_case_108_complement,
    test_case_109_complement,
    test_case_110_complement
]



#M4A3 Sherman Document

test_case_201 = ["How thick is the hull armor?", "1 inch"]
test_case_201_complement = ["How thick is the hull armor?", "15 inch"]

test_case_202 = ["What is the maximum sustained speed on a hard road?", "26 mph"]
test_case_202_complement = ["What is the maximum sustained speed on a hard road?", "26 kmh"]

test_case_203 = ["What range does the voltmeter have?", "16 to 32 volts"]
test_case_203_complement = ["What range does the voltmeter have?", "6 to 62 volts"]

test_case_204 = ["Is the spark control automatic?", "Yes"]
test_case_204_complement = ["Is the spark control automatic?", "No"]

test_case_205 = ["What is the rated horsepower for the engine?", "500 at 2600 rpm"]
test_case_205_complement = ["What is the rated horsepower for the engine?", "250 at 2600 rpm"]

test_case_206 = ["What is the weight without armament, fuel or crew?", "59560 lb"]
test_case_206_complement = ["What is the weight without armament, fuel or crew?", "59560 kg"]

test_case_207 = ["What guns are part of the combination turret mount?", "1 gun, 75-mm, M3 and 1 gun, machine, cal. .30, M1919A4"]
test_case_207_complement = ["What guns are part of the combination turret mount?", "1 gun, 90-mm, M4 and 1 gun, machine, cal. .50, M2-Browning"]

test_case_208 = ["How many degrees can the turret be rotated?", "360"]
test_case_208_complement = ["How many degrees can the turret be rotated?", "300"]

test_case_209 = ["How to stop the engine?", "After completing a run, the engine must be allowed to operate at 500 rpm for two minutes to assure a gradual and uniform cooling of the valves and other various engine parts."]
test_case_209_complement = ["How to stop the engine?", "Just turn it off by taking out the key"]

test_case_210 = ["What is the overall length?", "232 1/2-in"]
test_case_210_complement = ["What is the overall length?", "40 meters"]


sherman_positive_test_cases = [
    test_case_201,
    test_case_202,
    test_case_203,
    test_case_204,
    test_case_205,
    test_case_206,
    test_case_207,
    test_case_208,
    test_case_209,
    test_case_210
]

sherman_negative_test_cases = [
    test_case_201_complement,
    test_case_202_complement,
    test_case_203_complement,
    test_case_204_complement,
    test_case_205_complement,
    test_case_206_complement,
    test_case_207_complement,
    test_case_208_complement,
    test_case_209_complement,
    test_case_210_complement
]




#Germany fact list Document
test_case_301 = ["What was the real gdp of Germany in 2023?", "5.23 trillion"]
test_case_301_complement = ["What was the real gdp of Germany in 2023?", "6 trillion"]

test_case_302 = ["Who is the biggest export partner of Germany?", "The United States 🦅"]
test_case_302_complement = ["Who is the biggest export partner of Germany?", "Luxemburg"]

test_case_303 = ["Who is the biggest import partner of Germany?", "China"]
test_case_303_complement = ["Who is the biggest import partner of Germany?", "France"]

test_case_304 = ["Who is the head of government?", "Olaf Scholz"]
test_case_304_complement = ["Who is the head of government?", "Angela Merkel"]

test_case_305 = ["Who is the chief of state?", "Frank-Walter Steinmeier"]
test_case_305_complement = ["Who is the chief of state?", "Pierre Danke"]

test_case_306 = ["What is the population growth?", "-0.12%"]
test_case_306_complement = ["What is the population growth?", "0.14%"]

test_case_307 = ["What is the total population?", "84119100"]
test_case_307_complement = ["What is the total population?", "22200000"]

test_case_308 = ["What is the total area of Germany? How much land and how water does it consist of?", "totaL: 357022 sq km, land: 348672 sq km, water: 8350 sq km"]
test_case_308_complement = ["What is the total area of Germany? How much land and how water does it consist of?", "totaL: 100000 sq km, land: 1000 sq km, water: 99000 sq km"]

test_case_309 = ["What are the 3 largest ethnic groups in Germany?", "1. German (85,4%), 2.Turkish(1.8%), 3.Ukrainian(1.4%)"]
test_case_309_complement = ["What are the 3 largest ethnic groups in Germany?", "1. French (45%), 2.Albanian(44%), 3.Mongolian(1%)"]

test_case_310 = ["What are the 3 largest religions in Germany?", "1.Roman Catholic (24.8%), 2.Protestant (22.6%), 3.Muslim (3.7%)"]
test_case_310_complement = ["What are the 3 largest religions in Germany?", "1.Hindu (25%), 2.Muslim (21%), 3.Jewish (12 %)"]


germany_positive_test_cases = [
    test_case_301,
    test_case_302,
    test_case_303,
    test_case_304,
    test_case_305,
    test_case_306,
    test_case_307,
    test_case_308,
    test_case_309,
    test_case_310
]

germany_negative_test_cases = [
    test_case_301_complement,
    test_case_302_complement,
    test_case_303_complement,
    test_case_304_complement,
    test_case_305_complement,
    test_case_306_complement,
    test_case_307_complement,
    test_case_308_complement,
    test_case_309_complement,
    test_case_310_complement
]

positive_test_cases = fiba_positive_test_cases + sherman_positive_test_cases + germany_positive_test_cases
negative_test_cases = fiba_negative_test_cases + sherman_negative_test_cases + germany_negative_test_cases