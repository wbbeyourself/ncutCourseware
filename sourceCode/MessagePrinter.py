from Color import *


class MessagePrinter:

    colorer = Color()

    @staticmethod
    def print_errormessage(message):
        print ''
        print ''
        MessagePrinter.colorer.print_red_text(message)
        print ''
        print ''

    @staticmethod
    def print_warningmessage(message):
        print ''
        print ''
        MessagePrinter.colorer.print_blue_text(message)
        print ''
        print ''

    @staticmethod
    def print_promptmessage(message):
        print ''
        print ''
        MessagePrinter.colorer.print_green_text(message)
        print ''
        print ''

    @staticmethod
    def print_process_info(message):
        print ''
        print ''
        print message
        print ''
        print ''
