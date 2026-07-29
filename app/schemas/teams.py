from datetime import datetime, timezone

from pydantic import BaseModel, Field


class TeamBase(BaseModel):
    full_name: str = Field(..., description="Full name of the team member")
    email: str = Field("contact@pytogo.org",
                       description="Email address of the team member")
    role: str = Field(..., description="Role of the team member in the team")
    bio: str | None = Field(
        None, description="Short biography of the team member")
    photo_url: str | None = Field(
        None, description="URL to the photo of the team member")
    social_links: dict | None = Field(
        None, description="Social media links of the team member")
    is_volunteer: bool = Field(
        False, description="Indicates if the team member is a volunteer")
    is_active: bool = Field(
        True, description="Indicates if the team member is currently active")
    position: int | None = Field(
        None, description="Position or order of the team member in the list")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))


class TeamCreate(TeamBase):
    pass


class TeamUpdate(TeamBase):
    full_name: str | None = Field(
        None, description="Full name of the team member")
    email: str | None = Field(
        None, description="Email address of the team member")
    role: str | None = Field(
        None, description="Role of the team member in the team")
    bio: str | None = Field(
        None, description="Short biography of the team member")
    photo_url: str | None = Field(
        None, description="URL to the photo of the team member")
    social_links: dict | None = Field(
        None, description="Social media links of the team member")
    is_volunteer: bool | None = Field(
        None, description="Indicates if the team member is a volunteer")
    is_active: bool | None = Field(
        None, description="Indicates if the team member is currently active")
    position: int | None = Field(
        None, description="Position or order of the team member in the list")

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))


class TeamMemberResponse(TeamBase):
    full_name: str = Field(..., description="Full name of the team member")
    role: str = Field(..., description="Role of the team member in the team")
    bio: str | None = Field(
        None, description="Short biography of the team member")
    photo_url: str | None = Field(
        None, description="URL to the photo of the team member")
    social_links: dict | None = Field(
        None, description="Social media links of the team member")
    is_volunteer: bool = Field(
        False, description="Indicates if the team member is a volunteer")
    is_active: bool = Field(
        True, description="Indicates if the team member is currently active")
    position: int | None = Field(
        None, description="Position or order of the team member in the list")
