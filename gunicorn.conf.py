wsgi_app = "app:app"
workers = 1
bind = ["0.0.0.0:80"]
worker_class = "uvicorn.workers.UvicornH11Worker"
proxy_protocol = True
accesslog = "-"
