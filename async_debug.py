import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.core.asgi:application",
        host="127.0.0.1",
        port=8000,
        reload=True,
        loop="asyncio",
        http="httptools",
        lifespan="off",
        interface="asgi3",
    )
