# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: aftl.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import trillian_pb2 as trillian__pb2
from crypto.sigpb import sigpb_pb2 as crypto_dot_sigpb_dot_sigpb__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='aftl.proto',
  package='aftl',
  syntax='proto3',
  serialized_options=_b('Z\005proto'),
  serialized_pb=_b('\n\naftl.proto\x12\x04\x61\x66tl\x1a\x0etrillian.proto\x1a\x18\x63rypto/sigpb/sigpb.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\x8a\x01\n\x0c\x46irmwareInfo\x12\x13\n\x0bvbmeta_hash\x18\x01 \x01(\x0c\x12\x1b\n\x13version_incremental\x18\x02 \x01(\t\x12\x14\n\x0cplatform_key\x18\x03 \x01(\x0c\x12\x1d\n\x15manufacturer_key_hash\x18\x04 \x01(\x0c\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\"f\n\x12SignedFirmwareInfo\x12 \n\x04info\x18\x01 \x01(\x0b\x32\x12.aftl.FirmwareInfo\x12.\n\x0einfo_signature\x18\x02 \x01(\x0b\x32\x16.sigpb.DigitallySigned\"Q\n\x11\x46irmwareImageInfo\x12\x13\n\x0bvbmeta_hash\x18\x01 \x01(\x0c\x12\x0c\n\x04hash\x18\x02 \x01(\x0c\x12\x19\n\x11\x62uild_fingerprint\x18\x03 \x01(\t\"|\n\x17SignedFirmwareImageInfo\x12+\n\nimage_info\x18\x01 \x01(\x0b\x32\x17.aftl.FirmwareImageInfo\x12\x34\n\x14image_info_signature\x18\x02 \x01(\x0b\x32\x16.sigpb.DigitallySigned\"V\n\x0eInclusionProof\x12\x1e\n\x05proof\x18\x01 \x01(\x0b\x32\x0f.trillian.Proof\x12$\n\x03sth\x18\x02 \x01(\x0b\x32\x17.trillian.SignedLogRoot\"\xce\x01\n\x04Leaf\x12\x0f\n\x07version\x18\x01 \x01(\x05\x12-\n\ttimestamp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x10\n\x06vbmeta\x18\x03 \x01(\x0cH\x00\x12/\n\x07\x66w_info\x18\x04 \x01(\x0b\x32\x1c.aftl.FirmwareInfoAnnotationH\x00\x12:\n\rfw_image_info\x18\x05 \x01(\x0b\x32!.aftl.FirmwareImageInfoAnnotationH\x00\x42\x07\n\x05value\"@\n\x16\x46irmwareInfoAnnotation\x12&\n\x04info\x18\x01 \x01(\x0b\x32\x18.aftl.SignedFirmwareInfo\"W\n\x1b\x46irmwareImageInfoAnnotation\x12+\n\x04info\x18\x01 \x01(\x0b\x32\x1d.aftl.SignedFirmwareImageInfo\x12\x0b\n\x03url\x18\x02 \x01(\tB\x07Z\x05protob\x06proto3')
  ,
  dependencies=[trillian__pb2.DESCRIPTOR,crypto_dot_sigpb_dot_sigpb__pb2.DESCRIPTOR,google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])




_FIRMWAREINFO = _descriptor.Descriptor(
  name='FirmwareInfo',
  full_name='aftl.FirmwareInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='vbmeta_hash', full_name='aftl.FirmwareInfo.vbmeta_hash', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='version_incremental', full_name='aftl.FirmwareInfo.version_incremental', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='platform_key', full_name='aftl.FirmwareInfo.platform_key', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='manufacturer_key_hash', full_name='aftl.FirmwareInfo.manufacturer_key_hash', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='aftl.FirmwareInfo.description', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=96,
  serialized_end=234,
)


_SIGNEDFIRMWAREINFO = _descriptor.Descriptor(
  name='SignedFirmwareInfo',
  full_name='aftl.SignedFirmwareInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='info', full_name='aftl.SignedFirmwareInfo.info', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='info_signature', full_name='aftl.SignedFirmwareInfo.info_signature', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=236,
  serialized_end=338,
)


_FIRMWAREIMAGEINFO = _descriptor.Descriptor(
  name='FirmwareImageInfo',
  full_name='aftl.FirmwareImageInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='vbmeta_hash', full_name='aftl.FirmwareImageInfo.vbmeta_hash', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hash', full_name='aftl.FirmwareImageInfo.hash', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='build_fingerprint', full_name='aftl.FirmwareImageInfo.build_fingerprint', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=340,
  serialized_end=421,
)


_SIGNEDFIRMWAREIMAGEINFO = _descriptor.Descriptor(
  name='SignedFirmwareImageInfo',
  full_name='aftl.SignedFirmwareImageInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='image_info', full_name='aftl.SignedFirmwareImageInfo.image_info', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='image_info_signature', full_name='aftl.SignedFirmwareImageInfo.image_info_signature', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=423,
  serialized_end=547,
)


_INCLUSIONPROOF = _descriptor.Descriptor(
  name='InclusionProof',
  full_name='aftl.InclusionProof',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='proof', full_name='aftl.InclusionProof.proof', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sth', full_name='aftl.InclusionProof.sth', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=549,
  serialized_end=635,
)


_LEAF = _descriptor.Descriptor(
  name='Leaf',
  full_name='aftl.Leaf',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='aftl.Leaf.version', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='aftl.Leaf.timestamp', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='vbmeta', full_name='aftl.Leaf.vbmeta', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fw_info', full_name='aftl.Leaf.fw_info', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fw_image_info', full_name='aftl.Leaf.fw_image_info', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='value', full_name='aftl.Leaf.value',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=638,
  serialized_end=844,
)


_FIRMWAREINFOANNOTATION = _descriptor.Descriptor(
  name='FirmwareInfoAnnotation',
  full_name='aftl.FirmwareInfoAnnotation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='info', full_name='aftl.FirmwareInfoAnnotation.info', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=846,
  serialized_end=910,
)


_FIRMWAREIMAGEINFOANNOTATION = _descriptor.Descriptor(
  name='FirmwareImageInfoAnnotation',
  full_name='aftl.FirmwareImageInfoAnnotation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='info', full_name='aftl.FirmwareImageInfoAnnotation.info', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='url', full_name='aftl.FirmwareImageInfoAnnotation.url', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=912,
  serialized_end=999,
)

_SIGNEDFIRMWAREINFO.fields_by_name['info'].message_type = _FIRMWAREINFO
_SIGNEDFIRMWAREINFO.fields_by_name['info_signature'].message_type = crypto_dot_sigpb_dot_sigpb__pb2._DIGITALLYSIGNED
_SIGNEDFIRMWAREIMAGEINFO.fields_by_name['image_info'].message_type = _FIRMWAREIMAGEINFO
_SIGNEDFIRMWAREIMAGEINFO.fields_by_name['image_info_signature'].message_type = crypto_dot_sigpb_dot_sigpb__pb2._DIGITALLYSIGNED
_INCLUSIONPROOF.fields_by_name['proof'].message_type = trillian__pb2._PROOF
_INCLUSIONPROOF.fields_by_name['sth'].message_type = trillian__pb2._SIGNEDLOGROOT
_LEAF.fields_by_name['timestamp'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_LEAF.fields_by_name['fw_info'].message_type = _FIRMWAREINFOANNOTATION
_LEAF.fields_by_name['fw_image_info'].message_type = _FIRMWAREIMAGEINFOANNOTATION
_LEAF.oneofs_by_name['value'].fields.append(
  _LEAF.fields_by_name['vbmeta'])
_LEAF.fields_by_name['vbmeta'].containing_oneof = _LEAF.oneofs_by_name['value']
_LEAF.oneofs_by_name['value'].fields.append(
  _LEAF.fields_by_name['fw_info'])
_LEAF.fields_by_name['fw_info'].containing_oneof = _LEAF.oneofs_by_name['value']
_LEAF.oneofs_by_name['value'].fields.append(
  _LEAF.fields_by_name['fw_image_info'])
_LEAF.fields_by_name['fw_image_info'].containing_oneof = _LEAF.oneofs_by_name['value']
_FIRMWAREINFOANNOTATION.fields_by_name['info'].message_type = _SIGNEDFIRMWAREINFO
_FIRMWAREIMAGEINFOANNOTATION.fields_by_name['info'].message_type = _SIGNEDFIRMWAREIMAGEINFO
DESCRIPTOR.message_types_by_name['FirmwareInfo'] = _FIRMWAREINFO
DESCRIPTOR.message_types_by_name['SignedFirmwareInfo'] = _SIGNEDFIRMWAREINFO
DESCRIPTOR.message_types_by_name['FirmwareImageInfo'] = _FIRMWAREIMAGEINFO
DESCRIPTOR.message_types_by_name['SignedFirmwareImageInfo'] = _SIGNEDFIRMWAREIMAGEINFO
DESCRIPTOR.message_types_by_name['InclusionProof'] = _INCLUSIONPROOF
DESCRIPTOR.message_types_by_name['Leaf'] = _LEAF
DESCRIPTOR.message_types_by_name['FirmwareInfoAnnotation'] = _FIRMWAREINFOANNOTATION
DESCRIPTOR.message_types_by_name['FirmwareImageInfoAnnotation'] = _FIRMWAREIMAGEINFOANNOTATION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FirmwareInfo = _reflection.GeneratedProtocolMessageType('FirmwareInfo', (_message.Message,), {
  'DESCRIPTOR' : _FIRMWAREINFO,
  '__module__' : 'aftl_pb2'
  # @@protoc_insertion_point(class_scope:aftl.FirmwareInfo)
  })
_sym_db.RegisterMessage(FirmwareInfo)

SignedFirmwareInfo = _reflection.GeneratedProtocolMessageType('SignedFirmwareInfo', (_message.Message,), {
  'DESCRIPTOR' : _SIGNEDFIRMWAREINFO,
  '__module__' : 'aftl_pb2'
  # @@protoc_insertion_point(class_scope:aftl.SignedFirmwareInfo)
  })
_sym_db.RegisterMessage(SignedFirmwareInfo)

FirmwareImageInfo = _reflection.GeneratedProtocolMessageType('FirmwareImageInfo', (_message.Message,), {
  'DESCRIPTOR' : _FIRMWAREIMAGEINFO,
  '__module__' : 'aftl_pb2'
  # @@protoc_insertion_point(class_scope:aftl.FirmwareImageInfo)
  })
_sym_db.RegisterMessage(FirmwareImageInfo)

SignedFirmwareImageInfo = _reflection.GeneratedProtocolMessageType('SignedFirmwareImageInfo', (_message.Message,), {
  'DESCRIPTOR' : _SIGNEDFIRMWAREIMAGEINFO,
  '__module__' : 'aftl_pb2'
  # @@protoc_insertion_point(class_scope:aftl.SignedFirmwareImageInfo)
  })
_sym_db.RegisterMessage(SignedFirmwareImageInfo)

InclusionProof = _reflection.GeneratedProtocolMessageType('InclusionProof', (_message.Message,), {
  'DESCRIPTOR' : _INCLUSIONPROOF,
  '__module__' : 'aftl_pb2'
  # @@protoc_insertion_point(class_scope:aftl.InclusionProof)
  })
_sym_db.RegisterMessage(InclusionProof)

Leaf = _reflection.GeneratedProtocolMessageType('Leaf', (_message.Message,), {
  'DESCRIPTOR' : _LEAF,
  '__module__' : 'aftl_pb2'
  # @@protoc_insertion_point(class_scope:aftl.Leaf)
  })
_sym_db.RegisterMessage(Leaf)

FirmwareInfoAnnotation = _reflection.GeneratedProtocolMessageType('FirmwareInfoAnnotation', (_message.Message,), {
  'DESCRIPTOR' : _FIRMWAREINFOANNOTATION,
  '__module__' : 'aftl_pb2'
  # @@protoc_insertion_point(class_scope:aftl.FirmwareInfoAnnotation)
  })
_sym_db.RegisterMessage(FirmwareInfoAnnotation)

FirmwareImageInfoAnnotation = _reflection.GeneratedProtocolMessageType('FirmwareImageInfoAnnotation', (_message.Message,), {
  'DESCRIPTOR' : _FIRMWAREIMAGEINFOANNOTATION,
  '__module__' : 'aftl_pb2'
  # @@protoc_insertion_point(class_scope:aftl.FirmwareImageInfoAnnotation)
  })
_sym_db.RegisterMessage(FirmwareImageInfoAnnotation)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
