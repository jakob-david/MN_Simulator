import requests


class Telegram:

    chat_id = ""    # Add Chat ID here
    token = ""      # Add bot token here (including the "bot" at the beginning)

    def __init__(self):
        """
        Class that handles the Telegram messages.
        """

        self.message = ""

    def set_message(self, message):
        """
        Sets the message which should be sent by Telegram.
        """

        self.message = message

    def set_chat_id(self, chat_id):
        """
        Sets the chat id.

        :param chat_id: The chat id to which the variable should be set.
        """

        if not isinstance(chat_id, str):
            print("Error: Chat ID must be a string")

        self.chat_id = chat_id

    def send_message(self):
        """
        Sends the message via Telegram.
        """

        first_part = "https://api.telegram.org/" + self.token + "/sendMessage?chat_id="
        second_part = "&text="
        requests.get(first_part + self.chat_id + second_part + self.message)
