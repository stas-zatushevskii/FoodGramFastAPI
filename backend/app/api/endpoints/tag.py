from fastapi import APIRouter, Depends

from app.schemas.tag import Tag
from app.crud.tag import tag_crud

from app.core.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.get('/tags/',
            response_model=list[Tag],
            response_model_exclude_none=True)
async def get_tags(session: AsyncSession = Depends(get_async_session)):
    all_tags = await tag_crud.get_multi(session)
    return all_tags


@router.get('/tags/{id}/',
            response_model=Tag,
            response_model_exclude_none=True)
async def get_tag(
        id: int,
        session: AsyncSession = Depends(get_async_session),
):
    tag = await tag_crud.get(id, session)
    return tag


@router.post('/tag/',
             response_model=Tag,
             response_model_exclude_none=True)
async def create_tag(
        tag: Tag,
        session: AsyncSession = Depends(get_async_session),
):
    created_tag = await tag_crud.create(tag, session)
    return created_tag
