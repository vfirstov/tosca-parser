#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import hashlib


def hash_bytestr_iter(bytesiter, hasher, ashexstr=False):
    for block in bytesiter:
        hasher.update(block)
    return hasher.hexdigest() if ashexstr else hasher.digest()


def file_as_blockiter(afile, blocksize=65536):
    with afile:
        block = afile.read(blocksize)
        while len(block) > 0:
            yield block
            block = afile.read(blocksize)


def hash_all(template_path, import_dirs):

    hasher = hashlib.sha256()
    hashes = list()
    hashes.append(
        hash_bytestr_iter(
            file_as_blockiter(open(template_path, 'rb')), hashlib.sha256()
        )
    )

    template_dir = os.path.dirname(template_path)
    if isinstance(import_dirs, set):
        for _f_name in import_dirs:
            hashes.append(
                hash_bytestr_iter(
                    file_as_blockiter(
                        open(os.path.normpath(os.path.join(template_dir, _f_name)), 'rb')
                    ),
                    hashlib.sha256()
                )
            )
    else:
        for root, dirs, files in os.walk(import_dirs, topdown=True):
            dirs.sort()
            files.sort()
            for f_name in files:
                hashes.append(
                    hash_bytestr_iter(
                        file_as_blockiter(
                            open(os.path.normpath(os.path.join(root, f_name)), 'rb')
                        ),
                        hashlib.sha256()
                    )
                )

    for val in sorted(hashes):
        hasher.update(val)
    return hasher.hexdigest()