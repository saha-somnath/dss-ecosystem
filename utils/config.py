#!/usr/bin/python
"""
 *   BSD LICENSE
 *
 *   Copyright (c) 2021 Samsung Electronics Co., Ltd.
 *   All rights reserved.
 *
 *   Redistribution and use in source and binary forms, with or without
 *   modification, are permitted provided that the following conditions
 *   are met:
 *
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in
 *       the documentation and/or other materials provided with the
 *       distribution.
 *     * Neither the name of Samsung Electronics Co., Ltd. nor the names of
 *       its contributors may be used to endorse or promote products derived
 *       from this software without specific prior written permission.
 *
 *   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 *   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 *   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 *   A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 *   OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 *   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 *   LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 *   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 *   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 *   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 *   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import os,sys
import json
import argparse

class Config:

    def __init__(self, params):
        self.config_file = self.get_config_file(params.get("config"))
        self.params = params
        self.config = self.process_config()


    def get_config(self):
        """
        Get configuration details from config file ...
        :return:<dict> complete configuration dictionary.
        """
        return self.config


    def process_config(self):
        config = {}
        with open(self.config_file, "rb") as cfg:
            config = json.loads(cfg.read().decode('UTF-8', "ignore"))
        if self.params:
            for param in self.params:
                config[param] = self.params[param]
        return config


    def get_config_file(self, config_file):
        """
        Return the configuration file.
        :param config_file:
        :return:<string> complete configuration file
        """
        if not config_file:
            config_file = os.path.dirname(__file__) + "/../config/config.json"
            config_file = os.path.abspath(config_file)
            print("INFO: Using configuration file from {}".format(config_file))
        return config_file


def commandLineArgumentParser():
  parser = argparse.ArgumentParser(description='TESS Copy a NFS data mover tool!')
  subparser=parser.add_subparsers(help="Supported Operations ... ")

  put_parser=subparser.add_parser("PUT", help="Upload the files to S3 storage")
  list_parser = subparser.add_parser("LIST", help="List the buckets/objects from S3 storage!")
  get_parser = subparser.add_parser("GET", help="Download the files from S3 storage bucket!")
  del_parser = subparser.add_parser("DEL", help="Remove the objects from the S3 storage bucket!")

  ## All arguments for PUT
  put_parser.add_argument("--thread", "-t", type=int, default=1, required=False,
                      help='Specify number of Jobs to be used for parallel processing. ')
  put_parser.add_argument("--bucket", "-b", type=str, required=False, help='Specify bucket name.. ')
  put_parser.add_argument("--cluster", "-c", type=str, nargs="+", default="10.1.51.2", required=True,
                      help='Specify cluster name  ...')
  put_parser.add_argument("--prefix", "-p", type=str, required=False,
                      help='Specify operation type such as read=r write=w , wr...')
  put_parser.add_argument("--config", "-cfg", type=str, required=False, help='Specify configuration file path')

  ## All arguments for LIST
  list_parser.add_argument("--thread", "-t", type=int, default=1, required=False,
                          help='Specify number of Jobs to be used for parallel processing. ')
  list_parser.add_argument("--bucket", "-b", type=str, required=False, help='Specify bucket name.. ')
  list_parser.add_argument("--cluster", "-c", type=str, nargs="+", default="10.1.51.2", required=True,
                          help='Specify cluster name  ...')
  list_parser.add_argument("--prefix", "-p", type=str, required=False,
                          help='Specify operation type such as read=r write=w , wr...')
  list_parser.add_argument("--config", "-cfg", type=str, required=False, help='Specify configuration file path')

  ## All arguments for GET
  get_parser.add_argument("--thread", "-t", type=int, default=1, required=False,
                          help='Specify number of Jobs to be used for parallel processing. ')
  get_parser.add_argument("--bucket", "-b", type=str, required=False, help='Specify bucket name.. ')
  get_parser.add_argument("--cluster", "-c", type=str, nargs="+", default="10.1.51.2", required=True,
                          help='Specify cluster name  ...')
  get_parser.add_argument("--prefix", "-p", type=str, required=False,
                          help='Specify operation type such as read=r write=w , wr...')
  get_parser.add_argument("--config", "-cfg", type=str, required=False, help='Specify configuration file path')

  ## All arguments for DEL
  del_parser.add_argument("--thread", "-t", type=int, default=1, required=False,
                          help='Specify number of Jobs to be used for parallel processing. ')
  del_parser.add_argument("--bucket", "-b", type=str, required=False, help='Specify bucket name.. ')
  del_parser.add_argument("--cluster", "-c", type=str, nargs=  "+", default="10.1.51.2", required=True,
                          help='Specify cluster name  ...')
  del_parser.add_argument("--prefix", "-p", type=str, required=False,
                          help='Specify operation type such as read=r write=w , wr...')
  del_parser.add_argument("--config", "-cfg", type=str, required=False, help='Specify configuration file path')


  options = parser.parse_args()

  return ( sys.argv[1:2][0], vars(options) )


def ClientApplicationArgumentParser():
    parser = argparse.ArgumentParser(description='TESS Copy a NFS data mover tool!')
    parser.add_argument("--client_id", "-id", type=int, default=1, required=True,
                            help='Specify client node IP address ')
    parser.add_argument("--operation", "-op", type=str, required=True, help='Specify operation such as PUT,LIST,DEL,GET')
    parser.add_argument("--ip_address", "-ip", type=str, required=True,
                        help='Specify Client Node IP address')
    parser.add_argument("--master_node", "-mn", required=False, action='store_true',
                        help='Is client running on same node of master?')
    parser.add_argument("--config", "-cfg", type=str, required=False, help='Specify configuration file path')
    parser.add_argument("--dryrun", "-dr", required=False, action='store_true',
                           help='Dry run - Just check operation is working , but does not actual upload')
    parser.add_argument("--port_index", "-pi", type=str, required=True, help='Specify index port')
    parser.add_argument("--port_status", "-ps", type=str, required=True, help='Specify status port')
    parser.add_argument("--dest_path", "-dp", type=str, required=False, help='Specify Destination Directory for GET operation only')

    options = vars(parser.parse_args())
    return options

class CommandLineArgument:
    def __init__(self):
        parser = argparse.ArgumentParser(description='TESS Copy!')
        subparsers = parser.add_subparsers(help="Supported Operations ... ")
        put_parser = subparsers.add_parser("PUT", help="Upload the files to S3 storage")
        list_parser = subparsers.add_parser("LIST", help="List the buckets/objects from S3 storage!")
        get_parser = subparsers.add_parser("GET", help="Download the files from S3 storage bucket!")
        del_parser = subparsers.add_parser("DEL", help="Remove the objects from the S3 storage bucket!")

        if not  sys.argv[1:2]:
            parser.print_help()
            sys.exit()

        self.operation = sys.argv[1:2][0]

        #if not hasattr(self, self.operation):
        #    self.parser.print_help()
        #    sys.exit()

        if self.operation.upper() == "PUT":
            self.put(put_parser)
        elif self.operation.upper() == "GET":
            self.get(get_parser)
        elif self.operation.upper() == "LIST":
            self.list(list_parser)
        elif self.operation.upper() == "DEL":
            self.delete(del_parser)
        else:
            self.parser.print_help()
            sys.exit()

        self.options = vars(parser.parse_args())


    def put(self, subparser):
        subparser.add_argument("--thread", "-t", type=int, default=1, required=False,
                                help='Specify number of Jobs to be used for parallel processing. ')
        subparser.add_argument("--bucket", "-b", type=str, required=False, help='Specify bucket name.. ')
        subparser.add_argument("--cluster", "-c", type=str, nargs="+", default="10.1.51.2", required=True,
                                help='Specify cluster name  ...')
        subparser.add_argument("--prefix", "-p", type=str, required=False,
                                help='Specify operation type such as read=r write=w , wr...')
        subparser.add_argument("--config", "-cfg", type=str, required=False, help='Specify configuration file path')
        subparser.add_argument("--compaction", "-com", required=False, action='store_true', help='Enable target compaction')
        subparser.add_argument("--dryrun", "-dr", required=False, action='store_true',
                               help='Dry run - Just check operation is working , but does not actual upload')

    def get(self,subparser):
        subparser.add_argument("--thread", "-t", type=int, default=1, required=False,
                                help='Specify number of Jobs to be used for parallel processing. ')
        subparser.add_argument("--bucket", "-b", type=str, required=False, help='Specify bucket name.. ')
        subparser.add_argument("--cluster", "-c", type=str, nargs="+", default="10.1.51.2", required=True,
                                help='Specify cluster name  ...')
        subparser.add_argument("--prefix", "-p", type=str, required=False,
                                help='Specify operation type such as read=r write=w , wr...')
        subparser.add_argument("--config", "-cfg", type=str, required=False, help='Specify configuration file path')
        subparser.add_argument("--dest_path", "-d", type=str, required=True, help='Specify destination file path')
        subparser.add_argument("--dryrun", "-dr", required=False, action='store_true',
                               help='Dry run - Just check operation is working , but does not actual download')

    def list(self,subparser):
        subparser.add_argument("--thread", "-t", type=int, default=1, required=False,
                                 help='Specify number of Jobs to be used for parallel processing. ')
        subparser.add_argument("--bucket", "-b", type=str, required=False, help='Specify bucket name.. ')
        subparser.add_argument("--cluster", "-c", type=str, nargs="+", default="10.1.51.2", required=True,
                                 help='Specify cluster name  ...')
        subparser.add_argument("--prefix", "-p", type=str, required=False,
                                 help='Specify operation type such as read=r write=w , wr...')
        subparser.add_argument("--config", "-cfg", type=str, required=False, help='Specify configuration file path')
        subparser.add_argument("--dryrun", "-dr", required=False, action='store_true',
                               help='Dry run - Just check operation is working , but does not actual listing')
    def delete(self,subparser):
        subparser.add_argument("--thread", "-t", type=int, default=1, required=False,
                                help='Specify number of Jobs to be used for parallel processing. ')
        subparser.add_argument("--bucket", "-b", type=str, required=False, help='Specify bucket name.. ')
        subparser.add_argument("--cluster", "-c", type=str, nargs="+", default="10.1.51.2", required=True,
                                help='Specify cluster name  ...')
        subparser.add_argument("--prefix", "-p", type=str, required=False,
                                help='Specify operation type such as read=r write=w , wr...')
        subparser.add_argument("--compaction", "-com", required=False, action='store_true',
                               help='Enable target compaction')
        subparser.add_argument("--config", "-cfg", type=str, required=False, help='Specify configuration file path')
        subparser.add_argument("--dryrun", "-dr", required=False, action='store_true',
                               help='Dry run - Just check operation is working , but does not actual delete')
    def get_operation(self):
        return sys.argv[1:2][0]