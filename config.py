from prettytable import PrettyTable as pt
from aiogram.utils.markdown import link



template_1 = """
🎮 *Rust*   🏷 [{}]({}).

*buff163 ➡️ rust*      — {}%.
*buff163 ➡️ steam* — {}% (-30%).

🔗 [Buff163]({})     🧮 *{}*
🛒:     
*$:* {}
*₽:* {}

♻️:    
*$:* {}
*₽:* {}
"""

template_2 = """
🔗 [Rust]({})     🧮 *{}*   *Покупок:* *{}*
*MIN; AVG; MAX*
*$:* {}; {}; {}
*₽:* {}; {}; {}

🛒:
*$:* {}
*₽:* {}

*AUTOBUY*: 🧮 {}.
*$:* {}
*₽:* {}
"""

template_3 = """
🔗 *Rust*
⛔ *Нет на маркете.*
"""

template_4 = """
🔗 [Steam]({})

🛒:
*$:* {}
*₽:* {}
"""


a = """
Autobuy:    🧮 4
₽: 15.5, 15.49, 5, 0.5
$: 0.21, 0.21, 0.09, 0.005

Steam🔗 (http://c.cc/):    🧮 6793   Покупок(24h): 634
🛒: 
₽: 29,90(1), 30,95(1), 31,05(1), 33,96(40), 34,18(2)
$: 0.45(1), 0.46(1), 0.46(1), 0.47(40), 0.48(2)

📈*{}%*
"""





text_message = """
🎮 Rust.     buff➡️rust.tm.
🏷 {}.   🔗{}, {}, {}.

📈 {}%. {}$. {}₽.

🛒 Buff:
💵 {}.

🛒 Tm:
💵 {}.
avr: {}.
buys: {}.
"""

cap_message = """
🎮 Rust.     buff➡️rust.tm.
🏷 {}.   🔗buff, steam, tm.
"""

buff_part = """
🛒 Buff:
💵 {}.
"""

tm_part = """
🛒 Tm:
"""