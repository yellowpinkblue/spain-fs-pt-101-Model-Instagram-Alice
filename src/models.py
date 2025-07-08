from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime 

db = SQLAlchemy()

class Users(db.Model):
    __tablename__='users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

     # PROFILE (1 de 4 modelos). --> uselist=False es para forzar a que NO devuelva una lista
    profile: Mapped["Profiles"] = relationship(back_populates="user", uselist=False)        #Este USER se refiere a otro (más abajo)

    # POSTS (relación Uno a Muchos con Users)
    posts: Mapped[list["Post"]] = relationship(back_populates="user")

    # COMMENTS (relación Uno a Muchos con Users)
    comments: Mapped[list["Comment"]] = relationship(back_populates="user")

    # FOLLOWS (relación Muchos a Muchos con Users a través de Follow)
    # follower_id: Usuarios que Sigo (soy el seguidor)
    followed: Mapped[list["Follow"]] = relationship(
        foreign_keys='Follow.follower_id', back_populates="follower"
    )
    # followed_id: Usuarios que Me Siguen (soy el seguido)
    followers: Mapped[list["Follow"]] = relationship(
        foreign_keys='Follow.followed_id', back_populates="followed"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,

            #Profile si es posible acceder a través de serialize. Es un OBJETO. 
            "profile": self.profile.serialize(),
            "posts_count": len(self.posts),
            "comments_count": len(self.comments),
            "followed_count": len(self.followed),
            "followers_count": len(self.followers),



            # do not serialize the password, its a security breach
        }
    

#relacion de uno a uno entre users y profiles ---> 1 de 4 Modelos Instagram. Se crea una nueva class (tabla)
class Profiles(db.Model):
    __tablename__='profiles'
    id: Mapped[int] = mapped_column(primary_key=True)
    bio: Mapped[str] = mapped_column(String(250))
    # conexion a traves de la clave foranea (foreignkey)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))   #Se refiere a ESTE USER, en profile en class users. 
    # relacion con Users
    user: Mapped["Users"] = relationship(back_populates="profile")

    def serialize(self):
        return {
            "id": self.id,
            "bio": self.bio,
            "user_id": self.user_id   
        }


#relacion de 1 a Muchos entre users y post ---> 2 de 4 Modelos Instagram. Se crea una nueva class (tabla)
class Post(db.Model):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    caption: Mapped[str] = mapped_column(String(500)) 
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Clave foránea para el usuario que creó el post
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["Users"] = relationship(back_populates="posts")

    # Comentarios asociados a este post (relación Uno a Muchos con Comment)
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "caption": self.caption,
            "created_at": self.created_at.isoformat(), # Formato ISO para la fecha
            "user_id": self.user_id,
            "user_email": self.user.email, # Accedemos al email del usuario para contexto
            "comments_count": len(self.comments) # Contar los comentarios sin serializarlos todos
        }
    
#relacion de 1 a Muchos entre post y comentarios ---> 3 de 4 Modelos Instagram. Se crea una nueva class (tabla)
class Comment(db.Model):
    __tablename__ = 'comments'
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False) # Usamos Text para comentarios más largos
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Clave foránea para el usuario que hizo el comentario
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["Users"] = relationship(back_populates="comments")

    # Clave foránea para el post al que pertenece el comentario
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Post"] = relationship(back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id,
            "user_email": self.user.email,
            "post_id": self.post_id
        }

#relacion de Muchos a Muchos entre follow y users ---> 4 de 4 Modelos Instagram. Se crea una nueva class (tabla)

class Follow(db.Model):
    __tablename__ = 'follows'
    id: Mapped[int] = mapped_column(primary_key=True)

    # ID del usuario que sigue (el seguidor)
    follower_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # ID del usuario que es seguido
    followed_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relaciones para acceder a los objetos User
    follower: Mapped["Users"] = relationship(
        foreign_keys=[follower_id], back_populates="followed"
    )
    followed: Mapped["Users"] = relationship(
        foreign_keys=[followed_id], back_populates="followers"
    )

    def serialize(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "followed_id": self.followed_id,
            "created_at": self.created_at.isoformat(),
            "follower_email": self.follower.email,
            "followed_email": self.followed.email
        }
