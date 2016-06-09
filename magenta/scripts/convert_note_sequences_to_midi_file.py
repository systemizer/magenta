# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
r""""Converts TFRecord file of NoteSequence protos to MIDI files

Sample usage:
  $ bazel build magenta:convert_note_sequences_to_midi_file
  $ bazel-bin/magenta/convert_note_sequences_to_midi_file \
    --tfrecord_file=/path/to/tfrecord/file \
    --output_file=/path/to/midi/file
"""

import os

import tensorflow as tf

from magenta.lib import midi_io
from magenta.lib import note_sequence_io

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string('tfrecord_file', None,
                           'Path to the tfrecord file containing NoteSequences.')
tf.app.flags.DEFINE_string('output_dir', None,
                           'Path to directory where MIDI files will be written. Will be overwritten '
                           'if it already exists.')


def main(unused_argv):
  if not FLAGS.tfrecord_file:
    tf.logging.fatal('--tfrecord_file required')
    return
  if not FLAGS.output_dir:
    tf.logging.fatal('--output_dir required')
    return
  for note_sequence in note_sequence_io.note_sequence_record_iterator(FLAGS.tfrecord_file):
      pm = midi_io.sequence_proto_to_pretty_midi(note_sequence)
      pm.write(os.path.join(FLAGS.output_dir, note_sequence.filename))

if __name__ == '__main__':
  tf.app.run()
