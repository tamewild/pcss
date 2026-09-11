import re

def last_box(str):
    tag = "\\boxed{"
    tag_start = str.rfind(tag)
    if tag_start == -1:
        return str
    
    content = str[tag_start + len(tag):]
    depth = 1
    for i, char in enumerate(content):
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                return content[:i].strip()
                
    return content.strip()

#directly ported
def normalize_feature(feature: str):
    # standardize cases
    feature = feature.lower()

    # remove quotes
    feature = feature.replace("'", "")
    feature = feature.replace("\"", "")

    # remove spaces
    feature = feature.replace(" ", "")

    # remove the prefix
    feature = feature.removeprefix("the")

    # remove dashes
    feature = feature.replace("-", "")

    # remove commas
    feature = feature.replace(",", "")

    # remove dots
    feature = feature.replace(".", "")

    return feature

# not the fastest way to do things, but oh well. i can't be bothered.
def parse_answer(str, house_amount):
    try:
        final_answer = last_box(str).replace("\n", " ").replace(" \\ ", " \\\\ ") # replacements are to support old qwq

        houses = [[] * house_amount for _ in range(house_amount)]

        lines = final_answer.split(" \\\\ ")[1:-1] # skip header and footer

        for line in lines:
            normalized = re.sub(r"\\[a-z]+", "", line).replace("{", "").replace("}", "").strip()
            items = normalized.split(" & ")
            try:
                # handle houses as rows
                house_number = int(items[0])
                houses[house_number - 1].extend(items[1:])
            except:
                # handle houses as columns
                for i, feature in enumerate(items[1:]):
                    houses[i].append(feature)

        return houses
    except Exception as e:
        print(f"Error encountered when parsing answer: {e}")
        return None

def compare_answer(answer_text: str, solution_houses: list[list[str]]):
    def find_matching_solution_feature(feature, solution_features):
        feature = normalize_feature(feature)
        if not feature:
            return False

        for solution_feature in solution_features:
            solution_feature = normalize_feature(solution_feature)

            if solution_feature.find(feature) != -1:
                return True

            without_the = solution_feature.replace("the", "")

            if without_the.find(feature) != -1:
                return True

            tp_abbreviated = without_the.replace("toiletpaper", "tp")

            if tp_abbreviated.find(feature) != -1:
                return True

            gta_v_abbreviated = tp_abbreviated.replace("grandftauto", "gta")

            if gta_v_abbreviated.find(feature) != -1:
                return True

            lol_abbreviated = gta_v_abbreviated.replace("leagueoflegends", "lol")

            if lol_abbreviated.find(feature) != -1:
                return True

        return False

    houses = parse_answer(answer_text, len(solution_houses))

    if houses is None:
        return False

    for house, solution_house in zip(houses, solution_houses):
        if len(house) != len(solution_house):
            return False

        for feature in house:
            if not find_matching_solution_feature(feature, solution_house):
                return False

    return True

def parse_solution(solution_json):
    import json
    houses = json.loads(solution_json)["houses"]
    return list(map(lambda house: list(house["features"].values()), houses))

# tests

case_1 = r"\begin{array}{|c|c|c|c|c|} \hline \text{House Number} & \text{Activity} & \text{Holiday} & \text{Flower} & \text{Music} \ \hline 1 & \text{Fishing} & \text{Thanksgiving} & \text{Orchid} & \text{Electronic} \ \hline 2 & \text{Swimming} & \text{Christmas} & \text{Lily} & \text{Jazz} \ \hline \end{array}"

assert compare_answer(
    case_1,
    [
        [
            "Fishing",
            "Thanksgiving",
            "Orchid",
            "Electronic"
        ],
        [
            "Swimming",
            "Christmas",
            "Lily",
            "Jazz"
        ]
    ]
)

case_2 = r"""[\boxed{\begin{array}{cc}

\text{House} & \text{Social Media Platform} \

1 & \text{TikTok} \

2 & \text{Facebook} \

\end{array}}]"""

assert compare_answer(
    case_2,
    [
        ["TikTok"],
        ["Facebook"]
    ]
)

case_3 = r"""$$
\boxed{
\begin{array}{|c|c|c|c|c|c|}
\hline
\text{House} & \text{Name} & \text{Most Annoying Habit} & \text{Furniture Style} & \text{Company Role} & \text{Favorite American Football Player} \\
\hline
1 & \text{David} & \text{Talking During Movies} & \text{Rustic} & \text{Salesperson} & \text{Allen} \\
2 & \text{Eve} & \text{Interrupting} & \text{Bohemian} & \text{Engineer} & \text{Rodgers} \\
3 & \text{Alice} & \text{Clicking Pens} & \text{Mid-Century Modern} & \text{Analyst} & \text{Jackson} \\
4 & \text{Charlie} & \text{Tailgating} & \text{Traditional} & \text{Designer} & \text{Brady} \\
5 & \text{Bob} & \text{Loud Chewing} & \text{Industrial} & \text{Manager} & \text{Mahomes} \\
\hline
\end{array}
}
$$"""

assert compare_answer(
    case_3,
    [
        ["David", "Talking During Movies", "Rustic", "Salesperson", "Allen"],
        ["Eve", "Interrupting", "Bohemian", "Engineer", "Rodgers"],
        ["Alice", "Clicking Pens", "Mid-Century Modern", "Analyst", "Jackson"],
        ["Charlie", "Tailgating", "Traditional", "Designer", "Brady"],
        ["Bob", "Loud Chewing", "Industrial", "Manager", "Mahomes"]
    ]
)

case_4 = r"""\begin{array}{|c|c|c|c|c|c|}
\hline
\text{House} & \text{Board Game} & \text{Streamer} & \text{Weather} & \text{Dessert} & \text{Philosophical Quote} \\
\hline
1 & 7 \text{ Wonders} & \text{Ninja} & \text{Snowy} & \text{Cookies} & \text{'Know thyself'} \\
2 & \text{Catan} & \text{Sykkuno} & \text{Sunny} & \text{Brownies} & \text{'The unexamined life is not worth living'} \\
3 & \text{Codenames} & \text{Pokimane} & \text{Rainy} & \text{Fruit Salad} & \text{'Be the change that you wish to see in the world'} \\
4 & \text{Chess} & \text{xQc} & \text{Windy} & \text{Cake} & \text{'Cogito, ergo sum'} \\
5 & \text{Ticket to Ride} & \text{Valkyrae} & \text{Mild} & \text{Pie} & \text{'It is impossible to step into the same river twice'} \\
\hline
\end{array}"""

assert compare_answer(
    case_4,
    [
        ["7 Wonders", "Ninja", "Snowy", "Cookies", "'Know thyself'"],
        ["Catan", "Sykkuno", "Sunny", "Brownies", "'The unexamined life is not worth living'"],
        ["Codenames", "Pokimane", "Rainy", "Fruit Salad", "'Be the change that you wish to see in the world'"],
        ["Chess", "xQc", "Windy", "Cake", "'Cogito, ergo sum'"],
        ["Ticket to Ride", "Valkyrae", "Mild", "Pie", "'It is impossible to step into the same river twice'"]
    ]
)

case_5 = r"""\begin{array}{|c|c|c|c|c|}
\hline
\text{House} & \text{Preferred Time of Day} & \text{Most Annoying Habit} & \text{Favorite Room} & \text{Favorite Board Game} \\
\hline
1 & \text{Late Night} & \text{Clicking Pens} & \text{Bedroom} & \text{Codenames} \\
2 & \text{Afternoon} & \text{Loud Chewing} & \text{Garden} & \text{Pandemic} \\
3 & \text{Evening} & \text{Talking During Movies} & \text{Kitchen} & \text{Ticket to Ride} \\
4 & \text{Early Morning} & \text{Not Replacing Toilet Paper} & \text{Living Room} & \text{Catan} \\
\hline
\end{array"""

assert compare_answer(
    case_5,
    [
        ["Late Night", "Clicking Pens", "Bedroom", "Codenames"],
        ["Afternoon", "Loud Chewing", "Garden", "Pandemic"],
        ["Evening", "Talking During Movies", "Kitchen", "Ticket to Ride"],
        ["Early Morning", "Not Replacing the Toilet Paper", "Living Room", "Catan"]
    ]
)

case_6 = r"""\begin{array}{|c|c|c|c|c|}
\hline
\text{House} & \text{Person} & \text{Flower} & \text{House Style} & \text{Cigar} \\
\hline
1 & Eric & Carnations & Craftsman & Dunhill \\
2 & Peter & Daffodils & Colonial & Prince \\
3 & Alice & Lilies & Ranch & Blue Master \\
4 & Arnold & Roses & Victorian & Pall Mall \\
\hline
\end{array}"""

assert compare_answer(
    case_6,
    [
        ["Eric", "Carnations", "Craftsman", "Dunhill"],
        ["Peter", "Daffodils", "Colonial", "Prince"],
        ["Alice", "Lilies", "Blue Master", "Ranch"],
        ["Arnold", "Roses", "Victorian", "Pall Mall"]
    ]
)

case_7 = r"""\begin{array}{|c|c|c|c|c|}
\hline
\text{House} & \text{Season} & \text{Flower} & \text{Art} & \text{Quote} \\
\hline
1 & Autumn & Lily & Digital Art & Know thyself \\
2 & Spring & Rose & Photography & The unexamined life is not worth living \\
3 & Winter & Daisy & Sculpture & Be the change that you wish to see in the world \\
4 & Summer & Sunflower & Drawing & I think, therefore I am \\
\hline
\end{array}"""

assert compare_answer(
    case_7,
    [
        ["Autumn", "Lily", "Digital Art", "'Know thyself'"],
        ["Spring", "Rose", "Photography", "\"The unexamined life is not worth living\""],
        ["Winter", "Daisy", "Sculpture", "'Be the change that you wish to see in the world'"],
        ["Summer", "Sunflower", "Drawing", "\"I think, therefore I am\""]
    ]
)

case_8 = r"""\begin{array}{|c|c|c|c|c|}
\hline
\text{House} & \text{Shoe} & \text{Day} & \text{Coffee} & \text{Quote} \\
\hline
1 & \text{Flats} & \text{Sunday} & \text{Cold Brew} & \text{"The unexamined life is not worth living"} \\
2 & \text{Boots} & \text{Wednesday} & \text{Cappuccino} & \text{"It is impossible to step into the same river twice"} \\
3 & \text{Sneakers} & \text{Thursday} & \text{Latte} & \text{"I think, therefore I am"} \\
4 & \text{Heels} & \text{Saturday} & \text{Espresso} & \text{"Cogito, ergo sum"} \\
\hline
\end{array}"""

assert compare_answer(
    case_8,
    [
        ["Flats", "Sunday", "Cold Brew", "The unexamined life is not worth living"],
        ["Boots", "Wednesday", "Cappuccino", "'It is impossible to step into the same river twice'"],
        ["Sneakers", "Thursday", "Latte", "\"I think, therefore I am\""],
        ["Heels", "Saturday", "Espresso", "'Cogito, ergo sum'"]
    ]
)

case_9 = r"""\begin{array}{|c|c|c|c|c|}
\hline
\text{House} & \text{Name} & \text{Board Game} & \text{Cuisine} & \text{Furniture} \\
\hline
1 & Frank & Codenames & Thai & Modern \\
2 & Alice & Catan & Mexican & Rustic \\
3 & Charlie & Pandemic & Indian & Mid-Century \\
4 & Bob & Chess & French & Industrial \\
\hline
\end{array}"""

assert compare_answer(
    case_9,
    [
        ["Frank", "Codenames", "Thai", "Modern"],
        ["Alice", "Catan", "Mexican", "Rustic"],
        ["Charlie", "Pandemic", "Indian", "Mid-Century Modern"],
        ["Bob", "Chess", "French", "Industrial"]
    ]
)

case_10 = r"""\begin{array}{|c|c|c|c|c|}
\hline
\text{House} & \text{Preferred Time of Day} & \text{Most Annoying Habit} & \text{Favorite Room} & \text{Favorite Board Game} \\
\hline
1 & \text{Late Night} & \text{Clicking Pens} & \text{Bedroom} & \text{Codenames} \\
2 & \text{Afternoon} & \text{Loud Chewing} & \text{Garden} & \text{Pandemic} \\
3 & \text{Evening} & \text{Talking During Movies} & \text{Kitchen} & \text{Ticket to Ride} \\
4 & \text{Early Morning} & \text{Not Replacing TP} & \text{Living Room} & \text{Catan} \\
\hline
\end{array}"""

assert compare_answer(
    case_10,
    [
        ["Late Night", "Clicking Pens", "Bedroom", "Codenames"],
        ["Afternoon", "Loud Chewing", "Garden", "Pandemic"],
        ["Evening", "Talking During Movies", "Kitchen", "Ticket to Ride"],
        ["Early Morning", "Not Replacing the Toilet Paper Roll", "Living Room", "Catan"]
    ]
)

case_11 = r"""\begin{array}{|c|c|c|c|c|}
\hline
\text{House} & \text{Preferred Time of Day} & \text{Most Annoying Habit} & \text{Favorite Room} & \text{Favorite Board Game} \\
\hline
1 & \text{Late Night} & \text{Clicking Pens} & \text{Bedroom} & \text{Codenames} \\
2 & \text{Afternoon} & \text{Loud Chewing} & \text{Garden} & \text{Pandemic} \\
3 & \text{Evening} & \text{Talking During Movies} & \text{Kitchen} & \text{Ticket to Ride} \\
4 & \text{Early Morning} & \text{Not Replacing TP Roll} & \text{Living Room} & \text{Catan} \\
\hline
\end{array}"""

assert compare_answer(
    case_11,
    [
        ["Late Night", "Clicking Pens", "Bedroom", "Codenames"],
        ["Afternoon", "Loud Chewing", "Garden", "Pandemic"],
        ["Evening", "Talking During Movies", "Kitchen", "Ticket to Ride"],
        ["Early Morning", "Not Replacing the Toilet Paper Roll", "Living Room", "Catan"]
    ]
)

case_12 = r"""\begin{array}{|c|c|c|c|c|c|}
\hline
\text{House} & 1 & 2 & 3 & 4 & 5 \\
\hline
\text{Cooking Method} & \text{Sous Vide} & \text{Baking} & \text{Slow Cooking} & \text{Stovetop Cooking} & \text{Air Frying} \\
\hline
\text{Art Type} & \text{Painting} & \text{Calligraphy} & \text{Sculpture} & \text{Digital Art} & \text{Drawing} \\
\hline
\text{Role} & \text{Engineer} & \text{Designer} & \text{Marketer} & \text{Salesperson} & \text{Manager} \\
\hline
\text{Video Game} & \text{Minecraft} & \text{GTA V} & \text{Fortnite} & \text{Zelda} & \text{LoL} \\
\hline
\text{Annoying Habit} & \text{Talking During Movies} & \text{Loud Chewing} & \text{Not Replacing TP Roll} & \text{Clicking Pens} & \text{Tailgating} \\
\hline
\end{array}"""

assert compare_answer(
    case_12,
    [
        ["Sous Vide", "Painting", "Engineer", "Minecraft", "Talking During Movies"],
        ["Baking", "Calligraphy", "Designer", "Loud Chewing", "Grand Theft Auto V"],
        ["Slow Cooking", "Sculpture", "Marketer", "Fortnite", "Not Replacing the Toilet Paper Roll"],
        ["Stovetop Cooking", "Digital Art", "Salesperson", "Zelda", "Clicking Pens"],
        ["Air Frying", "Drawing", "Manager", "LoL", "Tailgating"]
    ]
)

assert compare_answer(
    case_12,
    [
        ["Sous Vide", "Painting", "Engineer", "Minecraft", "Talking During Movies"],
        ["Baking", "Calligraphy", "Designer", "Loud Chewing", "Grand Theft Auto V"],
        ["Slow Cooking", "Sculpture", "Marketer", "Fortnite", "Not Replacing the Toilet Paper Roll"],
        ["Stovetop Cooking", "Digital Art", "Salesperson", "Zelda", "Clicking Pens"],
        ["Air Frying", "Drawing", "Manager", "League of Legends", "Tailgating"]
    ]
)
