from asyncio import Queue

from app.tap_robotics.hamster_kombat.schemas import HamsterTask

task_queue: Queue[HamsterTask] = Queue()
