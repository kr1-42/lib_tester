import ctypes


class TList(ctypes.Structure):
    pass


TList._fields_ = [
    ("content", ctypes.c_void_p),
    ("next", ctypes.POINTER(TList)),
]


def _new_node(libft, libc, value):
    return libft.ft_lstnew(libc.strdup(value))


def _collect_values(head, c_string):
    values = []
    cur = head
    while cur:
        values.append(c_string(cur.contents.content))
        cur = cur.contents.next
    return values


def run(libft, libc, runner, c_string):
    libft.ft_lstnew.argtypes = [ctypes.c_void_p]
    libft.ft_lstnew.restype = ctypes.POINTER(TList)
    libft.ft_lstadd_front.argtypes = [ctypes.POINTER(ctypes.POINTER(TList)), ctypes.POINTER(TList)]
    libft.ft_lstadd_back.argtypes = [ctypes.POINTER(ctypes.POINTER(TList)), ctypes.POINTER(TList)]
    libft.ft_lstsize.argtypes = [ctypes.POINTER(TList)]
    libft.ft_lstsize.restype = ctypes.c_int
    libft.ft_lstlast.argtypes = [ctypes.POINTER(TList)]
    libft.ft_lstlast.restype = ctypes.POINTER(TList)
    libft.ft_lstdelone.argtypes = [ctypes.POINTER(TList), ctypes.CFUNCTYPE(None, ctypes.c_void_p)]
    libft.ft_lstclear.argtypes = [ctypes.POINTER(ctypes.POINTER(TList)), ctypes.CFUNCTYPE(None, ctypes.c_void_p)]
    libft.ft_lstiter.argtypes = [ctypes.POINTER(TList), ctypes.CFUNCTYPE(None, ctypes.c_void_p)]
    libft.ft_lstmap.argtypes = [
        ctypes.POINTER(TList),
        ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p),
        ctypes.CFUNCTYPE(None, ctypes.c_void_p),
    ]
    libft.ft_lstmap.restype = ctypes.POINTER(TList)

    del_calls = {"count": 0}

    @ctypes.CFUNCTYPE(None, ctypes.c_void_p)
    def del_cb(ptr):
        del_calls["count"] += 1
        libc.free(ptr)

    iter_cb_vals = []

    @ctypes.CFUNCTYPE(None, ctypes.c_void_p)
    def iter_cb(ptr):
        iter_cb_vals.append(ctypes.cast(ptr, ctypes.c_char_p).value)

    @ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)
    def map_cb(ptr):
        val = ctypes.cast(ptr, ctypes.c_char_p).value
        return libc.strdup(val.upper())

    head = ctypes.POINTER(TList)()
    runner.check(libft.ft_lstsize(head) == 0, "ft_lstsize", "empty")
    last = libft.ft_lstlast(head)
    runner.check(bool(last) is False, "ft_lstlast", "empty")

    n1 = _new_node(libft, libc, b"one")
    libft.ft_lstadd_front(ctypes.byref(head), n1)
    runner.check(libft.ft_lstsize(head) == 1, "ft_lstadd_front", "into empty")
    runner.check(c_string(head.contents.content) == b"one", "ft_lstadd_front", "head is one")

    n2 = _new_node(libft, libc, b"two")
    libft.ft_lstadd_back(ctypes.byref(head), n2)
    runner.check(libft.ft_lstsize(head) == 2, "ft_lstadd_back", "append")

    n3 = _new_node(libft, libc, b"three")
    libft.ft_lstadd_back(ctypes.byref(head), n3)
    values = _collect_values(head, c_string)
    runner.check(values == [b"one", b"two", b"three"], "ft_lstadd_back", "order preserved")

    n0 = _new_node(libft, libc, b"zero")
    libft.ft_lstadd_front(ctypes.byref(head), n0)
    values = _collect_values(head, c_string)
    runner.check(values == [b"zero", b"one", b"two", b"three"], "ft_lstadd_front", "prepend")

    last = libft.ft_lstlast(head)
    runner.check(c_string(last.contents.content) == b"three", "ft_lstlast", "non-empty")

    libft.ft_lstiter(head, iter_cb)
    runner.check(iter_cb_vals == [b"zero", b"one", b"two", b"three"], "ft_lstiter", "collect values")

    mapped = libft.ft_lstmap(head, map_cb, del_cb)
    mapped_vals = _collect_values(mapped, c_string)
    runner.check(mapped_vals == [b"ZERO", b"ONE", b"TWO", b"THREE"], "ft_lstmap", "upper")
    original_vals = _collect_values(head, c_string)
    runner.check(original_vals == [b"zero", b"one", b"two", b"three"], "ft_lstmap", "original intact")

    single = _new_node(libft, libc, b"tmp")
    libft.ft_lstdelone(single, del_cb)
    runner.check(del_calls["count"] >= 1, "ft_lstdelone", "del called")

    libft.ft_lstclear(ctypes.byref(head), del_cb)
    runner.check(bool(head) is False, "ft_lstclear", "head cleared")
    runner.check(libft.ft_lstsize(head) == 0, "ft_lstsize", "after clear")

    libft.ft_lstclear(ctypes.byref(mapped), del_cb)
