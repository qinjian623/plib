import sys
import pynotify
import datetime

def main():
    """
    """
    sendmessage("hello", "world, this is just a test, you fucker.");
    pass

def sendmessage(title, message):
    pynotify.init("image")
    notice = pynotify.Notification(title,message,"/usr/share/icons/gnome/48x48/status/appointment-missed.png").show()
    return notice

if __name__ == '__main__':
    main()
