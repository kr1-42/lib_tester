import ctypes


def _split_to_list(libc, split_ptr):
    parts = []
    if split_ptr:
        i = 0
        while split_ptr[i]:
            parts.append(ctypes.cast(split_ptr[i], ctypes.c_char_p).value)
            libc.free(split_ptr[i])
            i += 1
        libc.free(split_ptr)
    return parts


def _trim_and_check(libft, libc, runner, c_string, s, charset, expected, label):
    trim_ptr = libft.ft_strtrim(s, charset)
    runner.check(c_string(trim_ptr) == expected, "ft_strtrim", label)
    if trim_ptr:
        libc.free(trim_ptr)


def run(libft, libc, runner, c_string):
    _trim_and_check(libft, libc, runner, c_string, b"  hello  ", b" ", b"hello", "spaces")
    _trim_and_check(libft, libc, runner, c_string, b"xxhelloxx", b"x", b"hello", "custom set")
    _trim_and_check(libft, libc, runner, c_string, b"hello", b" ", b"hello", "no trim")
    _trim_and_check(libft, libc, runner, c_string, b"", b" ", b"", "empty string")
    _trim_and_check(libft, libc, runner, c_string, b"aaaa", b"a", b"", "all trimmed")
    _trim_and_check(libft, libc, runner, c_string, b"abc", b"", b"abc", "empty set")
    _trim_and_check(libft, libc, runner, c_string, b"\t\nhello \n", b" \n\t", b"hello", "whitespace set")
    _trim_and_check(libft, libc, runner, c_string, b"abca", b"a", b"bc", "trim ends only")
    _trim_and_check(libft, libc, runner, c_string, b"abc", b"abc", b"", "all chars set")
    _trim_and_check(libft, libc, runner, c_string, b"--hello--", b"-_", b"hello", "multi-char set")

    split_ptr = libft.ft_split(b"hello  world", b" ")
    parts = _split_to_list(libc, split_ptr)
    runner.check(parts == [b"hello", b"world"], "ft_split", "multi-spaces")

    split_ptr = libft.ft_split(b"  a  b c ", b" ")
    parts = _split_to_list(libc, split_ptr)
    runner.check(parts == [b"a", b"b", b"c"], "ft_split", "trim empties")

    split_ptr = libft.ft_split(b"", b" ")
    parts = _split_to_list(libc, split_ptr)
    runner.check(parts == [], "ft_split", "empty input")

    split_ptr = libft.ft_split(b"one", b" ")
    parts = _split_to_list(libc, split_ptr)
    runner.check(parts == [b"one"], "ft_split", "no delimiter")

    split_ptr = libft.ft_split(b",,a,,b,,", b",")
    parts = _split_to_list(libc, split_ptr)
    runner.check(parts == [b"a", b"b"], "ft_split", "leading/trailing delimiters")

    split_ptr = libft.ft_split(b"a,,b", b",")
    parts = _split_to_list(libc, split_ptr)
    runner.check(parts == [b"a", b"b"], "ft_split", "consecutive delimiters")

    split_ptr = libft.ft_split(b",,,,", b",")
    parts = _split_to_list(libc, split_ptr)
    runner.check(parts == [], "ft_split", "only delimiters")

    split_ptr = libft.ft_split(b"a b c", b" ")
    parts = _split_to_list(libc, split_ptr)
    runner.check(parts == [b"a", b"b", b"c"], "ft_split", "simple spaces")

    split_ptr = libft.ft_split(b"  ", b" ")
    parts = _split_to_list(libc, split_ptr)
    runner.check(parts == [], "ft_split", "spaces only")

    split_ptr = libft.ft_split(b"aba", b"a")
    parts = _split_to_list(libc, split_ptr)
    runner.check(parts == [b"b"], "ft_split", "delimiter char in string")

    split_ptr = libft.ft_split(b"x|y||z|", b"|")
    parts = _split_to_list(libc, split_ptr)
    runner.check(parts == [b"x", b"y", b"z"], "ft_split", "pipe delimiter")
