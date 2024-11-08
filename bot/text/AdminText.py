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
        return 'ты плохо себя вел!\nтебя забанили!\nтеперь ты не можешь лайкать анкеты и твою анкету не видно в поиске'
    def GOT_UNBAN():
        return 'тебя разбанили!\nв следующий раз будь поаккуратнее...'
    def ALREADY_BANNED():
        return 'пользователь уже забанен'
    def BANNED():
        return 'пользователь забанен'
    def NO_COMPLAINS():
        return 'нет жалоб на пользователя'
    def ERROR():
        return 'ошибка'
    def UNBANNED():
        return 'пользователь разбанен'
    def NOT_BANNED():
        return 'пользователь не в черном списке'
    def COMPLAINS_CLEAN():
        return 'жалобы удалены'