import requests
import re

# === НАСТРОЙКА ИГРОКОВ ===
PLAYERS = {
    "mrfakek": "mrfakek",
    "TrueRyoB": "TrueRyoB"
}

def get_leetcode_stats(username):
    # Используем открытое стабильное зеркало API LeetCode для обхода блокировок GitHub
    url = f"https://herokuapp.com/{username}"

    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            # Проверяем, что профиль успешно найден на сервере
            if data.get("status") == "success":
                return {
                    "easy": data.get("easySolved", 0),
                    "medium": data.get("mediumSolved", 0),
                    "hard": data.get("hardSolved", 0),
                    "total": data.get("totalSolved", 0)
                }
            else:
                print(f"⚠️ Пользователь {username} не найден на LeetCode.")
    except Exception as e:
        print(f"❌ Ошибка получения данных для {username}: {e}")
        
    return {"easy": 0, "medium": 0, "hard": 0, "total": 0}

def calculate_xp(stats):
    return (stats["easy"] * 10) + (stats["medium"] * 50) + (stats["hard"] * 200)

def main():
    leaderboard = []
    
    for display_name, leetcode_username in PLAYERS.items():
        print(f"Загрузка данных через зеркало для {display_name}...")
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
    
    # Сортировка по очкам опыта
    leaderboard.sort(key=lambda x: x["xp"], reverse=True)
    
    # Сборка разметки таблицы
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
    
    # Запись в README
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()
        
    pattern = r"<!-- ТАБЛИЦА_СТАРТ -->.*?<!-- ТАБЛИЦА_ЭНД -->"
    replacement = f"<!-- ТАБЛИЦА_СТАРТ -->\n{new_table_content}\n<!-- ТАБЛИЦА_ЭНД -->"
    updated_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_readme)
        
    print("Таблица лидеров успешно обновлена!")

if __name__ == "__main__":
    main()
