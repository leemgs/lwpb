import unittest
import sys
import lwpb


class CodecTestCase(unittest.TestCase):

  def __init__(self, **keywords):
    unittest.TestCase.__init__(self)

    for k, v in keywords.items():
      setattr(self, k, v)

  def runTest(self):

    self.assertEqual(
      self.encoder.encode(self.pydata, self.descriptor, self.msgnum),
      self.pbdata)

    self.assertEqual(
      self.decoder.decode(self.pbdata, self.descriptor, self.msgnum),
      self.pydata)

  def shortDescription(self):
    return self.name



if __name__ == '__main__':

  suite = unittest.TestSuite()

  decoder = lwpb.Decoder()
  encoder = lwpb.Encoder()

  protofile_descriptor = lwpb.Descriptor(lwpb.PROTOFILE_DEFINITION)
  protofile_messages = protofile_descriptor.message_types()
  protofile_bin = file(sys.argv[1]).read()

  msgnum = protofile_messages['google.protobuf.FileDescriptorSet']
  schema_def = decoder.decode(protofile_bin, protofile_descriptor, msgnum)
  schema_descriptor = lwpb.Descriptor(schema_def['file'][0])
  schema_messages = schema_descriptor.message_types()

  block = []

  f = open(sys.argv[2])

  for line in f:
    line = line.rstrip('\r\n')

    if line != "":
      block.append(line)
    elif len(block) >= 4:
      (name, msgname, pystr, pb2str) = block

      suite.addTest(CodecTestCase(
        name=name,
        encoder=encoder,
        decoder=decoder,
        descriptor=schema_descriptor,
        msgnum=schema_messages[msgname],
        pydata=eval(pystr),
        pbdata=pb2str.strip('"').decode('string_escape')
      ))

      block = []

  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)
