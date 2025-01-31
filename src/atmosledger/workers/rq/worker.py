from __future__ import annotations

import os

from redis import Redis
from rq import Connection, Queue, Worker

from atmosledger.settings import settings


def main() -> None:
    # Ensure src-layout works when running as a module with PYTHONPATH=src (recommended for dev)
    redis_url = settings.redis_url
    queue_name = settings.rq_queue

    conn = Redis.from_url(redis_url)

    with Connection(conn):
        q = Queue(queue_name)
        worker = Worker([q])
        worker.work()


if __name__ == "__main__":
    main()
