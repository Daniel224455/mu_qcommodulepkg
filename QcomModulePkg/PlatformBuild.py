##
## Script to Build LinuxLoader
##
## Copyright (C) Microsoft.
## Copyright (C) Daniel224455
##  SPDX-License-Identifier: BSD-2-Clause-Patent
##
import os, sys, logging
from edk2toolext.environment.uefi_build import UefiBuilder
from edk2toolext.invocables.edk2_platform_build import BuildSettingsManager
from edk2toolext.invocables.edk2_setup import SetupSettingsManager
from edk2toolext.invocables.edk2_update import UpdateSettingsManager
from edk2toollib.utility_functions import GetHostInfo
from edk2toolext.invocables.edk2_setup import RequiredSubmodule

class PlatformBuilder(UefiBuilder, UpdateSettingsManager, SetupSettingsManager, BuildSettingsManager):

    def GetWorkspaceRoot(self):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def GetActiveScopes(self):
        return ['hyperv', 'edk2-build']

    def GetPackagesSupported(self):
        return ("QcomModulePkg")

    def GetRequiredSubmodules(self):
        return [
            RequiredSubmodule("MU_BASECORE"),
            RequiredSubmodule("Silicon/ARM/MU_TIANO"),
            RequiredSubmodule("Common/MU_TIANO")
        ]

    def GetPackagesPath(self):
        pp = ('MU_BASECORE', 'Silicon/ARM/MU_TIANO', 'Common/MU_TIANO')
        ws = self.GetWorkspaceRoot()
        return [os.path.join(ws, x) for x in pp]

    def GetArchitecturesSupported(self):
        return ("AARCH64")

    def GetTargetsSupported(self):
        return ("DEBUG", "RELEASE")

    def GetLoggingLevel (self, loggerType):
        return logging.INFO
        return super().GetLoggingLevel(loggerType)

    def SetPlatformEnv(self):
        logging.debug("PlatformBuilder SetPlatformEnv")

        self.env.SetValue("PRODUCT_NAME", "QcomModulePkg", "Platform Hardcoded")
        self.env.SetValue("TOOL_CHAIN_TAG", "CLANGDWARF", "Platform hardcoded")
        self.env.SetValue("BLD_*_BUILD_UNIT_TESTS", "FALSE", "Unit Test build off by default")
        self.env.SetValue("BLD_*_BUILD_APPS", "FALSE", "App Build off by default")
        logging.debug("PlatformBuilder building AARCH64")
        self.env.SetValue("ACTIVE_PLATFORM", "QcomModulePkg/QcomModulePkg.dsc", "Platform Hardcoded")
        self.env.SetValue("TARGET_ARCH", "AARCH64", "Platform Hardcoded")
        self.env.SetValue("ARCH", "AARCH64", "Platform hardcoded")
        self.env.SetValue("BLD_*_BUILDID_STRING", "17.1590.800", "hardcoded for easy build file")
        # self.env.SetValue("BLD_*_[insert arg here] < example
        #self.env.SetValue("USERDATAIMAGE_FILE_SYSTEM_TYPE", "ext4", "Android userdata fs type")
        self.env.SetValue("LaunchBuildLogProgram", "Notepad", "default - will fail if already set", True)
        self.env.SetValue("LaunchLogOnSuccess", "True", "default - will fail if already set", True)
        self.env.SetValue("LaunchLogOnError", "True", "default - will fail if already set", False)

        return 0

    def SetPlatformEnvAfterTarget(self):
        logging.debug("PlatformBuilder SetPlatformEnvAfterTarget")
        return 0

    def PlatformPostBuild(self):
        # sign abl later
        return 0

    def PlatformPreBuild(self):
        return 0

    if __name__ == "__main__":
        import argparse
        import sys
        from edk2toolext.invocables.edk2_update import Edk2Update
        from edk2toolext.invocables.edk2_setup import Edk2PlatformSetup
        from edk2toolext.invocables.edk2_platform_build import Edk2PlatformBuild
        print("Invoking Stuart")
        print(r"     ) _     _")
        print(r"    ( (^)-~-(^)")
        print(r"__,-.\_( 0 0 )__,-.___")
        print(r"  'W'   \   /   'W'")
        print(r"         >o<")
        SCRIPT_PATH = os.path.relpath(__file__)
        parser = argparse.ArgumentParser(add_help=False)
        parse_group = parser.add_mutually_exclusive_group()
        parse_group.add_argument("--update", "--UPDATE",
                                 action='store_true', help="Invokes stuart_update")
        parse_group.add_argument("--setup", "--SETUP",
                                 action='store_true', help="Invokes stuart_setup")
        args, remaining = parser.parse_known_args()
        new_args = ["stuart", "-c", SCRIPT_PATH]
        new_args = new_args + remaining
        sys.argv = new_args
        if args.setup:
            print("Running stuart_setup -c " + SCRIPT_PATH)
            Edk2PlatformSetup().Invoke()
        elif args.update:
            print("Running stuart_update -c " + SCRIPT_PATH)
            Edk2Update().Invoke()
        else:
            print("Running stuart_build -c " + SCRIPT_PATH)
            Edk2PlatformBuild().Invoke()
