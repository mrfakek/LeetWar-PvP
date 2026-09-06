import requests
import re

# === НАСТРОЙКА ИГРОКОВ ===
PLAYERS = {
    "mrfakek": "mrfakek",
    "TrueRyoB": "TrueRyoB"
}

def get_leetcode_stats(username):
    url = "https://leetcode.com"
    query = """
    query userProblemsSolved($username: String!) {
        matchedUser(username: $username) {
            submitStatsGlobal {
                acSubmissionNum {
                    difficulty
                    count
                }
            }
        }
    }
    """
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://leetcode.com/"
    }
    
    try:
        response = requests.post(url, json={"query": query, "variables": {"username": username}}, headers=headers, timeout=15)
        if response.status_code == 200:
            json_data = response.json()
            
            # Проверяем, существует ли вообще такой пользователь в системе LeetCode
            if "data" in json_data and json_data["data"].get("matchedUser") is not None:
                submission_stats = json_data["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"]
                
                stats = {"easy": 0, "medium": 0, "hard": 0, "total": 0}
                for item in submission_stats:
                    # Переводим в нижний регистр, чтобы убрать проблемы с разным написанием "Easy" / "easy"
                    diff = item["difficulty"].lower()
                    if diff == "easy":
                        stats["easy"] = item["count"]
                    elif diff == "medium":
                        stats["medium"] = item["count"]
                    elif diff == "hard":
                        stats["hard"] = item["count"]
                    elif diff == "all":
                        stats["total"] = item["count"]
                return stats
            else:
                print(f"⚠️ Предупреждение: Пользователь {username} не найден на LeetCode (возможно, опечатка в нике).")
    except Exception as e:
        print(f"❌ Ошибка соединения с LeetCode для {username}: {e}")
        
    return {"easy": 0, "medium": 0, "hard": 0, "total": 0}


def calculate_xp(stats):
    return (stats["easy"] * 10) + (stats["medium"] * 50) + (stats["hard"] * 200)

def main():
    leaderboard = []
    
    for display_name, leetcode_username in PLAYERS.items():
        print(f"Загрузка данных напрямую с LeetCode для {display_name}...")
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
    
    # Сборка красивой разметки таблицы
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
    
    # Запись новой таблицы в README
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()
        
    pattern = r"<!-- ТАБЛИЦА_СТАРТ -->.*?<!-- ТАБЛИЦА_ЭНД -->"
    replacement = f"<!-- ТАБЛИЦА_СТАРТ -->\n{new_table_content}\n<!-- ТАБЛИЦА_ЭНД -->"
    updated_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_readme)
        
    print("Таблица лидеров успешно обновлена официальными данными!")

if __name__ == "__main__":
    main()
