from starlette.requests import Request
from starlette.datastructures import Headers
from starlette.types import ASGIApp, Scope, Receive, Send
from typing import Sequence
from app.utils.date_utils import D


class AccessControl:
    def __init__(
        self,
        app: ASGIApp,
        except_path_list: Sequence[str] = None,
        except_path_regex: str = None,
    ) -> None:
        if except_path_list is None:
            except_path_list = ["*"]
        self.app = app
        self.except_path_list = except_path_list
        self.except_path_regex = except_path_regex

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        # 실행 순서 확인 1
        print(self.except_path_regex)
        print(self.except_path_list)

        request = Request(scope=scope)
        headers = Headers(scope=scope)

        # 실행 순서 확인 2
        print(D.datetime())
        print(D.date())
        print(D.date_num())

        print(f"cookies: {request.cookies}")
        print(f"headers: {headers}")

        res = await self.app(scope, receive, send)
        return res
