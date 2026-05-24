## ユーザ情報更新時の権限判定について

ユーザ情報の更新 (`update_user()`) を許容する条件は以下である。

```
アプリ管理者であるとき
または
更新対象が自分であるとき
```

すなわち、以下の条件であれば更新を許可する。

```python
is_admin or is_owner
```

早期例外を発生させる場合は、この許可条件を否定して考える。

```python
not (is_admin or is_owner)
```

ド・モルガンの法則より、これは以下と同じである。

```python
not is_admin and not is_owner
```

したがって、以下の場合には`PermissionDeniedException`を発生させる。

```
アプリ管理者ではない
かつ
更新対象が自分ではない
```

実装例は以下である。

```python
is_admin = current_user.is_admin
is_owner = current_user.id == target.id

if not is_admin and not is_owner:
    raise PermissionDeniedException()
```

## ユーザ情報更新時のusernameの重複判定について

ユーザ情報の更新 (`update_user()`) では、`username`が他人のものと重複してはいけない。
ただし、自分自身が現在使っている `username` をそのまま送った場合は許可する。
そのため、`username`が更新データに含まれている場合だけ、既存ユーザーを検索する。

```python
if "username" in update_data:
    existing_user = repository.get_by_username(update_data["username"])
```

既存ユーザーが存在し、かつそのユーザーが自分自身ではない場合は、
`UserAlreadyExistsException` を発生させる。

```python
if existing_user and existing_user.id != target.id:
    raise UserAlreadyExistsException()
```
