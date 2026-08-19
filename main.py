from fastapi import FastAPI, Request, HTTPException,status
from contextlib import asynccontextmanager
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi import Depends
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from schemas import PostCreate, PostResponse, UserCreate, UserResponse, PostUpdate, UserUpdate
from typing import List
from typing_extensions import Annotated

from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import models
from database import Base, engine, get_db

#Base.metadata.create_all(bind=engine)
@asynccontextmanager
#Startup server
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # shutdown server 
    await engine.dispose()    
app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")
templates = Jinja2Templates(directory="templates")

# posts = [
#     {
#         "id": 1,
#         "author": "Corey Anderson",
#         "title": "FastAPI learning way",
#         "content": "This framework is really useful to learn and implement",
#         "date_posted": "April 20 2025"
#     },
#     {
#         "id": 2,
#         "author": "Kane Williamson",
#         "title": "Ruby on Rails dead nowadays",
#         "content": "This framework is really useful to learn and implement",
#         "date_posted": "May 20 2025"
#     }
# ]


## home
@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
async def home(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Post).options(selectinload(models.Post.author)))
    posts = result.scalars().all()
    return templates.TemplateResponse(
        request,
        "home.html",
        {"posts": posts, "title": "Home"},
    )

## post_page
@app.get("/posts/{post_id}", include_in_schema=False)
async def post_page(request: Request, post_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.Post).options(selectinload(models.Post.author)).where(models.Post.id == post_id),)
    post = result.scalars().first()
    if post:
        title = post.title[:50]
        return templates.TemplateResponse(
            request,
            "post.html",
            {"post": post, "title": title},
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found") 

## user_posts_page
# @app.get("/users/{user_id}/posts", include_in_schema=False, name="user_posts")
# def user_posts_page(
#     request: Request,
#     user_id: int,
#     db: Annotated[Session, Depends(get_db)],
# ):
#     result = db.execute(select(models.User).where(models.User.id == user_id))
#     user = result.scalars().first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found",
#         )

#     result = db.execute(select(models.Post).where(models.Post.user_id == user_id))
#     posts = result.scalars().all()
#     return templates.TemplateResponse(
#         request,
#         "user_posts.html",
#         {"posts": posts, "user": user, "title": f"{user.username}'s Posts"},
#     ) 


@app.get("/users/{user_id}/posts", include_in_schema=False, name="user_posts")
async def user_posts_page(
    request: Request,
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .where(models.Post.user_id == user_id),
    )
    posts = result.scalars().all()
    return templates.TemplateResponse(
        request,
        "user_posts.html",
        {"posts": posts, "user": user, "title": f"{user.username}'s Posts"},
    )





# create a new user in the Database
# @app.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
# def create_user(user:UserCreate, db: Annotated[Session, Depends(get_db)]):
#     result = db.execute(select(models.User).where(models.User.username == user.username),)
#     existing_user = result.scalars().first()

#     if existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="username already exists",
#         )


#     result = db.execute(select(models.User).where(models.User.email == user.email),)
#     existing_email = result.scalars().first()

#     if existing_email:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email already found"
#         )

#     new_user = models.User(
#         username= user.username,
#         email = user.email,
#     )

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)


#     return new_user





@app.post(
    "/api/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.User).where(models.User.username == user.username),
    )
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    result = await db.execute(
        select(models.User).where(models.User.email == user.email),
    )
    existing_email = result.scalars().first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    new_user = models.User(
        username=user.username,
        email=user.email,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# Get a single user from the Databse
# @app.get("/api/users/{user_id}", response_model=UserResponse)
# def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]):

#     result = db.execute(select(models.User).where(models.User.id == user_id),)
#     user = result.scalars().first()

#     if user:
#         return user

#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="User Not Found",
#     )


@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


## get_user_posts
# @app.get("/api/users/{user_id}/posts", response_model=PostResponse)
# def get_user_posts(user_id: int, db: Annotated[Session, Depends(get_db)]):
#     result = db.execute(select(models.User).where(models.User.id == user_id))
#     user = result.scalars().first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found",
#         )

#     result = db.execute(select(models.Post).where(models.Post.user_id == user_id))
#     posts = result.scalars().all()
#     return posts


@app.get("/api/users/{user_id}/posts", response_model=PostResponse)
async def get_user_posts(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .where(models.Post.user_id == user_id),
    )
    posts = result.scalars().all()
    return posts




#########################

# user update using Patch

# @app.patch("/api/users/{user_id}", response_model=UserUpdate)
# def update_user_partial(user_id: int, db: Annotated[Session, Depends(get_db)], user_update: UserUpdate):
#     result = db.execute(select(models.User).where(models.User.id == user_id),)
#     user = result.scalars().first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="No user Found"
#         )
#     if user_update.username is not None and user_update.username != user.username:
#         result = db.execute(select(models.User).where(models.User.username == user_update.username),)
#         existing_user = result.scalars().first()
#         if existing_user:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Username already exists",
#             )


#     if user_update.email is not None and user_update.email != user.email:
#             result = db.execute(select(models.User).where(models.User.email == user_update.email),)
#             existing_email = result.scalars().first()
#             if existing_email:
#                 raise HTTPException(
#                     status_code=status.HTTP_400_BAD_REQUEST,
#                     detail="Email already exists",
#                 )


#     if user_update.username is not None:
#         user.username = user_update.username
#     if user_update.email is not None:
#         user.email = user_update.email

#     if user_update.image_file is not None:
#         user.image_file = user_update.image_file

#     db.commit()
#     db.refresh(user)
#     return user    



@app.patch("/api/users/{user_id}", response_model=UserUpdate)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if user_update.username is not None and user_update.username != user.username:
        result = await db.execute(
            select(models.User).where(models.User.username == user_update.username),
        )
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )
    if user_update.email is not None and user_update.email != user.email:
        result = await db.execute(
            select(models.User).where(models.User.email == user_update.email),
        )
        existing_email = result.scalars().first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    if user_update.username is not None:
        user.username = user_update.username
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.image_file is not None:
        user.image_file = user_update.image_file

    await db.commit()
    await db.refresh(user)
    return user


## delete_user
# @app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
#     result = db.execute(select(models.User).where(models.User.id == user_id))
#     user = result.scalars().first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found",
#         )

#     db.delete(user)
#     db.commit()


@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    await db.delete(user)
    await db.commit()    


        


## get_posts
# @app.get("/api/posts", response_model=List[PostResponse])
# def get_posts(db: Annotated[Session, Depends(get_db)]):
#     result = db.execute(select(models.Post))
#     posts = result.scalars().all()
#     return posts


@app.get("/api/posts", response_model=List[PostResponse])
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


@app.post(
    "/api/posts",
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


@app.get("/api/posts/{post_id}", response_model=PostResponse)
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


@app.put("/api/posts/{post_id}", response_model=PostResponse)
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



@app.patch("/api/posts/{post_id}", response_model=PostResponse)
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


@app.delete("/api/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
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





## StarletteHTTPException Handler
@app.exception_handler(StarletteHTTPException)
async def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
   

    if request.url.path.startswith("/api"):
        return await http_exception_handler(request, exception)

    message = (
            exception.detail
            if exception.detail
            else "An error occurred. Please check your request and try again."
        )

        
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


### RequestValidationError Handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return await request_validation_exception_handler(request, exception) 
    
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "title": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )

