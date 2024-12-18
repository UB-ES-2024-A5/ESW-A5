""" Main API routes definition """
from fastapi import APIRouter, FastAPI, HTTPException
from app.api.routes import login, users, utils, accounts, books, wishlists, reviews, followers, search, forums

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(wishlists.router, prefix="/wishlists", tags=["wishlists"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(followers.router, prefix="/followers", tags=["followers"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(forums.router, prefix="/forums", tags=["forums"])

