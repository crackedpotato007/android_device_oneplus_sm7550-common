#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/oneplus/sm7550-common',
    'hardware/qcom-caf/sm8550',
    'hardware/qcom-caf/wlan',
    'hardware/oplus',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
]


def lib_fixup_odm_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'odm' else None


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'libpwirisfeature',
        'libpwirishalwrapper',
    ): lib_fixup_odm_suffix,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'libhwconfigurationutil',
        'vendor.oplus.hardware.cammidasservice-V1-ndk',
        'vendor.oplus.hardware.communicationcenter-V2-ndk',
        'vendor.oplus.hardware.performance-V1-ndk',
        'vendor.qti.diaghal@1.0',
        'vendor.qti.hardware.dpmservice@1.0',
        'vendor.qti.hardware.qccsyshal@1.0',
        'vendor.qti.hardware.qccsyshal@1.1',
        'vendor.qti.hardware.qccsyshal@1.2',
        'vendor.qti.hardware.qccvndhal@1.0',
        'vendor.qti.hardware.wifidisplaysession@1.0',
        'vendor.qti.imsrtpservice@3.0',
        'vendor.qti.imsrtpservice@3.1',
    ): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    'odm/bin/hw/vendor-oplus-hardware-performance-V1-service': blob_fixup()
        .add_needed('libbase_shim.so')
        .add_needed('libprocessgroup_shim.so'),
    'odm/lib64/libAlgoProcess.so': blob_fixup()
        .replace_needed('android.hardware.graphics.common-V3-ndk.so', 'android.hardware.graphics.common-V6-ndk.so'),
    ('odm/lib64/libCOppLceTonemapAPI.so', 'odm/lib64/libSuperRaw.so', 'odm/lib64/libYTCommon.so', 'odm/lib64/libyuv2.so', 'odm/lib64/libaps_frame_registration.so'): blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    ('odm/lib64/libHIS.so', 'odm/lib64/libOGLManager.so'): blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),
    'odm/lib64/libarcsoft_high_dynamic_range_v4.so': blob_fixup()
        .clear_symbol_version('remote_handle_close')
        .clear_symbol_version('remote_handle_invoke')
        .clear_symbol_version('remote_handle_open')
        .clear_symbol_version('remote_register_buf_attr')
        .clear_symbol_version('remote_register_buf'),
    'odm/lib64/libextensionlayer.so': blob_fixup()
        .replace_needed('libziparchive.so', 'libziparchive_odm.so'),
    'product/etc/sysconfig/com.android.hotwordenrollment.common.util.xml': blob_fixup()
        .regex_replace('/my_product', '/product'),
    ('vendor/etc/media_codecs_crow_v0.xml', 'vendor/etc/media_codecs_crow_v1.xml', 'vendor/etc/media_codecs_crow_v2.xml'): blob_fixup()
        .regex_replace('.*media_codecs_(google_audio|google_c2|google_telephony|google_video|vendor_audio).*\n', ''),
    'vendor/etc/seccomp_policy/qwesd@2.0.policy': blob_fixup()
        .add_line_if_missing('pipe2: 1'),
    'vendor/lib64/libqcodec2_core.so': blob_fixup()
        .add_needed('libcodec2_shim.so'),
    'vendor/lib64/vendor.libdpmframework.so': blob_fixup()
        .add_needed('libhidlbase_shim.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'sm7550-common',
    'oneplus',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
