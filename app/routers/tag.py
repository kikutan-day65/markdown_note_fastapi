from fastapi import APIRouter, status

from app.api.deps import TagServiceDep
from app.models.tag import Tag
from app.schemas.tag import TagSummary

router = APIRouter(tags=["tags"])


@router.get(
    "",
    response_model=list[TagSummary],
    status_code=status.HTTP_200_OK,
    name="list_tags",
)
def list_tags(service: TagServiceDep) -> list[Tag]:
    return service.list_tags()
