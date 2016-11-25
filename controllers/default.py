# -*- coding: utf-8 -*-
from rqredis import RqConn

def index():
    response.view = 'default/rq.html'
    return dict()

def start_worker():
    import subprocess
    rq = RqConn()
    id = len(rq.list_workers())
    worker = request.folder + '/private/web2py-rq.py'
    p = subprocess.Popen(['python', worker, 'high-'+str(id), 'normal-'+str(id), 'low-'+str(id)])
    stdout, stderr = p.communicate()
    return p.poll()

def stop_worker():
  #kill -SIGTERM
  worker = request.args(0)
  pid = worker.split('.')[1]
  import subprocess
  p= subprocess.Popen(['kill', '-SIGTERM', pid])
  stdout, stderr = p.communicate()
  return p.poll()

def jobs():
    queue = request.args(0) or "failed"
    rq = RqConn()
    return response.json({'jobs':rq.list_jobs(queue)})

def cancel_job():
    job_id = request.args(0) or None
    rq = RqConn()
    return rq.cancel_job(job_id)

def requeue_job():
    job_id = request.args(0) or None
    rq = RqConn()
    return rq.requeue_job(job_id)

def queues():
    rq = RqConn()
    return response.json({'queues':rq.list_queues()})

def workers():
    rq = RqConn()
    return response.json({'workers':rq.list_workers()})

def empty_queue():
    queue = request.args(0) or None
    rq = RqConn()
    return rq.empty_queue(queue)

def test_queue():
    # Test the job sleep in a randon queue
    import time, random
    rq = RqConn()
    queues = rq.list_queues()
    random_queue= random.randint(0, len(queues)-1)
    return rq.queue_job(time.sleep, queues[random_queue]['name'], 180, 10)


def test_fail_queue():
    # Test the job sleep in a randon queue
    import time, random
    rq = RqConn()
    queues = rq.list_queues()
    random_queue= random.randint(0, len(queues)-1)
    return rq.queue_job(time.sleep, queues[random_queue]['name'], 10, 22)

def requeue_failed():
    rq = RqConn()
    failed_jobs=rq.list_jobs('failed')
    for job in failed_jobs:
        rq.requeue_job(job['id'])
    return 0
