#!/usr/bin/env python3
import os
import sys
import socket


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flute.settings.production")
    HOSTNAME = socket.gethostname()

    if "webfaction.com" in HOSTNAME:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    else:
        print("ERROR: You should use manage.py instead of manage-production.py for local development")
        sys.exit()
