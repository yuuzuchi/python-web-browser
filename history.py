import collections


class HistoryManager:
    def __init__(self):
        self.history = []
        self.visited_map = collections.defaultdict(int)

    def append(self, url: str):
        # don't duplicate on refresh
        if self.history and self.history[-1] == url:
            return

        self.history.append(url)
        self.visited_map[url] += 1

    def remove(self, idx):
        if idx < len(self.history):
            url = self.history.pop(idx)
            assert self.visited_map[url] > 0
            self.visited_map[url] -= 1

            if self.visited_map[url] <= 0:
                del self.visited_map[url]

    def has_url(self, url: str) -> bool:
        return url in self.visited_map
