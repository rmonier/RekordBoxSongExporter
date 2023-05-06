from conan import ConanFile
from conans.errors import ConanException
from conan.tools.microsoft import MSBuild, MSBuildDeps, MSBuildToolchain

required_conan_version = ">=2.0"


class RekordBoxSongExporter(ConanFile):
    """
    Install and build with:

    conan build . -of conan/build/debug -pr ./conan/profiles/debug -pr:b ./conan/profiles/debug --build missing
    or
    conan build . -of conan/build/release -pr ./conan/profiles/release -pr:b ./conan/profiles/release --build missing
    """
    name = "RekordBoxSongExporter"
    version = "3.8"
    package_type = "application"
    settings = "build_type", "os", "arch", "compiler"
    build_policy = "missing"

    _platform = None

    def _requires(self, lib, version):
        profile = 'debug' if self.settings.build_type == 'Debug' else 'release'
        self.run(f"conan create conan/recipes/{lib} -pr ./conan/profiles/{profile} -pr:b ./conan/profiles/{profile} --build missing")
        self.requires(f"{lib}/{version}")

    def requirements(self):
        self._requires("capstone", "4.0.2")
        self._requires("link", "3.0.6")

    def validate(self):
        if self.settings.os != "Windows" or self.settings.compiler != "msvc" or self.settings.arch != "x86_64":
            raise ConanException("Only x86_64 Windows with MSVC is supported")
        if self.settings.arch == "x86_64":
            self._platform = "x64"
        else:
            raise ConanException("Unsupported architecture")

    def generate(self):
        ms = MSBuildDeps(self)
        ms.generate()
        tc = MSBuildToolchain(self)
        if self.settings.os == "Linux":
            tc.preprocessor_definitions["LINK_PLATFORM_LINUX"] = 1
        elif self.settings.os == "Macos":
            tc.preprocessor_definitions["LINK_PLATFORM_MACOS"] = 1
        elif self.settings.os == "Windows":
            tc.preprocessor_definitions["LINK_PLATFORM_WINDOWS"] = 1
        tc.generate()

    def build(self):
        msbuild = MSBuild(self)
        # hacky way to add parameters to the build command
        msbuild.platform = f"{self._platform} /p:ForceImportBeforeCppProps={self.build_folder}/conandeps.props " \
                           f"/p:ForceImportAfterCppDefaultProps={self.build_folder}/conantoolchain.props"
        msbuild.build(f"{self.source_folder}/RekordBoxSongExporter.sln")
