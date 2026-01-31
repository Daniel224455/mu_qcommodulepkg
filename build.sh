stuart_setup -c QcomModulePkg/PlatformBuild.py
stuart_update -c QcomModulePkg/PlatformBuild.py
stuart_build -c QcomModulePkg/PlatformBuild.py

if [ ! -d "sectools" ]; then
	git clone https://github.com/rubikpi-dev/sectools.git
fi

python QcomModulePkg/Tools/image_header.py Build/QcomModulePkg/DEBUG_CLANGDWARF/FV/FVMAIN_COMPACT.Fv abl.elf 0x9fa00000 elf 32

python sectools/sectools_builder.py \
  -t ./Build/signed \
  -i ./abl.elf \
  -g uefifv \
  --config sectools/config/integration/secimage_eccv3.xml \
  --hash_table_algo sha384 \
  --soc_hw_version 0x60180100 \
  --soc_vers 0x6018 \
  --build_policy_id DEFAULT_SIGN

rm abl.elf
cp Build/signed/sign/default/uefifv/abl.elf .