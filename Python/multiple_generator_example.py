import asyncio
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def subloop1(queue):
    for i in range(1, 10):
        await asyncio.sleep(1)
        print(f"1번 : {i}")
        await queue.put(i)

async def subloop2(queue):
    for i in range(1, 3):
        await asyncio.sleep(3)
        print(f"2번 : {i}")
        await queue.put(i)

async def mainloop():
    print("Starting")
    queue = asyncio.Queue()

    # Task 동시 실행을 위해 create_task
    task1 = asyncio.create_task(subloop1(queue))
    task2 = asyncio.create_task(subloop2(queue))

    while True:
        done, pending = await asyncio.wait(
            [task1, task2], return_when=asyncio.FIRST_COMPLETED # Future가 완료 혹은 취소되면 반환
        )
        
    
        for task in done:
            result = await task
            print(f"Received value: {result}")

        if not pending:
            break


if __name__ == "__main__":
    loop = asyncio.get_event_loop() # Thread에 설정된 이벤트 루프 get or create
    result = loop.run_until_complete(mainloop()) # 이벤트 루프 실행
    loop.close()
