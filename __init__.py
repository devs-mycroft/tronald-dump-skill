from mycroft import MycroftSkill, intent_file_handler


class TronaldDump(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('dump.tronald.intent')
    def handle_dump_tronald(self, message):
        self.speak_dialog('dump.tronald')


def create_skill():
    return TronaldDump()

