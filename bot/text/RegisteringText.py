class RegisteringText:
    def START_NO_PROFILE(username):
        return f'привет, {username}, создай анкету'

    def START_HAS_PROFILE():
        return 'у тебя уже есть анкета'

    def CHOOSE_NAME():
        return 'введи свое имя (ну или что-нибудь смешное хз)'
    
    def FAIL():
        return 'что-то пошло не так, попробуй еще раз 0_0'
    
    def CHOOSE_SEX():
        return 'теперь выбери свой гендер или пол или как там это называется'
    
    def CHOOSE_DESCRIPTION():
        return 'напиши описание - чем любишь заниматься, любимые группы, увлечения, все такое'
    
    def CHOOSE_DESCRIPTION_FAIL():
        return 'описание слишком длинное! попробуй сократить, максимум - 128 символов'
    
    def CHOOSE_PHOTO():
        return 'скинь фотку для анкеты'
    
    def PROFILE_SAVE():
        return 'анкета готова! теперь нажми сохранить анкету'
    
    def PROFILE_READY():
        return 'анкета сохранена'

    

