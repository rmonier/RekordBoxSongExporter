from conan import ConanFile
from conan.tools.microsoft import MSBuild, MSBuildToolchain
from conan.tools.files import replace_in_file, copy, symlinks
from conan.tools.scm import Git
from conans.errors import ConanException

required_conan_version = ">=2.0"


class Capstone(ConanFile):
    name = "capstone"
    version = "4.0.2"
    url = "https://github.com/capstone-engine/capstone"
    homepage = "https://www.capstone-engine.org/"
    description = "Capstone disassembly/disassembler framework: Core (Arm, Arm64, BPF, EVM, M68K, M680X, MOS65xx, " \
                  "Mips, PPC, RISCV, Sparc, SystemZ, TMS320C64x, Web Assembly, X86, X86_64, XCore) + bindings."
    settings = "build_type", "os", "arch", "compiler"
    build_policy = "missing"

    _platform = None
    _toolset = "v143"

    def source(self):
        git = Git(self)
        git.fetch_commit(self.url, self.version)
        self._patch_sources()

    def _patch_sources(self):
        # Customize Capstone library by modifying the preprocessor definitions
        replace_in_file(self, "msvc/capstone_static/capstone_static.vcxproj",
                        "<PreprocessorDefinitions>CAPSTONE_X86_ATT_DISABLE_NO;CAPSTONE_DIET_NO"
                        ";CAPSTONE_X86_REDUCE_NO;CAPSTONE_HAS_ARM;CAPSTONE_HAS_ARM64;CAPSTONE_HAS_EVM"
                        ";CAPSTONE_HAS_M68K;CAPSTONE_HAS_M680X;CAPSTONE_HAS_MIPS;CAPSTONE_HAS_POWERPC"
                        ";CAPSTONE_HAS_SPARC;CAPSTONE_HAS_SYSZ;CAPSTONE_HAS_TMS320C64X;CAPSTONE_HAS_X86"
                        ";CAPSTONE_HAS_XCORE;CAPSTONE_USE_SYS_DYN_MEM;WIN32;_DEBUG;_LIB;%("
                        "PreprocessorDefinitions)</PreprocessorDefinitions>",
                        "<PreprocessorDefinitions>CAPSTONE_X86_ATT_DISABLE_NO;CAPSTONE_DIET_NO"
                        ";CAPSTONE_X86_REDUCE_NO;CAPSTONE_HAS_X86;CAPSTONE_USE_SYS_DYN_MEM;WIN32;_DEBUG;_LIB;%("
                        "PreprocessorDefinitions)</PreprocessorDefinitions>")

        replace_in_file(self, "msvc/capstone_static/capstone_static.vcxproj",
                        "<PreprocessorDefinitions>CAPSTONE_X86_ATT_DISABLE_NO;CAPSTONE_DIET_NO"
                        ";CAPSTONE_X86_REDUCE_NO;CAPSTONE_HAS_ARM;CAPSTONE_HAS_ARM64;CAPSTONE_HAS_EVM"
                        ";CAPSTONE_HAS_M68K;CAPSTONE_HAS_M680X;CAPSTONE_HAS_MIPS;CAPSTONE_HAS_POWERPC"
                        ";CAPSTONE_HAS_SPARC;CAPSTONE_HAS_SYSZ;CAPSTONE_HAS_TMS320C64X;CAPSTONE_HAS_X86"
                        ";CAPSTONE_HAS_XCORE;CAPSTONE_USE_SYS_DYN_MEM;WIN32;NDEBUG;_LIB;%("
                        "PreprocessorDefinitions)</PreprocessorDefinitions>",
                        "<PreprocessorDefinitions>CAPSTONE_X86_ATT_DISABLE_NO;CAPSTONE_DIET_NO"
                        ";CAPSTONE_X86_REDUCE_NO;CAPSTONE_HAS_X86;CAPSTONE_USE_SYS_DYN_MEM;WIN32;NDEBUG;_LIB;%("
                        "PreprocessorDefinitions)</PreprocessorDefinitions>")

        replace_in_file(self, "msvc/capstone_static/capstone_static.vcxproj",
                        "<SubSystem>Windows</SubSystem>", "<SubSystem>Console</SubSystem>")

    def validate(self):
        if self.settings.arch == "x86_64":
            self._platform = "x64"
        else:
            raise ConanException("Unsupported architecture")

    def generate(self):
        tc = MSBuildToolchain(self)
        tc.toolset = self._toolset
        tc.generate()

    def build(self):
        msbuild = MSBuild(self)
        # hacky way to add parameters to the build command
        msbuild.platform = f"{self._platform} /p:PlatformToolset={self._toolset} /p:ForceImportAfterCppDefaultProps={self.build_folder}/conan_toolchain.props"
        msbuild.build("msvc/capstone.sln", targets=["capstone_static"])

    def package(self):
        copy(self, pattern="*", src=f"{self.source_folder}/include", dst=f"{self.package_folder}/include")
        copy(self, pattern="*", src=f"{self.build_folder}/msvc/{self._platform}/{self.settings.build_type}",
             dst=f"{self.package_folder}/lib", keep_path=False)
        symlinks.absolute_to_relative_symlinks(self, self.package_folder)

    def package_info(self):
        self.cpp_info.libs = ["capstone"]
