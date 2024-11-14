from sqlmodel.ext.asyncio.session import AsyncSession
from schema.todo import TodoCreateSchema
from models.TodoModel import Todo
from sqlmodel import select


class TodoService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_todos(self):
        statement = select(Todo).order_by(Todo.created_at)
        result = await self.session.exec(statement)
        return result.all()

    async def create_todo(self, todo_data: TodoCreateSchema):
        new_todo = Todo(**todo_data.model_dump())
        self.session.add(new_todo)
        await self.session.commit()
        return new_todo

    async def update_todo(self, todo_id: int, resource_path: str):
        statement = select(Todo).where(Todo.id == todo_id)
        result = await self.session.exec(statement)
        todo = result.first()
        todo.resources = resource_path
        await self.session.commit()
        return todo

    async def delete_todo(self, todo_id: int):
        statement = select(Todo).where(Todo.id == todo_id)
        result = await self.session.exec(statement)
        todo = result.first()
        await self.session.delete(todo)
        await self.session.commit()
