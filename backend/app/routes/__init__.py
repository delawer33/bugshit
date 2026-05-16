from fastapi import APIRouter

from app.routes import auth, comments, files, projects, tasks, users, wallet, webhooks, admin

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(wallet.router, prefix="/wallet", tags=["wallet"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
