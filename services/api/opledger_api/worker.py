from rq import Worker

from opledger_api.config import get_settings
from opledger_api.report_jobs import get_redis_connection


def main() -> None:
    settings = get_settings()
    worker = Worker(
        [settings.report_queue_name],
        connection=get_redis_connection(settings),
    )
    worker.work()


if __name__ == "__main__":
    main()
