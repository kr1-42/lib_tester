#!/usr/bin/env python3
import ctypes
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = Path(__file__).resolve().parent
SO_PATH = BUILD_DIR / "libft.so"


def build_shared_lib():
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    sources = sorted(str(p) for p in ROOT.glob("*.c"))
    if not sources:
        raise RuntimeError("No C sources found to build libft.so")
    cmd = [
        "gcc",
        "-shared",
        "-fPIC",
        "-O2",
        "-I",
        str(ROOT),
        "-o",
        str(SO_PATH),
    ] + sources
    subprocess.run(cmd, check=True)


def c_string(ptr):
    if not ptr:
        return None
    return ctypes.cast(ptr, ctypes.c_char_p).value


def ptr_offset(ptr, base):
    if not ptr:
        return None
    return int(ptr) - int(base)


class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.use_color = os.getenv("NO_COLOR") is None and sys.stdout.isatty()
        self.GREEN = "\033[0;32m" if self.use_color else ""
        self.RED = "\033[0;31m" if self.use_color else ""
        self.YELLOW = "\033[0;33m" if self.use_color else ""
        self.BOLD = "\033[1m" if self.use_color else ""
        self.RESET = "\033[0m" if self.use_color else ""

    def check(self, condition, message, detail=None):
        detail_text = f" - {detail}" if detail else ""
        if condition:
            self.passed += 1
            print(f"{self.GREEN}[PASS]{self.RESET} {message}{detail_text}")
        else:
            self.failed += 1
            print(f"{self.RED}[FAIL]{self.RESET} {message}{detail_text}")

    def summary(self):
        total = self.passed + self.failed
        status = "OK" if self.failed == 0 else "FAILED"
        color = self.GREEN if self.failed == 0 else self.RED
        print(
            f"\n{self.BOLD}Summary:{self.RESET} "
            f"{color}{status}{self.RESET} "
            f"({self.passed}/{total} passed)"
        )
        if self.failed:
            sys.exit(1)


def main():
    build_shared_lib()

    libft = ctypes.CDLL(str(SO_PATH))
    libc = ctypes.CDLL(None)

    libc.free.argtypes = [ctypes.c_void_p]
    libc.free.restype = None
    libc.strdup.argtypes = [ctypes.c_char_p]
    libc.strdup.restype = ctypes.c_void_p

    # Basic function signatures
    libft.ft_atoi.argtypes = [ctypes.c_char_p]
    libft.ft_atoi.restype = ctypes.c_int

    libft.ft_isalnum.argtypes = [ctypes.c_int]
    libft.ft_isalnum.restype = ctypes.c_int
    libft.ft_isalpha.argtypes = [ctypes.c_int]
    libft.ft_isalpha.restype = ctypes.c_int
    libft.ft_isascii.argtypes = [ctypes.c_int]
    libft.ft_isascii.restype = ctypes.c_int
    libft.ft_isdigit.argtypes = [ctypes.c_int]
    libft.ft_isdigit.restype = ctypes.c_int
    libft.ft_isprint.argtypes = [ctypes.c_int]
    libft.ft_isprint.restype = ctypes.c_int
    libft.ft_tolower.argtypes = [ctypes.c_int]
    libft.ft_tolower.restype = ctypes.c_int
    libft.ft_toupper.argtypes = [ctypes.c_int]
    libft.ft_toupper.restype = ctypes.c_int

    libft.ft_bzero.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    libft.ft_bzero.restype = None
    libft.ft_calloc.argtypes = [ctypes.c_size_t, ctypes.c_size_t]
    libft.ft_calloc.restype = ctypes.c_void_p
    libft.ft_memchr.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_size_t]
    libft.ft_memchr.restype = ctypes.c_void_p
    libft.ft_memcmp.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t]
    libft.ft_memcmp.restype = ctypes.c_int
    libft.ft_memcpy.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t]
    libft.ft_memcpy.restype = ctypes.c_void_p
    libft.ft_memmove.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t]
    libft.ft_memmove.restype = ctypes.c_void_p
    libft.ft_memset.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_size_t]
    libft.ft_memset.restype = ctypes.c_void_p

    libft.ft_strchr.argtypes = [ctypes.c_char_p, ctypes.c_int]
    libft.ft_strchr.restype = ctypes.c_void_p
    libft.ft_strdup.argtypes = [ctypes.c_char_p]
    libft.ft_strdup.restype = ctypes.c_void_p
    libft.ft_strjoin.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    libft.ft_strjoin.restype = ctypes.c_void_p
    libft.ft_strlcat.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t]
    libft.ft_strlcat.restype = ctypes.c_size_t
    libft.ft_strlcpy.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t]
    libft.ft_strlcpy.restype = ctypes.c_size_t
    libft.ft_strlen.argtypes = [ctypes.c_char_p]
    libft.ft_strlen.restype = ctypes.c_size_t
    libft.ft_strmapi.argtypes = [ctypes.c_char_p, ctypes.c_void_p]
    libft.ft_strmapi.restype = ctypes.c_void_p
    libft.ft_strncmp.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t]
    libft.ft_strncmp.restype = ctypes.c_int
    libft.ft_strnstr.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t]
    libft.ft_strnstr.restype = ctypes.c_void_p
    libft.ft_strrchr.argtypes = [ctypes.c_char_p, ctypes.c_int]
    libft.ft_strrchr.restype = ctypes.c_void_p
    libft.ft_strtrim.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    libft.ft_strtrim.restype = ctypes.c_void_p
    libft.ft_substr.argtypes = [ctypes.c_char_p, ctypes.c_uint, ctypes.c_size_t]
    libft.ft_substr.restype = ctypes.c_void_p
    libft.ft_itoa.argtypes = [ctypes.c_int]
    libft.ft_itoa.restype = ctypes.c_void_p
    libft.ft_split.argtypes = [ctypes.c_char_p, ctypes.c_char]
    libft.ft_split.restype = ctypes.POINTER(ctypes.c_void_p)
    libft.ft_striteri.argtypes = [ctypes.c_char_p, ctypes.c_void_p]
    libft.ft_striteri.restype = None

    libft.ft_putchar_fd.argtypes = [ctypes.c_char, ctypes.c_int]
    libft.ft_putchar_fd.restype = None
    libft.ft_putstr_fd.argtypes = [ctypes.c_char_p, ctypes.c_int]
    libft.ft_putstr_fd.restype = None
    libft.ft_putendl_fd.argtypes = [ctypes.c_char_p, ctypes.c_int]
    libft.ft_putendl_fd.restype = None
    libft.ft_putnbr_fd.argtypes = [ctypes.c_int, ctypes.c_int]
    libft.ft_putnbr_fd.restype = None

    runner = TestRunner()

    # Character tests
    runner.check(libft.ft_isalpha(ord('A')) != 0, "ft_isalpha('A')")
    runner.check(libft.ft_isalpha(ord('1')) == 0, "ft_isalpha('1')")
    runner.check(libft.ft_isdigit(ord('9')) != 0, "ft_isdigit('9')")
    runner.check(libft.ft_isalnum(ord('Z')) != 0, "ft_isalnum('Z')")
    runner.check(libft.ft_isascii(127) != 0, "ft_isascii(127)")
    runner.check(libft.ft_isprint(ord(' ')) != 0, "ft_isprint(' ')")
    runner.check(libft.ft_toupper(ord('a')) == ord('A'), "ft_toupper")
    runner.check(libft.ft_tolower(ord('Z')) == ord('z'), "ft_tolower")

    # atoi
    runner.check(libft.ft_atoi(b"42") == 42, "ft_atoi(42)")
    runner.check(libft.ft_atoi(b"   -42") == -42, "ft_atoi(-42)")
    runner.check(libft.ft_atoi(b"+123") == 123, "ft_atoi(+123)")

    # strlen
    runner.check(libft.ft_strlen(b"hello") == 5, "ft_strlen")

    # memset, bzero
    buf = ctypes.create_string_buffer(b"abcdef", 8)
    libft.ft_memset(buf, ord('x'), 3)
    runner.check(buf.raw[:6] == b"xxxdef", "ft_memset")
    libft.ft_bzero(buf, 6)
    runner.check(buf.raw[:6] == b"\x00" * 6, "ft_bzero")

    # memcpy, memmove
    src = ctypes.create_string_buffer(b"hello", 6)
    dst = ctypes.create_string_buffer(6)
    libft.ft_memcpy(dst, src, 6)
    runner.check(dst.raw[:6] == b"hello\x00", "ft_memcpy")
    overlap = ctypes.create_string_buffer(b"123456", 7)
    libft.ft_memmove(ctypes.byref(overlap, 2), overlap, 4)
    runner.check(overlap.raw[:6] == b"121234", "ft_memmove overlap")

    # memchr, memcmp
    data = ctypes.create_string_buffer(b"abcde", 6)
    base = ctypes.addressof(data)
    ptr = libft.ft_memchr(data, ord('d'), 5)
    runner.check(ptr_offset(ptr, base) == 3, "ft_memchr")
    runner.check(libft.ft_memcmp(b"abc", b"abd", 3) < 0, "ft_memcmp")

    # calloc
    calloc_ptr = libft.ft_calloc(4, 2)
    runner.check(bool(calloc_ptr), "ft_calloc non-null")
    if calloc_ptr:
        calloc_bytes = (ctypes.c_ubyte * 8).from_address(calloc_ptr)
        runner.check(all(b == 0 for b in calloc_bytes), "ft_calloc zeroed")
        libc.free(calloc_ptr)

    # strlcpy, strlcat
    dst = ctypes.create_string_buffer(3)
    ret = libft.ft_strlcpy(dst, b"hello", 3)
    runner.check(ret == 5 and dst.value == b"he", "ft_strlcpy trunc")
    dst = ctypes.create_string_buffer(b"hi", 10)
    ret = libft.ft_strlcat(dst, b"1234", 10)
    runner.check(ret == 6 and dst.value == b"hi1234", "ft_strlcat")

    # strchr, strrchr
    s = ctypes.create_string_buffer(b"banana", 7)
    base = ctypes.addressof(s)
    ptr = libft.ft_strchr(s, ord('n'))
    runner.check(ptr_offset(ptr, base) == 2, "ft_strchr")
    ptr = libft.ft_strrchr(s, ord('a'))
    runner.check(ptr_offset(ptr, base) == 5, "ft_strrchr")
    ptr = libft.ft_strrchr(s, 0)
    runner.check(ptr_offset(ptr, base) == 6, "ft_strrchr NUL")

    # strncmp, strnstr
    runner.check(libft.ft_strncmp(b"abc", b"abd", 3) < 0, "ft_strncmp")
    hay = ctypes.create_string_buffer(b"hello world", 12)
    base = ctypes.addressof(hay)
    ptr = libft.ft_strnstr(hay, b"world", 11)
    runner.check(ptr_offset(ptr, base) == 6, "ft_strnstr")

    # strdup, substr, strjoin, strtrim, itoa
    dup_ptr = libft.ft_strdup(b"copy")
    runner.check(c_string(dup_ptr) == b"copy", "ft_strdup")
    if dup_ptr:
        libc.free(dup_ptr)
    sub_ptr = libft.ft_substr(b"hello", 1, 3)
    runner.check(c_string(sub_ptr) == b"ell", "ft_substr")
    if sub_ptr:
        libc.free(sub_ptr)
    join_ptr = libft.ft_strjoin(b"foo", b"bar")
    runner.check(c_string(join_ptr) == b"foobar", "ft_strjoin")
    if join_ptr:
        libc.free(join_ptr)
    trim_ptr = libft.ft_strtrim(b"  hello  ", b" ")
    runner.check(c_string(trim_ptr) == b"hello", "ft_strtrim")
    if trim_ptr:
        libc.free(trim_ptr)
    itoa_ptr = libft.ft_itoa(-12345)
    runner.check(c_string(itoa_ptr) == b"-12345", "ft_itoa")
    if itoa_ptr:
        libc.free(itoa_ptr)

    # split
    split_ptr = libft.ft_split(b"hello  world", b' ')
    parts = []
    if split_ptr:
        i = 0
        while split_ptr[i]:
            parts.append(ctypes.cast(split_ptr[i], ctypes.c_char_p).value)
            libc.free(split_ptr[i])
            i += 1
        libc.free(split_ptr)
    runner.check(parts == [b"hello", b"world"], "ft_split")

    # strmapi
    @ctypes.CFUNCTYPE(ctypes.c_char, ctypes.c_uint, ctypes.c_int)
    def map_upper(idx, ch):
        if 97 <= ch <= 122:
            return ch - 32
        return ch

    mapi_ptr = libft.ft_strmapi(b"aBc", map_upper)
    runner.check(c_string(mapi_ptr) == b"ABC", "ft_strmapi")
    if mapi_ptr:
        libc.free(mapi_ptr)

    # striteri
    @ctypes.CFUNCTYPE(None, ctypes.c_uint, ctypes.POINTER(ctypes.c_char))
    def iter_upper(idx, ch_ptr):
        ch = ch_ptr[0]
        if isinstance(ch, bytes):
            ch = ch[0]
        if 97 <= ch <= 122:
            ch_ptr[0] = bytes([ch - 32])

    iter_buf = ctypes.create_string_buffer(b"aBc", 4)
    libft.ft_striteri(iter_buf, iter_upper)
    runner.check(iter_buf.value == b"ABC", "ft_striteri")

    # put* fd
    rfd, wfd = os.pipe()
    libft.ft_putchar_fd(b'Z', wfd)
    os.close(wfd)
    output = os.read(rfd, 10)
    os.close(rfd)
    runner.check(output == b"Z", "ft_putchar_fd")

    rfd, wfd = os.pipe()
    libft.ft_putstr_fd(b"hi", wfd)
    libft.ft_putendl_fd(b"!", wfd)
    libft.ft_putnbr_fd(-12, wfd)
    os.close(wfd)
    output = os.read(rfd, 64)
    os.close(rfd)
    runner.check(output == b"hi!\n-12", "ft_put* fd")

    # list functions
    class TList(ctypes.Structure):
        pass

    TList._fields_ = [
        ("content", ctypes.c_void_p),
        ("next", ctypes.POINTER(TList)),
    ]

    libft.ft_lstnew.argtypes = [ctypes.c_void_p]
    libft.ft_lstnew.restype = ctypes.POINTER(TList)
    libft.ft_lstadd_front.argtypes = [ctypes.POINTER(ctypes.POINTER(TList)), ctypes.POINTER(TList)]
    libft.ft_lstadd_back.argtypes = [ctypes.POINTER(ctypes.POINTER(TList)), ctypes.POINTER(TList)]
    libft.ft_lstsize.argtypes = [ctypes.POINTER(TList)]
    libft.ft_lstsize.restype = ctypes.c_int
    libft.ft_lstlast.argtypes = [ctypes.POINTER(TList)]
    libft.ft_lstlast.restype = ctypes.POINTER(TList)

    del_cb = ctypes.CFUNCTYPE(None, ctypes.c_void_p)(lambda p: libc.free(p))
    iter_cb_vals = []

    @ctypes.CFUNCTYPE(None, ctypes.c_void_p)
    def iter_cb(ptr):
        iter_cb_vals.append(ctypes.cast(ptr, ctypes.c_char_p).value)

    @ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)
    def map_cb(ptr):
        val = ctypes.cast(ptr, ctypes.c_char_p).value
        return libc.strdup(val.upper())

    libft.ft_lstdelone.argtypes = [ctypes.POINTER(TList), ctypes.CFUNCTYPE(None, ctypes.c_void_p)]
    libft.ft_lstclear.argtypes = [ctypes.POINTER(ctypes.POINTER(TList)), ctypes.CFUNCTYPE(None, ctypes.c_void_p)]
    libft.ft_lstiter.argtypes = [ctypes.POINTER(TList), ctypes.CFUNCTYPE(None, ctypes.c_void_p)]
    libft.ft_lstmap.argtypes = [ctypes.POINTER(TList), ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p), ctypes.CFUNCTYPE(None, ctypes.c_void_p)]
    libft.ft_lstmap.restype = ctypes.POINTER(TList)

    head = ctypes.POINTER(TList)()
    n1 = libft.ft_lstnew(libc.strdup(b"one"))
    n2 = libft.ft_lstnew(libc.strdup(b"two"))
    n3 = libft.ft_lstnew(libc.strdup(b"three"))
    libft.ft_lstadd_front(ctypes.byref(head), n1)
    libft.ft_lstadd_back(ctypes.byref(head), n2)
    libft.ft_lstadd_back(ctypes.byref(head), n3)

    runner.check(libft.ft_lstsize(head) == 3, "ft_lstsize")
    last = libft.ft_lstlast(head)
    runner.check(c_string(last.contents.content) == b"three", "ft_lstlast")
    libft.ft_lstiter(head, iter_cb)
    runner.check(iter_cb_vals == [b"one", b"two", b"three"], "ft_lstiter")

    mapped = libft.ft_lstmap(head, map_cb, del_cb)
    mapped_vals = []
    cur = mapped
    while cur:
        mapped_vals.append(c_string(cur.contents.content))
        cur = cur.contents.next
    runner.check(mapped_vals == [b"ONE", b"TWO", b"THREE"], "ft_lstmap")

    libft.ft_lstclear(ctypes.byref(head), del_cb)
    libft.ft_lstclear(ctypes.byref(mapped), del_cb)

    runner.summary()


if __name__ == "__main__":
    main()
