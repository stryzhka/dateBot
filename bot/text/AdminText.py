class AdminText:
    def START():
        return 'админка нефорпензабот v66.6'
    def FAIL():
        return 'ошибка доступа'
    def INPUT():
        return 'введи сообщение'
    def SEND_FAIL(id):
        return f'не отправилось пользователю {id}'
    def MSG_TO_ALL(text):
        return f"""
    ⚠️⚠️⚠️
    {text}
⚠️⚠️⚠️
    """
    def COMPLAINS_END():
        return 'просмотрены все жалобы'
    def COMPLAIN_ADDED(user):
        return f'{user} забанен'
    def GOT_BAN():
        return f'тебя забанили\nты плохо себя вел :('