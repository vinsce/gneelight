import threading


def run_in_thread(target, **kwargs):
    thread = threading.Thread(target=target, kwargs=kwargs)
    thread.daemon = True
    thread.start()
