from threading import Thread, Lock
from time import sleep, gmtime, strftime
from queue import Queue
import datetime
import random
import string


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


class Email:
    def __init__(self, from_, to, message):
        self.from_ = from_
        self.to = to
        self.message = message

    def __str__(self):
        return f'from: {self.from_}, to: {self.to}, message: {self.message}'


class EmailHandler:
    def __init__(self, email_queue=Queue()):
        self.email_queue = email_queue
        self.lock_push = Lock()
        self.lock_pop = Lock()

    def push_email(self, email):
        with self.lock_push:
            self.email_queue.put(email)

    def pop_email(self):
        with self.lock_pop:
            while self.email_queue.empty():
                sleep(0.1)
            return self.email_queue.get()


class EmailClient:
    __next_id__ = 0
    lock = Lock()

    def __init__(self):
        with EmailClient.lock:
            self.id = EmailClient.__next_id__
            EmailClient.__next_id__ += 1

    def send_random_messages(self, to, email_handler):
        for i in range(1, random.randint(1, 10)):
            email_handler.push_email(Email(self.id, to, randomword(random.randint(5, 30))))
            sleep(2)


class Mail:
    def __init__(self, name):
        self.name = name

    def process_email(self, email_handler):
        while datetime.datetime.now().time().hour in range(8, 18):
            email = email_handler.pop_email()
            print(f'{strftime("%Y-%m-%d %H:%M:%S", gmtime())} processed email: \'{email}\' by mail: \'{self.name}\'')
            sleep(1)


def main():
    email_handler = EmailHandler()
    mail = Mail('Mail.ru')
    client1 = EmailClient()
    client2 = EmailClient()
    # create threads
    t1 = Thread(target=client1.send_random_messages, args=(client2.id, email_handler))
    t2 = Thread(target=client2.send_random_messages, args=(client1.id, email_handler))
    t3 = Thread(target=mail.process_email, args=(email_handler,))

    # start the threads
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()


if __name__ == '__main__':
    main()
