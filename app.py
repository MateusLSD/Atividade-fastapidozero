from fastapi import FastAPI, HTTPException, status

from schemas import User, UserCreate, UserUpdate

app = FastAPI(title="API de Usuários", version="0.1.0")

_users: dict[int, dict[str, object]] = {}
_next_id = 1


def _model_dump(model: object, **kwargs: object) -> dict[str, object]:
    dump = getattr(model, "model_dump", None)
    if dump is not None:
        return dump(**kwargs)
    return model.dict(**kwargs)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "API de usuários ativa"}


@app.get("/users", response_model=list[User])
def list_users() -> list[dict[str, object]]:
    return list(_users.values())


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate) -> dict[str, object]:
    global _next_id

    if any(user["email"] == payload.email for user in _users.values()):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um usuário com este email",
        )

    user = {"id": _next_id, **payload.model_dump()}
    _users[_next_id] = user
    _next_id += 1
    return user


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int) -> dict[str, object]:
    user = _users.get(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return user


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, payload: UserUpdate) -> dict[str, object]:
    user = _users.get(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    updates = payload.model_dump(exclude_unset=True)

    if "email" in updates:
        email = updates["email"]
        if any(other_id != user_id and other["email"] == email for other_id, other in _users.items()):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um usuário com este email",
            )

    user.update(updates)
    return user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int) -> None:
    if user_id not in _users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    del _users[user_id]


def main() -> None:
    print("Hello, World!")


if __name__ == "__main__":
    main()