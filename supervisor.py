   [supervisord]
   nodaemon=true
   
   [program:webserver]
   command=python main.py
   autostart=true
   autorestart=true
