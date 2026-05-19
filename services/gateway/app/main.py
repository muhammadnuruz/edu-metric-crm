from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(
        base_url=settings.BACKEND_URL,
        timeout=30.0,
    )
    yield
    await app.state.http_client.aclose()


app = FastAPI(
    title="EduMetric Grant Management Gateway",
    description="API Gateway for PDP University Grant Management System",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "gateway"}


@app.get("/health/backend")
async def backend_health(request: Request):
    try:
        client: httpx.AsyncClient = request.app.state.http_client
        resp = await client.get("/api/v1/auth/users/me/")
        return {"status": "reachable", "backend_status": resp.status_code}
    except httpx.RequestError:
        return JSONResponse(
            {"status": "unreachable", "detail": "Backend service is not available"},
            status_code=503,
        )


async def _proxy(request: Request, path: str) -> Response:
    client: httpx.AsyncClient = request.app.state.http_client
    url = f"/api/v1/{path}"

    headers = dict(request.headers)
    headers.pop("host", None)

    body = await request.body()

    try:
        resp = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=body,
            params=dict(request.query_params),
        )
        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers=dict(resp.headers),
        )
    except httpx.RequestError as e:
        return JSONResponse(
            {"detail": f"Backend unavailable: {str(e)}"},
            status_code=503,
        )


@app.api_route(
    "/api/v1/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
async def proxy_to_backend(request: Request, path: str):
    return await _proxy(request, path)


@app.api_route(
    "/api/schema/{path:path}",
    methods=["GET"],
)
async def proxy_schema(request: Request, path: str):
    client: httpx.AsyncClient = request.app.state.http_client
    url = f"/api/schema/{path}" if path else "/api/schema/"
    resp = await client.get(url)
    return Response(content=resp.content, status_code=resp.status_code, headers=dict(resp.headers))


@app.api_route(
    "/api/docs/{path:path}",
    methods=["GET"],
)
async def proxy_docs(request: Request, path: str):
    client: httpx.AsyncClient = request.app.state.http_client
    url = f"/api/docs/{path}" if path else "/api/docs/"
    resp = await client.get(url)
    return Response(content=resp.content, status_code=resp.status_code, headers=dict(resp.headers))
