class AdminText:
    def START():
        return 'админка нефорпензабот v66.6\n команды:\n/ban [id] - бан пользователя\n/unban [id] - разбан пользователя\n/clean - очистить список жалоб\n/assign [id] - назначить админом\n/unassign [id] - разжаловать админа'
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
    def ADMIN_ADDED():
        return 'добавлен новый админ'
    def ADMIN_DELETED():
        return 'админ удален'
    def GOT_ADMIN():
        return 'тебя назначили администратором! будь осторожен...\nвход в админку: /admin'
    def GOT_UNASSIGN():
        return 'ты больше не админ!'