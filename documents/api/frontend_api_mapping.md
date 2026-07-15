# Frontend API Mapping

## `/`

- [ ] GET `/articles`

## `/articles/create`

- [ ] GET `/tags`
- [ ] Submit: POST `/articles`

## `/articles/{article_id}`

- [ ] GET `/articles/{article_id}`
- [ ] GET `/articles/{article_id}/comments`
- [ ] Like: POST `/articles/{article_id}/like`
- [ ] Unlike: DELETE `/articles/{article_id}/unlike`
- [ ] Submit (add comment): POST `/articles/{article_id}/comments`

## `/articles/{article_id}/update`

- [ ] GET `/articles/{article_id}`
- [ ] GET `/tags`
- [ ] Submit: PATCH `/articles/{article_id}`

## `/articles/{article_id}/delete`

- [ ] Yes: DELETE `/articles/{article_id}`
- [ ] No: Redirect to `/users/me`

## `/users/me`

- [ ] GET `/users/me`
- [ ] GET `/users/me/articles`
- [ ] GET `/users/me/comments`

## `/users/me/update`

- [ ] GET `/users/me`
- [ ] Submit: PATCH `/users/me`

## `/users/me/delete`

- [ ] Yes: DELETE `/users/me`
- [ ] No: Redirect to `/users/me`

## `/users/{user_id}`

- [ ] GET `/users/{user_id}`
- [ ] GET `/users/{user_id}/articles`

## `/comments/{comment_id}/update`

- [ ] GET `/comments/{comment_id}`
- [ ] Submit: PATCH `/comments/{comment_id}`

## `/comments/{comment_id}/delete`

- [ ] Yes: DELETE `/comments/{comment_id}`
- [ ] No: Redirect to `/users/me`

## `/auth/login`

- [ ] Submit: POST `/auth/login`

## `/auth/signup`

- [ ] Submit: POST `/users`

## Common

- [ ] If the authenticated request returns `401 Unauthorized`, try to refresh the access token -> POST `/auth/refresh`
- [ ] If token refresh succeeds, retry the original request
- [ ] If token refresh fails, redirect to `/auth/login`
- [ ] Logout: POST `/auth/logout`
