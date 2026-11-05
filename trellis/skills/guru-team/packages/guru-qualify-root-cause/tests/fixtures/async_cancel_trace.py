"""One local job with a normal cancellation between enqueue and consumption."""
import asyncio
import json

async def main():
    queue=asyncio.Queue()
    cancelled=False
    worker_finished=asyncio.Event()
    release_consumer=asyncio.Event()
    events=[]
    def record(event, **fields):
        events.append({'sequence':len(events), 'job':'job17', 'event':event, **fields})
    async def worker():
        record('worker_flag_read', cancelled=cancelled)
        if not cancelled:
            await queue.put({'job':'job17','result':42})
            record('queue_enqueue')
        worker_finished.set()
    async def consumer():
        await release_consumer.wait()
        result=await queue.get()
        record('queue_dequeue', cancelled=cancelled)
        record('publish', result=result['result'])
    work=asyncio.create_task(worker())
    consume=asyncio.create_task(consumer())
    await worker_finished.wait()
    cancelled=True
    record('cancel_ack', cancelled=cancelled)
    release_consumer.set()
    await asyncio.gather(work,consume)
    print(json.dumps({'events':events},indent=2))

asyncio.run(main())
