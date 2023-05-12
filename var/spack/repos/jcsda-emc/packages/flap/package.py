# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Flap(CMakePackage):
    """Fortran command Line Arguments Parser for poor people"""

    homepage = "https://github.com/mathomp4/FLAP"
    url = "https://github.com/mathomp4/FLAP/archive/refs/tags/geos/v1.10.0.tar.gz"
    git = "https://github.com/mathomp4/FLAP.git"

    maintainers("mathomp4")

    version("geos", branch="geos", submodules=True)
