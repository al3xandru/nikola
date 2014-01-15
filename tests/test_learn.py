import unittest

try:
    from urlparse import urlparse, urlsplit, urljoin
except ImportError:
    from urllib.parse import urlparse, urlsplit, urljoin  # NOQA

def abs_link(base_url, dst):
    # Normalize
    dst = urljoin(base_url, dst)

    return urlparse(dst).path

def rel_link(base_url, src, dst):
    # Normalize
    src = urljoin(base_url, src)
    dst = urljoin(src, dst)
    # Avoid empty links.
    if src == dst:
        return "#"
    # Check that link can be made relative, otherwise return dest
    parsed_src = urlsplit(src)
    parsed_dst = urlsplit(dst)
    if parsed_src[:2] != parsed_dst[:2]:
        return dst
    # Now both paths are on the same site and absolute
    src_elems = parsed_src.path.split('/')[1:]
    dst_elems = parsed_dst.path.split('/')[1:]
    i = 0
    for (i, s), d in zip(enumerate(src_elems), dst_elems):
        if s != d:
            break
    else:
        i += 1
    # Now i is the longest common prefix
    return '/'.join(['..'] * (len(src_elems) - i - 1) + dst_elems[i:])


class LearnTest(unittest.TestCase):
    BASE_URL = 'http://stage.docs.datastax.com/'

    def test_urljoin(self):
        result = urljoin(self.BASE_URL, '/assets/css/style.css')
        self.assertEqual('http://stage.docs.datastax.com/assets/css/style.css', result)

        result = urljoin(self.BASE_URL, 'assets/css/style.css')
        self.assertEqual('http://stage.docs.datastax.com/assets/css/style.css', result)

        result = urljoin(self.BASE_URL + 'dir1/', 'assets/css/style.css')
        self.assertEqual('http://stage.docs.datastax.com/dir1/assets/css/style.css', result)

        result = urljoin(self.BASE_URL + 'dir1/a_page.html', '../assets/css/style.css')
        self.assertEqual('http://stage.docs.datastax.com/assets/css/style.css', result)

        result = urljoin(self.BASE_URL + 'dir1/dir2/a_page', '../assets/css/style.css')
        self.assertEqual('http://stage.docs.datastax.com/dir1/assets/css/style.css', result)


    def test_rel_link(self):
        result = abs_link(self.BASE_URL, '/assets/css/style.css')
        self.assertEqual('/assets/css/style.css', result)

        result = abs_link(self.BASE_URL, 'assets/css/style.css')
        self.assertEqual('/assets/css/style.css', result)

        result = abs_link(self.BASE_URL, self.BASE_URL + 'assets/css/style.css')
        self.assertEqual('/assets/css/style.css', result)

        result = abs_link(self.BASE_URL + 'dir1', self.BASE_URL + 'dir1/dir2/a_page.html')
        self.assertEqual('/dir1/dir2/a_page.html', result)

    def test_abs_link(self):
        result = abs_link(self.BASE_URL, '/assets/css/style.css')
        self.assertEqual('/assets/css/style.css', result)

        result = abs_link(self.BASE_URL, 'assets/css/style.css')
        self.assertEqual('/assets/css/style.css', result)

        result = abs_link(self.BASE_URL, self.BASE_URL + 'assets/css/style.css')
        self.assertEqual('/assets/css/style.css', result)

        result = abs_link(self.BASE_URL + 'dir1', self.BASE_URL + 'dir1/dir2/a_page.html')
        self.assertEqual('/dir1/dir2/a_page.html', result)
