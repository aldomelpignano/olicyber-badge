import requests
import base64
import os 
import json
from collections import defaultdict
import io
import matplotlib.pyplot as plt

TOKEN = os.getenv("OC_TOKEN")

if not (TOKEN.count("-") == 4 and len(TOKEN) == 36):
    raise ValueError("Invalid token format")

PLAYER_URL = "https://training.olicyber.it/api/scoreboard/player"
SCOREBOARD_URL = "https://training.olicyber.it/api/scoreboard"

HEADERS = {
    "Authorization": f"Token {TOKEN}"
}

TEMPLATE_COLOR_PALETTES = {
    "hacker": ['#00ff00', '#00cc00', '#009900',
               '#00ff00', '#00cc00', '#006600', '#003300']
}

def resolve_fullname(player_data):
    return f'{player_data["name"]} {player_data["surname"]} ({player_data["nickname"]})'

def find_scoreboard_position(player_data):
    display_name = resolve_fullname(player_data)

    scoreboard = requests.get(
        SCOREBOARD_URL,
        params={"noFreeze": False},
        headers=HEADERS
    ).json()["scoreboard"]

    return next(
        i for i, player in enumerate(scoreboard)
        if player["displayedName"] == display_name
    ) + 1

def find_best_category(player_data):
    categories = player_data["categories"]
    return max(categories, key=lambda c: categories[c]["solves"]).capitalize()

def generate_histogram_svg(categories):
    if not categories:
        return ""

    palette = TEMPLATE_COLOR_PALETTES["hacker"]
    title_color, text_color, *chart_colors = palette

    plt.figure(figsize=(6, 3), dpi=100)
    plt.style.use('default')

    plt.title("Completed Challenges",
              fontsize=14,
              color=title_color,
              fontweight='bold')

    category_names = list(categories.keys())
    percentages = list(categories.values())

    plt.pie(
        percentages,
        labels=category_names,
        colors=chart_colors,
        labeldistance=1.1,
        wedgeprops={
            'edgecolor': 'black',
            'linewidth': 1,
            'antialiased': True
        },
        textprops={
            'color': text_color,
            'fontsize': 10,
            'fontweight': 'bold'
        }
    )

    buffer = io.BytesIO()
    plt.savefig(buffer, format='svg',
                bbox_inches='tight', transparent=True)
    plt.close()

    svg_data = buffer.getvalue().decode('utf-8')
    return base64.b64encode(svg_data.encode('utf-8')).decode('utf-8')

def main():
    user_data = requests.get(PLAYER_URL, headers=HEADERS).json()

    rank = find_scoreboard_position(user_data)

    useful_data = {
        "scoreboard_position": rank,
        "solved_challenges": user_data["correctSubmissions"],
        "score": user_data["score"],
        "best_category": find_best_category(user_data),
    }

    with open("player_data.json", "w") as json_file:
        json.dump(useful_data, json_file, indent=4)

    categories = user_data["categories"]
    total_solves = user_data["correctSubmissions"]

    category_percentages = {}
    if total_solves > 0:
        for category in categories:
            solves = categories[category]["solves"]
            percentage = (solves / total_solves) * 100
            category_percentages[category.capitalize()] = percentage

    histogram_base64 = generate_histogram_svg(category_percentages)
    if histogram_base64:
        useful_data["histogram"] = f'data:image/svg+xml;base64,{histogram_base64}'
    else:
        useful_data["histogram"] = ""

    with open("data/template_hacker.svg", 'r') as template_file:
        card_template = template_file.read()

    card = card_template.format_map(defaultdict(lambda: "", useful_data))

    with open("card.svg", "w") as f:
        f.write(card)

if __name__ == "__main__":
    main()