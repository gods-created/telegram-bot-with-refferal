#!/bin/sh

python main.py &
celery -A modules.tasks:app worker --concurrency=10 --queues=high_priority &
celery -A modules.tasks:app flower
