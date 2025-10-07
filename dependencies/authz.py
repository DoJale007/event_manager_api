from dependencies.authn import authenticated_user
from fastapi import Depends, HTTPException, status
from typing import Annotated


def has_roles(roles):
    def check_role(user: Annotated[any, Depends(authenticated_user)]):
        if not user["role"] in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access Denied!",
            )

    return check_role


permissions = [
    {
        "role": "admin",
        "permissions": [
            "post_event",
            "get_events",
            "get_event",
            "put_event",
            "delete_event",
            "delete_user",
            "put_user",
        ],
    },
    {
        "role": "host",
        "permissions": [
            "post_event",
            "get_events",
            "get_event",
            "put_event",
            "delete_event",
        ],
    },
    {
        "role": "guest",
        "permissions": [
            "get_events",
            "get_event",
        ],
    },
]
