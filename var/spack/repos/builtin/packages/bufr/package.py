# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import os


class Bufr(CMakePackage):
    """The NOAA bufr library contains subroutines, functions and other
    utilities that can be used to read (decode) and write (encode)
    data in BUFR, which is a WMO standard format for the exchange of
    meteorological data. This is part of the NCEPLIBS project.
    The library also includes a Python interface.
    """

    homepage = "https://noaa-emc.github.io/NCEPLIBS-bufr"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-bufr/archive/refs/tags/bufr_v11.5.0.tar.gz"

    maintainers = ['t-brown', 'kgerheiser', 'edwardhartnett', 'Hang-Lei-NOAA',
                   'jbathegit']

    version('11.5.0', sha256='d154839e29ef1fe82e58cf20232e9f8a4f0610f0e8b6a394b7ca052e58f97f43')

    # Patch to not add '-c' to ranlib flags when using llvm-ranlib on Apple systems
    patch('cmakelists-apple-llvm-ranlib.patch', when='@:11.5.0')

    variant('python', default=False, description='Enable Python interface?')
    extends('python', when='+python')

    depends_on('python@3:', type=('build', 'run'), when='+python')
    depends_on('py-setuptools', type='build', when='+python')
    depends_on('py-numpy', type='build', when='+python')
    depends_on('py-pip', type='build', when='+python')


    def cmake_args(self):
        args = [
            self.define_from_variant('ENABLE_PYTHON', 'python')
        ]

        return args


    def flag_handler(self, name, flags):
        """
        On macOS if a library built with the ar utility contains objects
        with Fortran module data but no executable functions,
        the symbols corresponding to the module data may not be resolved
        when an object referencing them is linked against the library.
        You can work around this by compiling with option -fno-common.
        """
        fc = self.compiler.fc
        if self.spec.satisfies('platform=darwin'):
            if name == 'fflags':
                if 'ifort' in fc or 'gfortran' in fc:
                    flags.append('-fno-common')

        # Bufr inserts a path into source code which may be longer than 132
        if fc == 'gfortran':
            flags.append('-ffree-line-length-none')

        # Inject flags into CMake build
        return (None, None, flags)

    def _setup_bufr_environment(self, env, suffix):
        libname = 'libbufr_{0}'.format(suffix)
        lib = find_libraries(libname, root=self.prefix,
                             shared=False, recursive=True)

        lib_envname = 'BUFR_LIB{0}'.format(suffix)
        inc_envname = 'BUFR_INC{0}'.format(suffix)
        include_dir = 'include_{0}'.format(suffix)

        env.set(lib_envname, lib[0])
        env.set(inc_envname, include_dir)

        # Bufr has _DA (dynamic allocation) libs in versions <= 11.5.0
        if self.spec.satisfies('@:11.5.0'):
            da_lib = find_libraries(libname + "_DA", root=self.prefix,
                                    shared=False, recursive=True)
            env.set(lib_envname + '_DA', da_lib[0])
            env.set(inc_envname + '_DA', include_dir)

    def setup_run_environment(self, env):
        for suffix in ('4', '8', 'd'):
            self._setup_bufr_environment(env, suffix)

    # setup.py is generated by cmake and therefore lives in the
    # subdirectory 'python' of the package build_directory
    @run_after('install')
    def install_python_interface(self):
        prefix = self.prefix
        if self.spec.satisfies('+python'):
            with working_dir(os.path.join(self.build_directory,'python')):
                args = std_pip_args + ['--prefix=' + prefix, '.']
                pip(*args)
