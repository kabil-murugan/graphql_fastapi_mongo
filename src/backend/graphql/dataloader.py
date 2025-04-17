from strawberry.dataloader import DataLoader
from strawberry.dataloader import get_current_batch


class CustomDataLoader(DataLoader):
    def load(self, key):
        if self.cache:
            future = self.cache_map.get(key)

            if future is None or future.done():
                future = self.loop.create_future()
                if future is None:
                    self.cache_map.set(key, future)

        batch = get_current_batch(self)
        batch.add_task(key, future)
        return future
