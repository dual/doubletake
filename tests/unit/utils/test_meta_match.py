import unittest
from doubletake.utils.meta_match import MetaMatch


class TestMetaMatch(unittest.TestCase):

    def test_defaults(self):
        m = MetaMatch()
        self.assertEqual(m.pattern, '')
        self.assertEqual(m.replacement, '')
        self.assertIsInstance(m.breadcrumbs, set)
        self.assertEqual(len(m.breadcrumbs), 0)

    def test_custom_values(self):
        m = MetaMatch(pattern='foo', value='baz', replacement='bar', breadcrumbs={'a', 'b'})
        self.assertEqual(m.pattern, 'foo')
        self.assertEqual(m.value, 'baz')
        self.assertEqual(m.replacement, 'bar')
        self.assertEqual(m.breadcrumbs, {'a', 'b'})

    def test_repr_and_eq(self):
        m1 = MetaMatch(pattern='x', value='y', replacement='z', breadcrumbs={'w'})
        m2 = MetaMatch(pattern='x', value='y', replacement='z', breadcrumbs={'w'})
        m3 = MetaMatch(pattern='a', value='b', replacement='c', breadcrumbs={'c'})
        self.assertEqual(m1, m2)
        self.assertNotEqual(m1, m3)
        self.assertIn('MetaMatch', repr(m1))

    def test_breadcrumbs_are_independent(self):
        m1 = MetaMatch()
        m2 = MetaMatch()
        m1.breadcrumbs.add('foo')
        self.assertNotIn('foo', m2.breadcrumbs)
