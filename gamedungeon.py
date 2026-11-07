import os
import time
import random
import sys

lang = "th" 

texts = {
    "th": {
        "choose_lang": "เลือกภาษา / Select Language:\nพิมพ์ 't' สำหรับภาษาไทย\nพิมพ์ 'e' สำหรับ English\nเลือก: ",
        "invalid_lang": "กรุณาพิมพ์ 't' หรือ 'e' เท่านั้น",
        "intro1": "คุณตื่นขึ้นมาในดันเจี้ยนที่มืดมิด...",
        "intro2": "มีทางแยกอยู่ด้านหน้าคุณ",
        "status": " ❤️ HP: {hp}/100 | ⚔️ ATK: {atk} | 🧪 Potions: {potions} | 💰 Gold: {gold}",
        "controls": "\n[การเดิน] พิมพ์ W(หน้า) A(ซ้าย) S(ถอย) D(ขวา) | Q(ออก) แล้วกด Enter",
        "invalid_dir": "❌ กรุณาพิมพ์ W, A, S, D เพื่อเดิน หรือ Q เพื่อออก",
        "combat_intro": "\n⚠️ คุณเจอ {name} (HP: {hp}, ATK: {atk})! ⚠️",
        "combat_ctrl": "\n[การต่อสู้] พิมพ์ J(โจมตี) K(กินยา) L(หนี) แล้วกด Enter",
        "attack": "⚔️ คุณโจมตี {name} สร้างความเสียหาย {dmg} หน่วย!",
        "potion_heal": "🧪 คุณกินยา ฟื้นฟู HP {heal} หน่วย!",
        "no_potion": "❌ คุณมียาไม่พอ!",
        "run_success": "🏃 คุณวิ่งหนีสำเร็จ!",
        "run_fail": "❌ วิ่งหนีไม่สำเร็จ!",
        "monster_attack": "💥 {name} โจมตีคุณ สร้างความเสียหาย {dmg} หน่วย!",
        "monster_dead": "\n🎉 คุณปราบ {name} ได้สำเร็จ!",
        "gold_gain": "💰 ได้รับ {gold} Gold!",
        "event_treasure": "\n🎁 คุณเจอหีบสมบัติ! ได้รับ {gold} Gold!",
        "event_trap": "\n🪤 คุณเหยียบกับดัก! โดนความเสียหาย {dmg} HP!",
        "event_trap_dead": "\n💀 คุณตายเพราะกับดัก! Game Over...",
        "event_fountain": "\n⛲ คุณเจอน้ำพุศักดิ์สิทธิ์! ฟื้นฟู HP {heal} หน่วย!",
        "game_over": "\n=========================================\n💀 YOU DIED 💀\nคุณสะสม Gold ได้ทั้งหมด {gold} ก่อนตาย\nGame Over...\n=========================================",
        "continue": "\n(กด Enter เพื่อไปต่อ...)",
        "quit": "\nขี้เกียจผจญภัยแล้วเหรอ? Goodbye! 👋"
    },
    "en": {
        "choose_lang": "Select Language / เลือกภาษา:\nType 't' for Thai\nType 'e' for English\nChoose: ",
        "invalid_lang": "Please type only 't' or 'e'",
        "intro1": "You wake up in a dark dungeon...",
        "intro2": "There is a fork in the road ahead.",
        "status": " ❤️ HP: {hp}/100 | ⚔️ ATK: {atk} | 🧪 Potions: {potions} | 💰 Gold: {gold}",
        "controls": "\n[Move] Type W(Forward) A(Left) S(Backward) D(Right) | Q(Quit) then press Enter",
        "invalid_dir": "❌ Please type W, A, S, D to move, or Q to quit.",
        "combat_intro": "\n⚠️ You encountered {name} (HP: {hp}, ATK: {atk})! ⚠️",
        "combat_ctrl": "\n[Combat] Type J(Attack) K(Potion) L(Run) then press Enter",
        "attack": "⚔️ You attacked {name} for {dmg} damage!",
        "potion_heal": "🧪 You drank a potion and restored {heal} HP!",
        "no_potion": "❌ You don't have enough potions!",
        "run_success": "🏃 You successfully ran away!",
        "run_fail": "❌ Failed to run away!",
        "monster_attack": "💥 {name} attacked you for {dmg} damage!",
        "monster_dead": "\n🎉 You defeated {name}!",
        "gold_gain": "💰 You received {gold} Gold!",
        "event_treasure": "\n🎁 You found a treasure chest! Received {gold} Gold!",
        "event_trap": "\n🪤 You stepped on a trap! Took {dmg} HP damage!",
        "event_trap_dead": "\n💀 You died from a trap! Game Over...",
        "event_fountain": "\n⛲ You found a sacred fountain! Restored {heal} HP!",
        "game_over": "\n=========================================\n💀 YOU DIED 💀\nYou collected {gold} Gold before dying.\nGame Over...\n=========================================",
        "continue": "\n(Press Enter to continue...)",
        "quit": "\nTired of adventuring already? Goodbye! 👋"
    }
}

def t(key, **kwargs):
    text = texts[lang].get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text

def print_status(player):
    print("==================================")
    print(t("status", hp=player['hp'], atk=player['atk'], potions=player['potions'], gold=player['gold']))
    print("==================================")

def combat(player, monster):
    print(t("combat_intro", name=monster['name'], hp=monster['hp'], atk=monster['atk']))
    print(t("combat_ctrl"))
    
    while monster['hp'] > 0 and player['hp'] > 0:
        print_status(player)
        key = input("> ").strip().lower()
        
        if key == 'j':
            dmg = random.randint(5, player['atk'])
            monster['hp'] -= dmg
            print(f"\n{t('attack', name=monster['name'], dmg=dmg)}")
        elif key == 'k':
            if player['potions'] > 0:
                heal = random.randint(20, 40)
                player['hp'] = min(100, player['hp'] + heal)
                player['potions'] -= 1
                print(f"\n{t('potion_heal', heal=heal)}")
            else:
                print(f"\n{t('no_potion')}")
                continue
        elif key == 'l':
            if random.random() < 0.5:
                print(f"\n{t('run_success')}")
                return False
            else:
                print(f"\n{t('run_fail')}")
        else:
            print(f"\n❌ Please type J, K, or L")
            continue

        # Monster counter-attack
        if monster['hp'] > 0:
            m_dmg = random.randint(5, monster['atk'])
            player['hp'] -= m_dmg
            print(f"{t('monster_attack', name=monster['name'], dmg=m_dmg)}")
        
        if player['hp'] > 0 and monster['hp'] > 0:
            print(t("combat_intro", name=monster['name'], hp=monster['hp'], atk=monster['atk']))

    if player['hp'] <= 0:
        return "dead"
    elif monster['hp'] <= 0:
        print(f"{t('monster_dead', name=monster['name'])}")
        gold = random.randint(20, 50)
        player['gold'] += gold
        print(f"{t('gold_gain', gold=gold)}")
        return "win"

def main():
    global lang
    
    print("=========================================")
    print("   🗡️ DUNGEON ADVENTURE 🗡️")
    print("=========================================")
    print(t("choose_lang"))
    while True:
        key = input("> ").strip().lower()
        if key == 't':
            lang = 'th'
            break
        elif key == 'e':
            lang = 'en'
            break
        else:
            print(t("invalid_lang"))

    print("\n=========================================")
    print(t("intro1"))
    print(t("intro2"))
    input(t("continue"))

    player = {'hp': 100, 'atk': 15, 'potions': 3, 'gold': 0}
    
    monsters = [
        {'name': 'Goblin', 'hp': 30, 'atk': 10},
        {'name': 'Skeleton', 'hp': 45, 'atk': 12},
        {'name': 'Orc', 'hp': 60, 'atk': 18},
        {'name': 'Dark Knight', 'hp': 80, 'atk': 25}
    ]

    while True:
        print("\n\n------------------------------------")
        print_status(player)
        print(t("controls"))
        
        key = input("> ").strip().lower()
        
        if key == 'q':
            print(f"\n{t('quit')}")
            break
        elif key in ['w', 'a', 's', 'd']:
            pass 
        else:
            print(f"\n{t('invalid_dir')}")
            continue

        event = random.randint(1, 100)
        
        if event <= 50: # Monster 50%
            monster = random.choice(monsters)
            result = combat(player, monster)
            if result == "dead":
                print(t("game_over", gold=player['gold']))
                break
                
        elif event <= 75: # Treasure 25%
            gold_found = random.randint(10, 30)
            player['gold'] += gold_found
            print(t("event_treasure", gold=gold_found))
            input(t("continue"))
            
        elif event <= 90: # Trap 15%
            dmg = random.randint(10, 20)
            player['hp'] -= dmg
            print(t("event_trap", dmg=dmg))
            if player['hp'] <= 0:
                print(t("event_trap_dead"))
                break
            input(t("continue"))
            
        else: # Fountain 10%
            heal = random.randint(15, 30)
            player['hp'] = min(100, player['hp'] + heal)
            print(t("event_fountain", heal=heal))
            input(t("continue"))

if __name__ == "__main__":
    main()
