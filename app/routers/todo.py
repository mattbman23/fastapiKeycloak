from fastapi import APIRouter, HTTPException, Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from services.todoService import TodoService
from schema.todo import TodoCreateSchema
from utils.db import db_session
from http import HTTPStatus

router = APIRouter(prefix="/todo")


@router.get("/")
async def get_all_todos(session: AsyncSession = Depends(db_session)):
    todos = await TodoService(session).get_all_todos()
    return todos


@router.post("/", status_code=HTTPStatus.CREATED)
async def create_todo(
    todo_data: TodoCreateSchema,
    request: Request,
    session: AsyncSession = Depends(db_session),
):
    # check if user has admin role access
    if "admin" not in request.state.user_data.get("realm_access", {}).get("roles", []):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid access: Not enough permission",
        )

    new_todo = await TodoService(session).create_todo(todo_data)
    return new_todo
