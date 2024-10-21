from evaluation import test_model

#We number the test such that they always begin with a hundred to stay flexible and add tests for a specific document if necessary

#FIBA Rulebook DOCUMENT
def test_case_101():
    test_model("A game of Basketball is played by how many teams?", "2")


def test_case_101_complement():
    test_model("A game of Basketball is played by how many teams?", "10")


def test_case_102():
    test_model("What dimensions is the playing ground?", "28 m in length by 15 m in width")

def test_case_102_complement():
    test_model("What dimensions is the playing ground?", "12 m in length by 5 m in width")

def test_case_103():
    test_model("Can lines be of different colors?", "No")

def test_case_103_complement():
    test_model("Can lines be of different colors?", "Yes")


def test_case_104():
    test_model("How can a defensive player establish a legal guarding position?", "Face his opponent and have both feet on the floor")

def test_case_104_complement():
    test_model("How can a defensive player establish a legal guarding position?", "Be airborne")

def test_case_105():
    test_model("May a team substitute a player?", "Yes")

def test_case_105_complement():
    test_model("May a team substitute a player?", "No")

def test_case_106():
    test_model("How long does a timeout last?", "1 Minute")

def test_case_106_complement():
        test_model("How long does a timeout last?", "1 hour")

def test_case_107():
    test_model("Of how many quarters does a game consist?", "4")

def test_case_107_complement():
    test_model("Of how many quarters does a game consist?", "2")

def test_case_108():
    test_model("How many minutes does a quarter have?", "10 minutes")

def test_case_108_complement():
    test_model("How many minutes does a quarter have?", "15 minutes")

def test_case_109():
    test_model("How many players are allowed for each team on the play court?", "5")

def test_case_109_complement():
    test_model("How many minutes does a quarter have?", "15 minutes")

def test_case_110():
    test_model("What is charging?", "Charging is illegal personal contact, with or without the "
                                    "ball, by pushing or moving into an opponent’s torso.")

def test_case_110_complement():
    test_model("What is charging?", "Pulling yourself up via the rim to score a goal")

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

def test_case_201():
    test_model("How thick is the hull armor?", "1 inch")

def test_case_201_complement():
    test_model("How thick is the hull armor?", "15 inch")


def test_case_202():
    test_model("What is the maximum sustained speed on a hard road?", "26 mph")

def test_case_202_complement():
    test_model("What is the maximum sustained speed on a hard road?", "26 kmh")

def test_case_203():
    test_model("What range does the voltmeter have?", "16 to 32 volts")

def test_case_203_complement():
    test_model("What range does the voltmeter have?", "6 to 62 volts")

def test_case_204():
    test_model("Is the spark control automatic?", "Yes")

def test_case_204_complement():
    test_model("Is the spark control automatic?", "No")

def test_case_205():
    test_model("What is the rated horsepower for the engine?", "500 at 2600 rpm")

def test_case_205_complement():
    test_model("What is the rated horsepower for the engine?", "250 at 2600 rpm")

def test_case_206():
    test_model("What is the weight without armament, fuel or crew?", "59560 lb")

def test_case_206_complement():
    test_model("What is the weight without armament, fuel or crew?", "59560 kg")

def test_case_207():
    test_model("What guns are part of the combination turret mount?", "1 gun, 75-mm, M3 and 1 gun, machine, cal. .30, M1919A4")

def test_case_207_complement():
    test_model("What guns are part of the combination turret mount?", "1 gun, 90-mm, M4 and 1 gun, machine, cal. .50, M2-Browning")

def test_case_208():
    test_model("How many degrees can the turret be rotated?", "360")

def test_case_208_complement():
    test_model("How many degrees can the turret be rotated?", "300")

def test_case_209():
    test_model("How to stop the engine?", "After completing a run, the engine must be allowed to"
                                          " operate at 500 rpm for two minutes to assure a gradual and uniform cooling "
                                          "of the valves and other various engine parts.")
def test_case_209_complement():
    test_model("How to stop the engine?", "Just turn it off by taking out the key")


def test_case_210():
    test_model("What is the overall length?", "232 1/2-in")

def test_case_210_complement():
    test_model("What is the overall length?", "40 meters")

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
def test_case_301():
    test_model("What was the real gdp of Germany in 2023?", "5.23 trillion")


def test_case_301_complement():
    test_model("What was the real gdp of Germany in 2023?", "6 trillion")


def test_case_302():
    test_model("Who is the biggest export partner of Germany?", "The United States 🦅")

def test_case_302_complement():
    test_model("Who is the biggest export partner of Germany?", "Luxemburg")

def test_case_303():
    test_model("Who is the biggest import partner of Germany?", "China")

def test_case_303_complement():
    test_model("Who is the biggest import partner of Germany?", "France")

def test_case_304():
    test_model("Who is the head of government?", "Olaf Scholz")

def test_case_304_complement():
    test_model("Who is the head of government?", "Angela Merkel")

def test_case_305():
    test_model("Who is the chief os state?", "Frank-Walter Steinmeier")

def test_case_305_complement():
    test_model("Who is the chief os state?", "Pierre Danke")

def test_case_306():
    test_model("What is the population growth?", "-0.12%")

def test_case_306_complement():
    test_model("What is the population growth?", "0.14%")

def test_case_307():
    test_model("What is the total population?", "84119100")

def test_case_307_complement():
    test_model("What is the total population?", "22200000")

def test_case_308():
    test_model("What is the total area of Germany? How much land and how water does it consist of?", "totaL: 357022 sq km, land: 348672 sq km, water: 8350 sq km")

def test_case_308_complement():
    test_model("What is the total area of Germany? How much land and how water does it consist of?", "totaL: 100000 sq km, land: 1000 sq km, water: 99000 sq km")


def test_case_309():
    test_model("What are the 3 largest ethnic groups in Germany?", "1. German (85,4%), 2.Turkish(1.8%), 3.Ukrainian(1.4%)")

def test_case_309_complement():
    test_model("What are the 3 largest ethnic groups in Germany?", "1. French (45%), 2.Albanian(44%), 3.Mongolian(1%)")

def test_case_310():
    test_model("What are the 3 largest religions?", "1.Roman Catholic (24.8%), 2.Protestant (22.6%), 3.Muslim (3.7%)")

def test_case_310_complement():
    test_model("What are the 3 largest religions?", "1.Hindu (25%), 2.Muslim (21%), 3.Jewish (12 %)")

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