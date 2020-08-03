from locust import HttpLocust, TaskSet, task

def index(l):
    l.client.get("/")

def stats(l):
    l.client.get("/edit/1")

class UserTasks(TaskSet):
    # one can specify tasks like this
    tasks = [index, stats]

    # but it might be convenient to use the @task decorator
    @task
    def page404(self):
        self.client.get("/edit/2")

class WebsiteUser(HttpLocust):
    """
    Locust user class that does requests to the locust web server running on localhost
    """
    host = "http://127.0.0.1:5000"
    min_wait = 2000
    max_wait = 5000
    stop_timeout = 10
    task_set = UserTasks


# from locust import Locust, TaskSet, task
#
# class MyTaskSet(TaskSet):
#     @task
#     def my_task(self):
#         print "executing my_task"
#
# class MyLocust(Locust):
#     task_set = MyTaskSet
#     min_wait = 5000
#     max_wait = 15000
