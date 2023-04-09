import threading as th


def sctn():
    print("SECTION FOR LIFE")


th.Timer(5.0, sctn).start()

print("Exit Program")