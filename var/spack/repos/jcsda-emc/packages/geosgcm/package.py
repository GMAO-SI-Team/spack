# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Geosgcm(CMakePackage):
    """
    GEOS Earth System Model GEOSgcm Fixture
    """

    homepage = "https://github.com/GEOS-ESM/GEOSgcm"
    url = "https://github.com/GEOS-ESM/GEOSgcm/releases/download/v10.25.0/GEOSgcm-v10.25.0.COMPLETE.tar.xz"
    git = "https://github.com/GEOS-ESM/GEOSgcm.git"

    maintainers("mathomp4", "tclune")

    def url_for_version(self, version):
        url_base = "https://github.com/GEOS-ESM/GEOSgcm/releases/download/"
        url = url_base + "v{0}/GEOSgcm-v{0}.COMPLETE.tar.xz"

        return url.format(version)

    version("main", branch="main")

    # Must be retrieve with spack checksum@vX.Y.Z as it is not a usual git release
    version("11.0.0", sha256="1c209bda4fcd8462d0f1189d7c8db423c8432fc929b245f91eda581234b361e3")
    version("10.25.1", sha256="f541dc38163c554177c21746999e8cd9fb2daa127de1a4171ef82ac1a536fa2f")
    version("10.25.0", sha256="08887ca652387d51d92e62fd16c0944e6c2a53513abb081cc1150a28d128c4c3")
    version("10.24.0", sha256="59e35b446f258a36ba41f753c5724eb08c7cd0ccbafca1cfb329419cac045e24")
    version("10.23.3", sha256="131585394b2ece57af7585247e73d7bff6e27c42daa40cd05b47f90a471d06cf")
    version("10.23.2", sha256="0f3adb6f65e57cab372bbf1e00b4fcd5d6e7009d4851d4968d2f4c87345a43ec")
    version("10.23.1", sha256="6469331858ef005bf0d8eb90fe1c4d7b37648bebc0529a32284a0ceaf8d9274f")
    version("10.23.0", sha256="99579429f6116e4f4e82587f423132dc896f7cfd336499487094ddeb227b450a")

    variant("f2py", default=False, description="Build with f2py support")
    variant("extdata2g", default=True, description="Use ExtData2G")

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release", "Aggressive"),
    )

    depends_on("cmake@3.17:")
    depends_on("mpi")
    depends_on("ecbuild")

    # These are for MAPL AGC and stubber
    depends_on("python@3:")
    depends_on("py-pyyaml")
    depends_on("perl")

    # These are similarly the dependencies of MAPL. Not sure if we'll ever use MAPL as library
    depends_on("hdf5")
    depends_on("netcdf-c@4.9.0:")
    depends_on("netcdf-fortran@4.6.0:")
    depends_on("esmf@8.4.0:")
    depends_on("gftl@1.5.5:")
    depends_on("gftl-shared@1.3.1:")
    depends_on("yafyaml@1.0.4:", when="+extdata2g")
    depends_on("pflogger@1.9.1:")
    depends_on("fargparse@1.4.1:")
    depends_on("flap@geos")

    # MAPL as library would be like:
    #  depends_on("mapl@2.34:+flap+pflogger+extdata2g+fargparse")
    # but we don't want to do this in general due to the speed of MAPL development

    # When we move to FMS as library, we'll need to add this:
    #depends_on("fms@2022.04:~gfs_phys+fpic~quad_precision+32bit+64bit+yaml constants=GEOS")

    def cmake_args(self):
        args = [
            self.define_from_variant("USE_F2PY", "f2py"),
            self.define_from_variant("USE_EXTDATA2G", "extdata2g"),
            self.define("CMAKE_MODULE_PATH", self.spec["esmf"].prefix.cmake),
            "-DCMAKE_C_COMPILER=%s" % self.spec["mpi"].mpicc,
            "-DCMAKE_CXX_COMPILER=%s" % self.spec["mpi"].mpicxx,
            "-DCMAKE_Fortran_COMPILER=%s" % self.spec["mpi"].mpifc,
        ]

        return args
