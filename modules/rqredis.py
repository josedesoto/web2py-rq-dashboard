#from redis import Redis
from redis import Redis
from rq import Queue, Worker, Connection
from rq import cancel_job, requeue_job, get_failed_queue
from gluon.html import URL
from gluon.globals import current
import thread
#from gluon import *

locker = thread.allocate_lock()

def RqConn(*args, **vars):
    locker.acquire()
    try:
        instance_name = 'rq_' + current.request.application
        if not hasattr(RqConn, instance_name):
            setattr(RqConn, instance_name, Rq())
        return getattr(RqConn, instance_name)
    finally:
        locker.release()


class Rq(object):
    def __init__(self): 
      self.redis_conn = Redis('localhost', 6379)

    def list_queues(self):
	 with Connection(self.redis_conn):
	  l=[]
	  if len(get_failed_queue().jobs) > 0:
	     l.append({
		'worker': "N/A",
		'name': 'failed',
		'jobs': len(get_failed_queue().jobs),
		'link': URL("admin", "jobs", args=["failed"])})
	     
	  for w in Worker.all():
	    for q in w.queues:
	      l.append({
		'worker': w.name,
		'name': q.name,
		'jobs': q.count,
		'link': URL("admin", "jobs", args=[q.name])})
	 
	  return l
      
    
    def list_workers(self):
	with Connection(self.redis_conn):
	  l=[]
	  for w in Worker.all():
	    l.append({
	      'name': w.name,
              'state': w.get_state(),
              'queues': [q.name for q in w.queues]})
	  return l
	
	
    def list_jobs(self, queue="default"):
	with Connection(self.redis_conn):
	  '''Response a json with the jobs  and the name queue'''
	  q = Queue(queue)
	  l=[]
	  for j in q.jobs:
	      l.append({
	      'id': j.id,
              'created_at': j.created_at,
              'enqueued_at': j.enqueued_at,
              'ended_at': j.ended_at,
              'origin':j.origin,
              'result': j._result,
              'exc_info': j.exc_info,
              'description': j.description})
	  return l

    def get_queue(self, name='default', timeout=180):
      with Connection(self.redis_conn):
        return Queue(name, default_timeout=timeout)
      
    def queue_job(self, function, queue='default', timeout=180, *args, **kwargs):
        return self.get_queue(queue, timeout).enqueue(function, *args, **kwargs)
      
    def requeue_job(self, job_id):
      with Connection(self.redis_conn):
        try:
            requeue_job(job_id)
            status = True
        except:
            status = False
        return status
    
    def cancel_job(self, job_id):
      with Connection(self.redis_conn):
        try:
            cancel_job(job_id)
            status = True
        except:
            status = False
        return status
      
    def empty_queue(self, queue):
      with Connection(self.redis_conn):
        q = Queue(queue)
        return q.empty()
      
     