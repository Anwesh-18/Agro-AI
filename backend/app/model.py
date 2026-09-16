from datetime import datetime,timezone

from sqlalchemy import String,Integer,Float,DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    username: Mapped[str] = mapped_column(String(50),unique=True,nullable=False,index=True)
    first_name: Mapped[str] = mapped_column(String(50),nullable=False)
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50),nullable=False,unique=True,index=True)
    password_hash: Mapped[str] = mapped_column(String(255),nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc),nullable=False)
    predictions: Mapped[list["Prediction"]] = relationship(back_populates="user",cascade="all, delete-orphan")

class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,nullable=False)
    nitrogen: Mapped[float] = mapped_column(Float,nullable=False)
    phosphorus: Mapped[float] = mapped_column(Float,nullable=False)
    potassium: Mapped[float] = mapped_column(Float,nullable=False)
    temperature: Mapped[float] = mapped_column(Float,nullable=False)
    humidity: Mapped[float] = mapped_column(Float,nullable=False)
    ph: Mapped[float] = mapped_column(Float,nullable=False)
    rainfall: Mapped[float] = mapped_column(Float,nullable=False)

    Predicted_crop: Mapped[str] = mapped_column(String(100),nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=lambda:datetime(timezone.utc),nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    user: Mapped["User"] = relationship(back_populates="predictions")