from src.services.ai_engine import AIEngine

engine = AIEngine()

print("Вопрос: Как платить?")
print("Ответ:", engine.get_answer("Как я могу оплатить ваши услуги?"))

print("\nВопрос: Какая погода в Москве?")
print("Ответ:", engine.get_answer("Какая сейчас погода в Москве?"))