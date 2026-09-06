import requests
import re

# === НАСТРОЙКА ИГРОКОВ ===
PLAYERS = {
    "mrfakek": "mrfakek",
    "TrueRyoB": "TrueRyoB"
}

def get_leetcode_stats(username):
    url = f"https://vercel.app{username}"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if "parsedRawUser" in data:
                stats = data["parsedRawUser"]["submitStatsGlobal"]["acSubmissionNum"]
                # Порядок в API обычно: 0-All, 1-Easy, 2-Medium, 3-Hard
                return {
                    "easy": stats[1]["count"],
                    "medium": stats[2]["count"],
                    "hard": stats[3]["count"],
                    "total": stats[0]["count"]
                }
    except Exception as e:
        print(f"Ошибка при запросе профиля {username}: {e}")
    return {"easy": 0, "medium": 0, "hard": 0, "total": 0}

def calculate_xp(stats):
    return (stats["easy"] * 10) + (stats["medium"] * 50) + (stats["hard"] * 200)

def main():
    leaderboard = []
    
    for display_name, leetcode_username in PLAYERS.items():
        print(f"Загрузка данных для {display_name}...")
        stats = get_leetcode_stats(leetcode_username)
        xp = calculate_xp(stats)
        
        leaderboard.append({
            "name": display_name,
            "easy": stats["easy"],
            "medium": stats["medium"],
            "hard": stats["hard"],
            "total": stats["total"],
            "xp": xp
        })
    
    # Сортируем: у кого больше XP, тот на 1 месте
    leaderboard.sort(key=lambda x: x["xp"], reverse=True)
    
    # Собираем новую Markdown таблицу
    table_lines = [
        "| Место | Герой | 🟢 Easy | 🟡 Med | 🔴 Hard | Всего задач | 🔥 Общий счет (XP) |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: |"
    ]
    
    for index, p in enumerate(leaderboard, start=1):
        medal = "🥇" if index == 1 else "🥈"
        table_lines.append(
            f"| {medal} | **{p['name']}** | {p['easy']} | {p['medium']} | {p['hard']} | {p['total']} | **{p['xp']} XP** |"
        )
        
    new_table_content = "\n".join(table_lines)
    
    # Читаем README.md и обновляем таблицу между маркерами
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()
        
    pattern = r"<!-- ТАБЛИЦА_СТАРТ -->.*?<!-- ТАБЛИЦА_ЭНД -->"
    replacement = f"<!-- ТАБЛИЦА_СТАРТ -->\n{new_table_content}\n<!-- ТАБЛИЦА_ЭНД -->"
    updated_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_readme)
        
    print("Таблица лидеров успешно пересчитана!")

if __name__ == "__main__":
    main()
