import requests
import re

# === НАСТРОЙКА ИГРОКОВ ===
# Имена в левой части автоматически станут названиями колонок в таблице
PLAYERS = {
    "mrfakek-fortress": "mrfakek",
    "TrueRyoB-fortress": "TrueRyoB"
}

def get_leetcode_stats(username):
    # Работаем через стабильное и быстрое API-зеркало без блокировок SSL
    site = "https://alfa-leetcode-api.onrender.com"
    folder = "/userProfile/"
    url = site + folder + str(username)
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            
            # Проверяем структуру ответа
            if "totalSolved" in data:
                return {
                    "easy": data.get("easySolved", 0),
                    "medium": data.get("mediumSolved", 0),
                    "hard": data.get("hardSolved", 0),
                    "total": data.get("totalSolved", 0)
                }
    except Exception as e:
        print(f"Ошибка получения данных для {username}: {e}")
        
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
    
    # Сортировка участников по количеству XP (у кого больше — тот выше)
    leaderboard.sort(key=lambda x: x["xp"], reverse=True)
    
    # === ИСПРАВЛЕНО: Сборка структуры под лор Некро-Крепостей ===
    table_lines = [
        "| Место | Крепость некроманта| 💀 Скелеты (Easy) | 👻 Вампиры (Medium) | 👹 Архидемоны (Hard) | Гарнизон Стен | 🔥 Боевая Мощь Цитадели (XP) |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: |"
    ]
    
    for index, p in enumerate(leaderboard, start=1):
        medal = "🥇" if index == 1 else "🥈"
        table_lines.append(
            f"| {medal} | **{p['name']}** | {p['easy']} | {p['medium']} | {p['hard']} | {p['total']} | **{p['xp']} XP** |"
        )
        
    new_table_content = "\n".join(table_lines)
    
    # Чтение и автоматическая перезапись README
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()
        
    pattern = r"<!-- ТАБЛИЦА_СТАРТ -->.*?<!-- ТАБЛИЦА_ЭНД -->"
    replacement = f"<!-- ТАБЛИЦА_СТАРТ -->\n{new_table_content}\n<!-- ТАБЛИЦА_ЭНД -->"
    updated_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_readme)
        
    print("Таблица лидеров успешно обновилась!")

if __name__ == "__main__":
    main()


