import uuid

from fastapi import APIRouter, status

from app.api.deps import CommentServiceDep, CurrentActiveUserDep
from app.models.comment import Comment
from app.schemas.comment import CommentPublic, CommentUpdate

router = APIRouter(tags=["comments"])


@router.get(
    "/{comment_id}",
    response_model=CommentPublic,
    status_code=status.HTTP_200_OK,
    name="retrieve_comment",
)
def retrieve_comment(comment_id: uuid.UUID, service: CommentServiceDep) -> Comment:
    return service.retrieve_comment(comment_id=comment_id)


@router.patch(
    "/{comment_id}",
    response_model=CommentPublic,
    status_code=status.HTTP_200_OK,
    name="update_comment",
)
def update_comment(
    current_user: CurrentActiveUserDep,
    comment_id: uuid.UUID,
    comment_data: CommentUpdate,
    service: CommentServiceDep,
) -> Comment:
    return service.update_comment(
        user=current_user, comment_id=comment_id, comment_data=comment_data
    )


@router.delete(
    "/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, name="delete_comment"
)
def delete_comment(
    current_user: CurrentActiveUserDep,
    comment_id: uuid.UUID,
    service: CommentServiceDep,
) -> None:
    return service.delete_comment(user=current_user, comment_id=comment_id)
