import unittest
import cxxheader as ch

def get_config(outfile, namespaces):
    args = ['-o', outfile, '-n'] + namespaces
    header_config = ch.parse(args)
    return header_config

class CxxHeader(unittest.TestCase):

    def assert_config_for_namespaces(self, outfile, expected_header_guard,
            expected_namespaces):
        config = get_config(outfile, expected_namespaces)
        self.assertEqual(expected_namespaces, config.cxx_namespaces)
        self.assertEqual(expected_header_guard, config.header_guard)

    def assert_config(self, outfile_and_namespaces, expected_header_guard):
        split = outfile_and_namespaces.split(',')
        outfile = split[0]
        namespaces = split[1:]
        self.assert_config_for_namespaces(outfile, expected_header_guard,
            namespaces)

    def test_no_namespace_option_is_default(self):
        self.assert_config_for_namespaces('~/dev/my_header.hpp',
            '_PROJECT_MYHEADER_HPP_', ['project'])

    def test_gets_namespaces(self):
        self.assert_config('vector.hh,company,project,detail',
            '_COMPANY_PROJECT_DETAIL_VECTOR_HH_')

    def test_allows_multiple_dots_in_file(self):
        self.assert_config('header.abc.xyz,ns', '_NS_HEADERABC_XYZ_')
    
    def test_ignores_outfile_dirs(self):
        self.assert_config('~/dev/out.h,ns1,ns2', '_NS1_NS2_OUT_H_')

if __name__ == '__main__':
    unittest.main()
