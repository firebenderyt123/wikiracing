from typing import List, Dict, Any, Optional


class CustomList:

    def __init__(self):
        self._data = []
        self._curr_obj = -1
        self._curr_level = -1
        self._total_levels = 0

    @property
    def curr_level(self):
        return self._curr_level

    @curr_level.setter
    def curr_level(self, level: int):
        if level > -1 and level < self._total_levels:
            self._curr_level = level

    def get_title(self, level: int):
        return [obj['title'] for obj in self._data[level]]

    def get_parent(self, level: int):
        return [obj['parent'] for obj in self._data[level]]

    def get_level(self) -> Optional[List[Dict[str, Any]]]:
        if self._curr_level > -1 and self._curr_level < self._total_levels:
            return self._data[self._curr_level]

    def next_level(self) -> Optional[List[Dict[str, Any]]]:
        if self._curr_level < self._total_levels - 1:
            self._curr_level += 1
            return self._data[self._curr_level]

    def prev_level(self) -> Optional[List[Dict[str, Any]]]:
        if self._curr_level > 0:
            self._curr_level -= 1
            return self._data[self._curr_level]

    def get_data(self) -> Optional[Dict[str, Any]]:
        if (self._curr_obj > -1 and
                self._curr_obj < len(self._data[self._curr_level])):
            return self._data[self._curr_level][self._curr_obj]

    def next_data(self) -> Optional[Dict[str, Any]]:
        if self._curr_obj < len(self._data[self._curr_level]) - 1:
            self._curr_obj += 1
            return self._data[self._curr_level][self._curr_obj]

    def prev_data(self) -> Optional[Dict[str, Any]]:
        if self._curr_obj > 0:
            self._curr_obj -= 1
            return self._data[self._curr_level][self._curr_obj]

    def append_level(self) -> int:
        self._data.append([])
        self._total_levels += 1
        self._curr_level = self._total_levels - 1
        return self._curr_level

    def insert_level(self, num: int) -> int:
        self._data.insert(num, [])
        self._total_levels += 1
        self._curr_level = num
        return self._curr_level

    def remove_level(self, level: int):
        self._data.remove(level)
        self._total_levels -= 1
        if level <= self._curr_level:
            self._curr_level -= 1

    def append_data(self, obj: Dict[str, Any]):
        self._data[self._curr_level].append(obj)
        self._curr_obj = len(self._data[-1]) - 1

    def insert_data(self, obj: Dict[str, Any], level: int = 0): # noqa
        self._data[level].append(obj)
        self._curr_obj = len(self._data[level]) - 1

    def prepend_data(self, obj: Dict[str, Any]):
        self._data[self._curr_level].insert(0, obj)
        self._curr_obj = len(self._data[0]) - 1

    def compare(self) -> bool:
        left_part = self._data[:self._total_levels // 2]
        right_part = self._data[self._total_levels // 2:]
        right_titles = [obj['title'] for arr in right_part for obj in arr]
        for arr in left_part:
            for obj in arr:
                if obj['title'] in right_titles:
                    return obj['title']
        return False


# cL = CustomList()
# cL.append_level()
# cL.append_data({'title': 'Title11', 'link': 'test'})
# cL.append_data({'title': 'Title12', 'link': 'test'})
# cL.append_data({'title': 'Title13', 'link': 'test'})
# cL.append_data({'title': 'Title14', 'link': 'test'})
# cL.append_level()
# cL.append_data({'title': 'Title21', 'link': 'test'})
# cL.append_data({'title': 'Title22', 'link': 'test'})
# cL.append_data({'title': 'Title23', 'link': 'test'})
# cL.append_level()
# cL.append_data({'title': 'Title31', 'link': 'test'})
# cL.append_data({'title': 'Title32', 'link': 'test'})
# cL.append_data({'title': 'Title33', 'link': 'test'})
# cL.append_level()
# cL.append_data({'title': 'Title41', 'link': 'test'})
# cL.append_data({'title': 'Title42', 'link': 'test'})
# cL.append_data({'title': 'Title43', 'link': 'test'})
# level = cL._curr_level
# print(level)
# obj_num = cL._curr_obj
# print(obj_num)
# data = cL.get_data()
# print(data)
# data = cL.prev_data()
# obj_num = cL._curr_obj
# print(obj_num)
# print(data)
# data = cL.prev_data()
# obj_num = cL._curr_obj
# print(obj_num)
# print(data)
# data = cL.prev_data()
# obj_num = cL._curr_obj
# print(obj_num)
# print(data)
# level = cL.prev_level()
# print(level)
# data = cL.get_data()
# print(data)
# data = cL.next_data()
# print(data)
# data = cL.next_data()
# print(data)
# data = cL.next_data()
# print(data)
# obj_num = cL._curr_obj
# data = cL.next_data()
# print(obj_num)
# print(data)

# cL.compare()
