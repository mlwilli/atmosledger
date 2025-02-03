from __future__ import annotations

from redis import Redis
from rq import Queue, Worker

from atmosledger.settings import settings


def main() -> None:
    redis_conn = Redis.from_url(settings.redis_url)
    queue = Queue(settings.rq_queue, connection=redis_conn)

    worker = Worker([queue], connection=redis_conn)
    worker.work(with_scheduler=False)


if __name__ == "__main__":
    main()
