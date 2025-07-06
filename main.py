
import uvicorn
from fast import app


from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)

from apps.health.route import router
app.include_router(router)

from apps.user.route import router
app.include_router(router)

from apps.dish.route import router
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", debug=True, reload=True)