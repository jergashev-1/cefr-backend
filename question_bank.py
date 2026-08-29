"""
CEFR Multilevel Speaking imtihoni uchun namunaviy savollar banki.
Bu savollar rasmiy imtihon uslubiga mos ravishda tayyorlangan (har bir
Part uchun mos qiyinlik darajasida), lekin rasmiy imtihon savollarining
o'zi emas — mashq qilish uchun namunaviy savollardir.
(Foydalanuvchining ishlab turgan Speaking botidan olingan, o'zgarishsiz.)
"""
import random

QUESTION_BANK = {
    "1.1": [
        "What is your name and where are you from?",
        "What do you usually do at the weekend?",
        "Do you like your job or studies? Why or why not?",
        "What is your favourite food?",
        "How many people are there in your family?",
        "What time do you usually wake up?",
        "Do you prefer tea or coffee?",
        "What is the weather like today in your city?",
    ],
    "1.2": [
        "Tell me about a place you visited recently.",
        "What did you do last weekend?",
        "Describe your daily routine on a typical working day.",
        "What kind of music do you like listening to, and why?",
        "Have you ever learned a new skill? Tell me about it.",
        "What do you usually do to relax after a busy day?",
        "Describe a memorable meal you had recently.",
        "What are your plans for the next holiday?",
    ],
    "2": [
        "Describe your favourite place to visit and explain why you like it.",
        "Talk about a book or film that made a strong impression on you.",
        "Describe a person who has influenced your life and explain how.",
        "Talk about a skill you would like to learn in the future and why.",
        "Describe a memorable trip you took and explain why it was special.",
        "Talk about the advantages and disadvantages of living in a big city.",
    ],
    "3": [
        "Some people think technology makes our lives easier, while others believe it makes life more complicated. Discuss both views and give your opinion.",
        "Discuss the advantages and disadvantages of remote work compared to working in an office.",
        "Some people believe that social media has a positive effect on society, while others disagree. Discuss both sides and give your own opinion.",
        "Discuss whether governments should invest more in public transport or in building new roads.",
        "Some people think that studying abroad is the best way to learn a language, while others believe you can learn just as well at home. Discuss both views.",
        "Discuss the impact of artificial intelligence on the job market, considering both opportunities and risks.",
    ],
}


def get_random_question(part: str) -> str:
    """Berilgan qism (part) uchun banki dan tasodifiy savol qaytaradi."""
    return random.choice(QUESTION_BANK[part])
