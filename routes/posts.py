## Imports for Posts Router
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import models
from database import get_db
from schemas import PostCreate, PostResponse, PostUpdate

router = APIRouter()

## get_posts
# @app.get("/api/posts", response_model=List[PostResponse])
# def get_posts(db: Annotated[Session, Depends(get_db)]):
#     result = db.execute(select(models.Post))
#     posts = result.scalars().all()
#     return posts


@router.get("", response_model=List[PostResponse])
async def get_posts(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Post).options(selectinload(models.Post.author)),
    )
    posts = result.scalars().all()
    return posts








## create_post
# @app.post(
#     "/api/posts",
#     response_model=PostResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# def create_post(post: PostCreate, db: Annotated[Session, Depends(get_db)]):
#     result = db.execute(select(models.User).where(models.User.id == post.user_id))
#     user = result.scalars().first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found",
#         )

#     new_post = models.Post(
#         title=post.title,
#         content=post.content,
#         user_id=post.user_id,
#     )
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post


@router.post(
    "",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(post: PostCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.User).where(models.User.id == post.user_id),
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    new_post = models.Post(
        title=post.title,
        content=post.content,
        user_id=post.user_id,
    )
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post, attribute_names=["author"])
    return new_post


## get_post
# @app.get("/api/posts/{post_id}", response_model=PostResponse)
# def get_post(post_id: int, db: Annotated[Session, Depends(get_db)]):
#     result = db.execute(select(models.Post).where(models.Post.id == post_id))
#     post = result.scalars().first()
#     if post:
#         return post
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .where(models.Post.id == post_id),
    )
    post = result.scalars().first()
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

## update

# @app.put("/api/posts/{post_id}", response_model=PostResponse)
# def update_post_full(post_id: int, db: Annotated[Session, Depends(get_db)], post_data: PostCreate):

#     result = db.execute(select(models.Post).where(models.Post.id == post_id),)
#     post = result.scalars().first()
#     if not post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail= "No post available",
#         )
#     if post_data.user_id != post.user_id:
#         result = db.execute(select(models.User).where(models.User.id == post_data.user_id),)
#         user = result.scalars().first()
#         if not user:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="User Not Found",
#             )

#     post.title = post_data.title
#     post.content = post_data.content
#     post.user_id = post_data.user_id

#     db.commit()
#     db.refresh(post)
#     return post    


@router.put("/{post_id}", response_model=PostResponse)
async def update_post_full(
    post_id: int,
    post_data: PostCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    if post_data.user_id != post.user_id:
        result = await db.execute(
            select(models.User).where(models.User.id == post_data.user_id),
        )
        user = result.scalars().first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

    post.title = post_data.title
    post.content = post_data.content
    post.user_id = post_data.user_id

    await db.commit()
    await db.refresh(post, attribute_names=["author"])
    return post



# patch post update

# @app.patch("/api/posts/{post_id}", response_model=PostResponse)
# def update_post_partial(post_id: int, db: Annotated[Session, Depends(get_db)], post_data: PostUpdate):
#     result = db.execute(select(models.Post).where(models.Post.id == post_id),)
#     post = result.scalars().first()
#     if not post:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail= "No post available",
#             )

#     update_data = post_data.model_dump(exclude_unset=True)
#     for field, value in update_data.items():
#         setattr(post, field, value)


#     db.commit()
#     db.refresh(post)
#     return post  



@router.patch("/{post_id}", response_model=PostResponse)
async def update_post_partial(
    post_id: int,
    post_data: PostUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    update_data = post_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)

    await db.commit()
    await db.refresh(post, attribute_names=["author"])
    return post


# Delete Posts

## get_post
# @app.delete("/api/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(post_id: int, db: Annotated[Session, Depends(get_db)]):
#     result = db.execute(select(models.Post).where(models.Post.id == post_id))
#     post = result.scalars().first()
#     if not post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail= "No post available",
#                 )
#     db.delete(post)
#     db.commit()


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    await db.delete(post)
    await db.commit()    
