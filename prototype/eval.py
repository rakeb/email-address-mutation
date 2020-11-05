# def start_(shadow_list):
#     pass
#
#
# if __name__ == '__main__':
#     shadow_list = ['rakeb_123@gmail.com', 'rakeb_4565@gmail.com', 'rakeb_64654@gmail.com', 'rakeb_9845@gmail.com',
#                    'rakeb_94567@gmail.com', 'rakeb_9645@gmail.com', 'rakeb_92145@gmail.com', 'rakeb_9658@gmail.com',
#                    'rakeb_253495@gmail.com', 'rakeb_33568@gmail.com']
#     start_(shadow_list)
import threading
import time
from apscheduler.schedulers.background import BackgroundScheduler

REFRESH_INTERVAL = 3600  # seconds
s = 10
s = 20
s = 30
s = 50
# s = 100


scheduler = BackgroundScheduler()
scheduler.start()

scheduled_shadow_id = 0

from random import randint


def main():
    # Call our function the first time
    myFunction()

    # then every 60 seconds after that.
    scheduler.add_job(myFunction, 'interval', seconds=REFRESH_INTERVAL)

    # main loop
    while True:
        time.sleep(1)


def myFunction():
    global scheduled_shadow_id, s
    scheduled_shadow_id = randint(0, s)
    # current_shadow_id = current_shadow_id + 1
    print("Scheduled shadow ID: %d" % scheduled_shadow_id)


def start_():
    s_list = [10, 20, 30, 50, 100]
    # t_list = [7200, 3600, 1800, 600, 300, 60]
    t_list = [6, 5, 4, 3, 2, 1]
    global scheduled_shadow_id, s, REFRESH_INTERVAL

    for t in t_list:
        REFRESH_INTERVAL = t
        with open('eval.txt', 'a') as file:
            file.write(str(REFRESH_INTERVAL))
            file.write('\t')
            file.close()
        for s_ in s_list:
            s = s_
            i = 0
            print("Mutation Time: %d, Number of shadow email: %d" % (REFRESH_INTERVAL, s))
            limit = 1000
            avg_iteration = 0
            while True:
                iteration = 1
                while True:
                    current_shadow_id = randint(0, 2147483647)
                    # print("current shadow id: %d", current_shadow_id)
                    if current_shadow_id == scheduled_shadow_id:
                        avg_iteration += iteration
                        # break
                        # print("A hit after: %d iteration, total iteration: %d. Current Shadow ID: %d, Found shadow ID: %d "
                        #       "where i: %d" % (iteration, avg_iteration, current_shadow_id, scheduled_shadow_id, i))
                        break
                    iteration += 1
                    # time.sleep(.2)

                i += 1
                if i > limit:
                    break
            print("avg iteration: %d" % int(avg_iteration / limit))
            with open('eval.txt', 'a') as file:
                file.write(str(int(avg_iteration / limit)))
                file.write('\t')
                file.close()
        with open('eval.txt', 'a') as file:
            # file.write(str(REFRESH_INTERVAL))
            file.write('\n')
            file.close()

        print('Will wait for: %d' % REFRESH_INTERVAL)
        time.sleep(REFRESH_INTERVAL)
        # with open()


def start_new():
    # s_list = [10, 20, 30, 50, 100]
    # t_list = [7200, 3600, 1800, 600, 300, 60]
    # t_list = [6, 5, 4, 3, 2, 1]
    global scheduled_shadow_id, s, REFRESH_INTERVAL

    limit = 1000
    avg_iteration = 0
    i = 0
    while True:
        iteration = 1
        while True:
            current_shadow_id = randint(0, 1000)
            # print("current shadow id: %d", current_shadow_id)
            if current_shadow_id == scheduled_shadow_id:
                avg_iteration += iteration
                # break
                # print("A hit after: %d iteration, total iteration: %d. Current Shadow ID: %d, Found shadow ID: %d "
                #       "where i: %d" % (iteration, avg_iteration, current_shadow_id, scheduled_shadow_id, i))
                break
            iteration += 1
            # time.sleep(.2)

        i += 1
        if i > limit:
            break
    print("avg iteration: %d" % int(avg_iteration / limit))


if __name__ == "__main__":
    client_handler = threading.Thread(
        target=main,
        # without comma you'd get a... TypeError:
        # handle_client_connection() argument after
        # * must be a sequence, not _socketobject
        # args=(thunderbird_client_socket, gmail_client,)
    )
    client_handler.setDaemon(True)
    client_handler.start()
    start_new()
