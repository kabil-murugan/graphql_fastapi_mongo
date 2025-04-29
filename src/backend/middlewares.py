"""Middlewares"""

import cProfile
import pstats

from fastapi.responses import Response


class ProfilingMiddleware:
    """Middleware to profile requests using cProfile."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            profiler = cProfile.Profile()
            profiler.enable()

            response = Response("Internal Server Error", status_code=500)
            try:
                response = await self.app(scope, receive, send)
            finally:
                profiler.disable()

                # Save profiling stats to a file
                with open("profile_stats.prof", "w") as f:
                    ps = pstats.Stats(profiler, stream=f).sort_stats(
                        pstats.SortKey.TIME
                    )
                    ps.print_stats()

            return response
        else:
            await self.app(scope, receive, send)
