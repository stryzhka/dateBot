class MatchesText:
    def NO_LIKES():
        return 'нет симпатий :('
    def SENT_MATCH(username):
        return f'@{username} начинай общаться!'
    def GOT_MATCH(username):
        return f'на твою симпатию ответил @{username}, начинай общаться!'
    def END_LIKES():
        return 'больше нет симпатий'