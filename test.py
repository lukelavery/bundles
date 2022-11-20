# # sequence = [5, 2, 4, 6, 1, 3]


# def insertion_sort(seq: list[int]) -> list[int]:
#     for j, key in enumerate(seq):
#         i = j - 1
#         while i >= 0 and seq[i] < key:
#             seq[i + 1] = seq[i]
#             i = i - 1
#         seq[i + 1] = key
#     return seq


# # def linear_search(seq: list[int], v: int) -> int:
# #     for j, key in enumerate(seq):
# #         if key == v:
# #             return j
# #     return ('NIL')


# class MyParent:
#     def __init__(self):
#         self.dictionary = {}
#         self.child = MyChild(self.dictionary)


# class MyChild:
#     def __init__(self, dictionary):
#         self.dictionary = dictionary


# myParent = MyParent()
# myParent.dictionary.update({'test': 1})
# print(myParent.child.dictionary)

import os


print(os.path.isfile(
    "C:/Users/lukel/Desktop/900000/900000/Prepare Bundles/Test Bundle/index_template.docx"))
