import uvicorn
from app import app

app: app


async def main():
    config = uvicorn.Config("main:app", port=8000, log_level="info", workers=4)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    # asyncio.run(main())
    config = uvicorn.Config("main:app", port=8000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    server.run()
