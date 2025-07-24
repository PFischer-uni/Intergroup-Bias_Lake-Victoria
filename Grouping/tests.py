from . import *

class PlayerBot(Bot):
    def play_round(self):
        yield Instructions
        yield Demographics, dict(gender='Divers', age=0, religion='Andere', fish=self.player.id_in_group % 2, prime='Beep boob I am a bot')

